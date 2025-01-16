"""
sudo apt install texlive-xetex texlive-latex-extra texlive-fonts-recommended fonts-freefont-ttf ttf-mscorefonts-installer

The script includes:

Default letter-size paper
Portrait/landscape orientation options
Custom font and font size for image captions
Proper handling of multiple images per page
Timestamp-based image sorting

python latex-picture-book.py --image-directory ./images --output-directory ./output \
    --document-name photobook --page-size legal --orientation landscape
"""
import os
import argparse
from PIL import Image
import subprocess
from datetime import datetime


def get_image_creation_time(filepath):
    """Get file creation/modification time."""
    return os.path.getmtime(filepath)


def escape_latex_filename(filename):
    """Escape special characters in filenames for LaTeX."""
    filename = filename.replace('_', '\\_')
    special_chars = ['&', '%', '$', '#', '{', '}', '~', '^']
    for char in special_chars:
        filename = filename.replace(char, f'\\{char}')
    return filename


def get_image_dimensions_in_inches(image_path, usable_width, usable_height, scaling_factor):
    """Get image dimensions in inches, applying scaling factor and page constraints."""
    with Image.open(image_path) as img:
        # Use a default DPI of 96 for sizing
        base_dpi = 96

        # Convert pixels to inches at base DPI and apply scaling factor
        width_in = (img.width / base_dpi) * scaling_factor
        height_in = (img.height / base_dpi) * scaling_factor

        # Scale down further if image is still larger than page
        if width_in > usable_width or height_in > usable_height:
            width_scale = usable_width / width_in
            height_scale = usable_height / height_in
            scale = min(width_scale, height_scale) * 0.95  # Add 5% margin for safety

            width_in *= scale
            height_in *= scale

        return width_in, height_in


def calculate_page_dimensions(page_size, orientation):
    """Calculate usable page dimensions in inches, accounting for margins."""
    margins = 0.5  # 0.5 inch margins

    if page_size.lower() == 'letter':
        width, height = (11, 8.5) if orientation == 'landscape' else (8.5, 11)
    elif page_size.lower() == 'a4':
        width, height = (11.69, 8.27) if orientation == 'landscape' else (8.27, 11.69)
    elif page_size.lower() == 'legal':
        width, height = (14, 8.5) if orientation == 'landscape' else (8.5, 14)

    # Account for margins
    usable_width = width - (2 * margins)
    usable_height = height - (2 * margins)

    return usable_width, usable_height


def group_images_for_pages(image_files, image_dir, usable_width, usable_height, scaling_factor):
    """Group images that can fit together on the same page."""
    pages = []
    current_page = []
    current_y = 0
    max_spacing = 0.3  # inches between images

    for filename, _ in image_files:
        filepath = os.path.join(image_dir, filename)
        img_width, img_height = get_image_dimensions_in_inches(filepath, usable_width, usable_height, scaling_factor)

        # If this is the first image on the page or it fits with existing images
        if not current_page or (current_y + img_height + max_spacing <= usable_height):
            current_page.append({
                'filename': filename,
                'width': img_width,
                'height': img_height
            })
            current_y += img_height + max_spacing
        else:
            # Start new page
            pages.append(current_page)
            current_page = [{
                'filename': filename,
                'width': img_width,
                'height': img_height
            }]
            current_y = img_height + max_spacing

    if current_page:
        pages.append(current_page)

    return pages


def create_latex_picture_book(image_dir, output_dir, doc_name, page_size="letter", orientation="portrait",
                              scaling_factor=0.50):
    """Creates a LaTeX picture book from images in a directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f"{doc_name}.tex")

    # Get usable page dimensions
    usable_width, usable_height = calculate_page_dimensions(page_size, orientation)

    # Get list of image files sorted by timestamp
    image_files = []
    for filename in os.listdir(image_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            filepath = os.path.join(image_dir, filename)
            image_files.append((filename, get_image_creation_time(filepath)))

    image_files.sort(key=lambda x: x[1])  # Sort by timestamp

    # Group images into pages
    pages = group_images_for_pages(image_files, image_dir, usable_width, usable_height, scaling_factor)

    with open(output_file, "w") as f:
        # Document preamble
        f.write("\\documentclass{article}\n")
        f.write("\\usepackage{graphicx}\n")
        f.write("\\usepackage[utf8]{inputenc}\n")
        f.write("\\usepackage[margin=0.5in]{geometry}\n")
        f.write("\\usepackage{float}\n")

        # Set page size and orientation
        if orientation.lower() == 'landscape':
            if page_size.lower() == 'letter':
                f.write("\\geometry{paperwidth=11in,paperheight=8.5in}\n")
            elif page_size.lower() == 'a4':
                f.write("\\geometry{paperwidth=297mm,paperheight=210mm}\n")
            elif page_size.lower() == 'legal':
                f.write("\\geometry{paperwidth=14in,paperheight=8.5in}\n")
        else:
            if page_size.lower() == 'letter':
                f.write("\\geometry{paperwidth=8.5in,paperheight=11in}\n")
            elif page_size.lower() == 'a4':
                f.write("\\geometry{paperwidth=210mm,paperheight=297mm}\n")
            elif page_size.lower() == 'legal':
                f.write("\\geometry{paperwidth=8.5in,paperheight=14in}\n")

        # Set up graphics path
        f.write(f"\\graphicspath{{{{{image_dir}/}}}}\n")
        f.write("\\pagestyle{empty}\n")

        f.write("\\begin{document}\n")

        # Process each page of images
        for page in pages:
            f.write("\\begin{center}\n")

            for img in page:
                filename = img['filename']
                escaped_filename = escape_latex_filename(filename)

                # Create a figure environment for each image and its caption
                f.write("\\begin{figure}[H]\n")
                f.write("\\centering\n")
                f.write(f"\\includegraphics[width={img['width']}in,height={img['height']}in]{{{filename}}}\n")
                f.write(f"\\caption*{{\\texttt{{\\small {escaped_filename}}}}}\n")
                f.write("\\end{figure}\n\n")

            f.write("\\end{center}\n")
            f.write("\\clearpage\n\n")

        f.write("\\end{document}\n")

    return output_file


def compile_latex_to_pdf(tex_file):
    """Compile LaTeX file to PDF using pdflatex."""
    try:
        # Run pdflatex twice
        for _ in range(2):
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode',
                 '-output-directory', os.path.dirname(tex_file), tex_file],
                capture_output=True, text=True)

            if result.returncode != 0:
                print("LaTeX compilation failed. Error output:")
                print(result.stderr)
                print("\nStandard output:")
                print(result.stdout)
                return False
        return True
    except FileNotFoundError:
        print("Error: pdflatex not found. Please install texlive-latex-base")
        return False


def main():
    parser = argparse.ArgumentParser(description='Create a LaTeX picture book from images')
    parser.add_argument('--image-directory', required=True, help='Directory containing images')
    parser.add_argument('--output-directory', required=True, help='Output directory for LaTeX and PDF files')
    parser.add_argument('--document-name', required=True, help='Name of the output document (without extension)')
    parser.add_argument('--no-pdf', action='store_true', help='Skip PDF generation')
    parser.add_argument('--page-size', default='letter',
                        choices=['letter', 'a4', 'legal'],
                        help='Page size (default: letter)')
    parser.add_argument('--orientation', default='portrait',
                        choices=['portrait', 'landscape'],
                        help='Page orientation (default: portrait)')
    parser.add_argument('--image-scaling-factor', type=float, default=0.50,
                        help='Scale factor for images (default: 0.50, range: 0.1-1.0)')

    args = parser.parse_args()

    # Validate scaling factor
    if args.image_scaling_factor < 0.1 or args.image_scaling_factor > 1.0:
        print("Warning: Scaling factor should be between 0.1 and 1.0. Using default value of 0.50")
        args.image_scaling_factor = 0.50

    tex_file = create_latex_picture_book(
        args.image_directory,
        args.output_directory,
        args.document_name,
        args.page_size,
        args.orientation,
        args.image_scaling_factor
    )

    if not args.no_pdf:
        if compile_latex_to_pdf(tex_file):
            print(f"Successfully created PDF: {os.path.splitext(tex_file)[0]}.pdf")
        else:
            print("Failed to create PDF")


if __name__ == "__main__":
    main()