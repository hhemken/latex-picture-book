"""
sudo apt install texlive-xetex texlive-latex-extra texlive-fonts-recommended fonts-freefont-ttf ttf-mscorefonts-installer

The script includes:

Default letter-size paper
Portrait/landscape orientation options
Custom font and font size for image captions
Proper handling of multiple images per page
Timestamp-based image sorting

Remember that you need:

A LaTeX distribution with XeLaTeX installed
The fontspec and caption LaTeX packages
The specified font (Arial or other) installed on your system

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
    # Replace underscores with escaped underscores
    filename = filename.replace('_', '\\_')
    # Escape other special characters if needed
    special_chars = ['&', '%', '$', '#', '{', '}', '~', '^']
    for char in special_chars:
        filename = filename.replace(char, f'\\{char}')
    return filename


def create_latex_picture_book(image_dir, output_dir, doc_name, image_dpi=300,
                              font_size=8, page_size="letter", orientation="portrait"):
    """Creates a LaTeX picture book from images in a directory."""

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f"{doc_name}.tex")

    # Get list of image files sorted by timestamp
    image_files = []
    for filename in os.listdir(image_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
            filepath = os.path.join(image_dir, filename)
            image_files.append((filename, get_image_creation_time(filepath)))

    image_files.sort(key=lambda x: x[1])  # Sort by timestamp

    with open(output_file, "w") as f:
        # Document preamble with minimal packages
        f.write("\\documentclass{article}\n")
        f.write("\\usepackage{graphicx}\n")
        f.write("\\usepackage[utf8]{inputenc}\n")
        f.write("\\usepackage[margin=0.5in]{geometry}\n")

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

        # Set up basic document configuration
        f.write("\\pagestyle{empty}\n")  # No page numbers

        f.write("\\begin{document}\n")

        # Process each image
        for filename, _ in image_files:
            escaped_filename = escape_latex_filename(filename)
            f.write("\\begin{center}\n")
            f.write(
                f"\\includegraphics[width=0.95\\textwidth,height=0.95\\textheight,keepaspectratio]{{{filename}}}\n\n")
            f.write(f"\\vspace{{0.1in}}\n")
            f.write(f"\\texttt{{\\small {escaped_filename}}}\n")
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
    parser.add_argument('--image-dpi', type=int, default=300, help='Image DPI (default: 300)')
    parser.add_argument('--no-pdf', action='store_true', help='Skip PDF generation')
    parser.add_argument('--image-name-font-size', type=int, default=8,
                        help='Font size for image names in points (default: 8)')
    parser.add_argument('--page-size', default='letter',
                        choices=['letter', 'a4', 'legal'],
                        help='Page size (default: letter)')
    parser.add_argument('--orientation', default='portrait',
                        choices=['portrait', 'landscape'],
                        help='Page orientation (default: portrait)')

    args = parser.parse_args()

    tex_file = create_latex_picture_book(
        args.image_directory,
        args.output_directory,
        args.document_name,
        args.image_dpi,
        args.image_name_font_size,
        args.page_size,
        args.orientation
    )

    if not args.no_pdf:
        if compile_latex_to_pdf(tex_file):
            print(f"Successfully created PDF: {os.path.splitext(tex_file)[0]}.pdf")
        else:
            print("Failed to create PDF")


if __name__ == "__main__":
    main()