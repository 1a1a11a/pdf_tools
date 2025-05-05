# PDF Tools

A collection of command-line tools for working with PDF files.

## Features

### Extract First Page
Extract the first page from multiple PDF files and combine them into a single PDF.

### Add Page Numbers
Add customizable page numbers to PDF files with different positioning options.

## Installation

### Requirements
- Python 3.6 or higher
- PyMuPDF
- PyPDF2
- reportlab (for test PDF generation)

### Setup
```bash
# Clone the repository
git clone https://github.com/1a1a11a/pdf_tools.git
cd pdf_tools

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Extract First Page

This tool extracts the first page from each input PDF file and combines them into a single output PDF.

```bash
python extract_first_page.py -o output.pdf input1.pdf input2.pdf input3.pdf
```

You can also use a directory containing PDF files:

```bash
python extract_first_page.py -o output.pdf path/to/pdf/directory
```

Options:
- `-o, --output`: Output PDF file path (required)
- `inputs`: One or more input PDF files or directories (required)
- `-v, --verbose`: Enable verbose output

### Add Page Numbers

This tool adds page numbers to one or more PDF files.

```bash
python add_pagenumber.py -i input.pdf -o output.pdf
```

You can also process an entire directory:

```bash
python add_pagenumber.py -i input_directory -o output_directory
```

Options:
- `-i, --input`: Input PDF file or directory (required)
- `-o, --output`: Output PDF file or directory (required)
- `-p, --position`: Position of page numbers (choices: bottom, top, bottomright, bottomleft, topright, topleft; default: bottom)
- `-f, --font`: Font to use for page numbers (default: helv)
- `-s, --size`: Font size in points (default: 12)
- `-v, --verbose`: Enable verbose output
- `--open`: Open the output PDF file(s) when done

## Examples

Extract first pages from a directory:
```bash
python extract_first_page.py -o combined_first_pages.pdf -v ~/Documents/PDFs/
```

Add page numbers to bottom right of PDFs:
```bash
python add_pagenumber.py -i ~/Reports/ -o ~/Reports/Numbered/ -p bottomright -s 10 -v
```

## License

MIT License

## Author

Created by Juncheng
