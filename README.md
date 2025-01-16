# LaTeX Picture Book Generator

A Python script that creates PDF photo books from a directory of images using LaTeX. The script intelligently arranges images, preserves their aspect ratios, and can fit multiple images per page when space allows.

## Features

- Creates PDF photo books from image directories
- Supports JPG, JPEG, PNG, and BMP formats
- Maintains image aspect ratios
- Intelligently arranges multiple images per page when possible
- Preserves image filenames as captions
- Sorts images by creation timestamp
- Supports multiple page sizes (letter, A4, legal)
- Supports both portrait and landscape orientations
- Configurable image scaling

## Prerequisites

1. Python 3.6 or higher
2. LaTeX distribution (texlive-latex-base)
3. Required LaTeX packages:
   - texlive-xetex
   - texlive-latex-extra
   - texlive-fonts-recommended
   - fonts-freefont-ttf
   - ttf-mscorefonts-installer

## Installation

1. Install the required LaTeX packages:
```bash
sudo apt install texlive-xetex texlive-latex-extra texlive-fonts-recommended fonts-freefont-ttf ttf-mscorefonts-installer
```

2. Install Python dependencies:
```bash
pip install Pillow
```

3. Clone or download this repository.

## Usage

Basic usage:
```bash
python3 latex-picture-book.py \
    --image-directory /path/to/images/ \
    --output-directory /path/to/output/ \
    --document-name photobook
```

All available options:
```bash
python3 latex-picture-book.py \
    --image-directory /path/to/images/ \
    --output-directory /path/to/output/ \
    --document-name photobook \
    --page-size letter \
    --orientation landscape \
    --image-scaling-factor 0.50 \
    --no-pdf
```

### Command Line Arguments

- `--image-directory`: Directory containing the images (required)
- `--output-directory`: Directory for output files (required)
- `--document-name`: Name of the output document without extension (required)
- `--page-size`: Page size (choices: letter, a4, legal; default: letter)
- `--orientation`: Page orientation (choices: portrait, landscape; default: portrait)
- `--image-scaling-factor`: Scale factor for images (default: 0.50, range: 0.1-1.0)
- `--no-pdf`: Skip PDF generation and only create LaTeX file (optional)

## Output

The script generates two main files in the output directory:
1. A `.tex` file containing the LaTeX source
2. A `.pdf` file containing the final photo book (unless `--no-pdf` is specified)

## Image Handling

- Images are displayed at their natural size multiplied by the scaling factor
- Large images are automatically scaled down to fit the page
- Multiple small images are arranged on the same page when possible
- Images maintain their aspect ratios
- A 0.5-inch margin is maintained on all sides
- Images are centered on the page
- Filenames are displayed as captions below each image

## Example

Create a landscape letter-sized photo book with images scaled to 50%:
```bash
python3 latex-picture-book.py \
    --image-directory ~/Pictures/vacation/ \
    --output-directory ~/Documents/photobooks/ \
    --document-name vacation-2024 \
    --page-size letter \
    --orientation landscape \
    --image-scaling-factor 0.50
```

## Troubleshooting

1. If you get a "pdflatex not found" error:
   - Ensure you have installed the required LaTeX packages
   - Try running `sudo apt install texlive-latex-base`

2. If images are too large or small:
   - Adjust the `--image-scaling-factor` value
   - Use a smaller value (e.g., 0.25) to fit more images per page
   - Use a larger value (e.g., 0.75) for higher quality single images

## License

This project is licensed under the MIT License - see the LICENSE file for details.