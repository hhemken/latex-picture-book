# LaTeX Picture Book Generator

A Python script that creates a PDF photo album from a directory of images. The script automatically scales images to fit two per page while preserving aspect ratios, and sorts them by creation date.

## Features

- Creates a professional-looking photo album with two images per page
- Automatically scales large images to fit the page while maintaining aspect ratios
- Sorts images by creation date
- Supports multiple page sizes (Letter, A4, Legal) and orientations (Portrait, Landscape)
- Handles special characters in filenames
- Displays image filenames below each image
- Supports JPG, JPEG, PNG, and BMP formats

## Prerequisites

1. Python 3.6 or higher
2. LaTeX distribution (e.g., TexLive or MiKTeX) with pdflatex installed
3. Required Python packages:
   ```bash
   pip install Pillow
   ```

## Installation

1. Clone this repository or download the script
2. Install the required Python package:
   ```bash
   pip install Pillow
   ```
3. Ensure you have a LaTeX distribution installed:
   - For Ubuntu/Debian:
     ```bash
     sudo apt-get install texlive-latex-base
     ```
   - For macOS (using Homebrew):
     ```bash
     brew install --cask mactex
     ```
   - For Windows: Download and install MiKTeX from https://miktex.org/

## Usage

Basic usage:
```bash
python picture_book.py --image-directory /path/to/images --output-directory /path/to/output --document-name album
```

Full options:
```bash
python picture_book.py \
  --image-directory /path/to/images \
  --output-directory /path/to/output \
  --document-name album \
  --image-dpi 300 \
  --image-name-font-size 8 \
  --page-size letter \
  --orientation portrait \
  --no-pdf
```

### Command Line Arguments

- `--image-directory`: Directory containing the images (required)
- `--output-directory`: Directory where the LaTeX file and PDF will be saved (required)
- `--document-name`: Name of the output document without extension (required)
- `--image-dpi`: Image resolution in DPI (default: 300)
- `--image-name-font-size`: Font size for image names in points (default: 8)
- `--page-size`: Page size - choices: letter, a4, legal (default: letter)
- `--orientation`: Page orientation - choices: portrait, landscape (default: portrait)
- `--no-pdf`: Skip PDF generation, only create LaTeX file (optional)

## Output

The script generates:
1. A LaTeX (.tex) file in the specified output directory
2. A PDF file (unless --no-pdf is specified) containing the photo album

## Example

To create a landscape-oriented A4 photo album:
```bash
python picture_book.py \
  --image-directory ~/Pictures/vacation \
  --output-directory ~/Documents/albums \
  --document-name vacation_album \
  --page-size a4 \
  --orientation landscape
```

## Troubleshooting

1. If you get a "pdflatex not found" error:
   - Ensure LaTeX is installed
   - Make sure pdflatex is in your system PATH
   - Try running `pdflatex --version` to verify the installation

2. If images don't appear in the PDF:
   - Check if the image files are readable
   - Verify the image formats are supported (JPG, JPEG, PNG, BMP)
   - Ensure the image directory path is correct and accessible

3. If the script fails to create the PDF:
   - Check the LaTeX compilation output for errors
   - Verify you have write permissions in the output directory
   - Make sure the image filenames don't contain unsupported special characters

## Limitations

- Only supports JPG, JPEG, PNG, and BMP image formats
- Requires a LaTeX distribution to be installed
- Images are scaled to fit two per page, which may make very wide images appear small
- All pages will attempt to show two images (except possibly the last page if there's an odd number of images)

## License

This project is licensed under the MIT License - see the LICENSE file for details.