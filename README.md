sudo apt install texlive-xetex texlive-latex-extra texlive-fonts-recommended fonts-freefont-ttf ttf-mscorefonts-installer

The script includes:

Default letter-size paper
Portrait/landscape orientation options
Custom font and font size for image captions
Proper handling of multiple images per page
Timestamp-based image sorting

python latex-picture-book.py --image-directory ./images --output-directory ./output \
    --document-name photobook --page-size legal --orientation landscape
