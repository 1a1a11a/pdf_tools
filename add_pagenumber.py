#!/usr/bin/env python3

"""
Script to add page numbers to PDF files.

Usage:
    python add_pagenumber.py -i input.pdf -o output.pdf
    python add_pagenumber.py -i input_directory -o output_directory
"""

import fitz  # PyMuPDF
import os
import argparse
import subprocess
from pathlib import Path


def get_pdf_files_from_directory(directory_path, verbose=False):
    """
    Find all PDF files in the given directory.

    Args:
        directory_path (str): Path to the directory
        verbose (bool): Whether to print verbose output

    Returns:
        list: List of paths to PDF files
    """
    pdf_files = []
    try:
        directory = Path(directory_path)
        if not directory.is_dir():
            print(f"Error: {directory_path} is not a directory.")
            return pdf_files

        # Get all pdf files in the directory
        for file_path in directory.glob("*.pdf"):
            pdf_files.append(str(file_path))

        if not pdf_files:
            print(f"No PDF files found in {directory_path}")
        elif verbose:
            print(f"Found {len(pdf_files)} PDF files in {directory_path}")

        return pdf_files
    except Exception as e:
        print(f"Error reading directory {directory_path}: {str(e)}")
        return pdf_files


def add_page_numbers(
    input_pdf,
    output_pdf,
    position="bottom",
    fontname="helv",
    fontsize=12,
    verbose=False,
):
    """
    Add page numbers to a PDF file.

    Args:
        input_pdf (str): Path to the input PDF file
        output_pdf (str): Path to save the output PDF file
        position (str): Position of the page number: 'bottom', 'top', 'bottomright', 'bottomleft', 'topright', 'topleft'
        fontname (str): Font name to use
        fontsize (int): Font size in points
        verbose (bool): Whether to print verbose output

    Returns:
        bool: True if successful, False otherwise
    """
    # Open the PDF file
    try:
        doc = fitz.open(input_pdf)
        if verbose:
            print(f"Processing {doc.page_count} pages in {input_pdf}...")

        for page_num in range(doc.page_count):
            page = doc[page_num]

            # Get page dimensions
            width, height = page.rect.width, page.rect.height
            if verbose:
                print(f"Page {page_num + 1} dimensions: {width} x {height}")

            # Calculate text and position
            text = str(page_num + 1)
            tw = fitz.get_text_length(text, fontname=fontname, fontsize=fontsize)

            # Determine position based on the 'position' parameter
            margin = 20  # margin from the edge

            if position == "bottom":
                # Cover the entire bottom area of the page with white
                rect = fitz.Rect(0, height - 50, width, height)
                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                text_point = fitz.Point(width / 2 - tw / 2, height - margin)
            elif position == "top":
                rect = fitz.Rect(0, 0, width, 50)
                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                text_point = fitz.Point(width / 2 - tw / 2, margin + fontsize / 2)
            elif position == "bottomright":
                rect = fitz.Rect(width - 100, height - 50, width, height)
                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                text_point = fitz.Point(width - margin - tw, height - margin)
            elif position == "bottomleft":
                rect = fitz.Rect(0, height - 50, 100, height)
                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                text_point = fitz.Point(margin, height - margin)
            elif position == "topright":
                rect = fitz.Rect(width - 100, 0, width, 50)
                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                text_point = fitz.Point(width - margin - tw, margin + fontsize / 2)
            elif position == "topleft":
                rect = fitz.Rect(0, 0, 100, 50)
                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                text_point = fitz.Point(margin, margin + fontsize / 2)
            else:  # Default to bottom if invalid position
                rect = fitz.Rect(0, height - 50, width, height)
                page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                text_point = fitz.Point(width / 2 - tw / 2, height - margin)

            # Insert the text
            page.insert_text(
                text_point,  # position
                text,  # page number
                fontname=fontname,  # font
                fontsize=fontsize,  # font size
            )

        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_pdf)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the modified PDF
        doc.save(output_pdf)
        if verbose:
            print(f"Saved to {output_pdf}")
        return True

    except Exception as e:
        print(f"Error processing {input_pdf}: {e}")
        return False


def process_pdf(
    input_path, output_path, position, fontname, fontsize, verbose, open_output
):
    """
    Process a single PDF file or directory of PDF files.

    Args:
        input_path (str): Path to the input PDF file or directory
        output_path (str): Path to save the output PDF file or directory
        position (str): Position of the page number
        fontname (str): Font name to use
        fontsize (int): Font size in points
        verbose (bool): Whether to print verbose output
        open_output (bool): Whether to open the output file when done

    Returns:
        int: Number of successfully processed files
    """
    # Check if input path exists
    if not os.path.exists(input_path):
        print(f"Error: Input path {input_path} does not exist.")
        return 0

    # Process a directory of PDFs
    if os.path.isdir(input_path):
        if not os.path.isdir(output_path) and output_path.lower().endswith(".pdf"):
            print(
                f"Error: When input is a directory, output must also be a directory, not a PDF file."
            )
            return 0

        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Get all PDF files in the directory
        pdf_files = get_pdf_files_from_directory(input_path, verbose)
        if not pdf_files:
            return 0

        # Process each PDF file
        successful_files = 0
        for pdf_file in pdf_files:
            # Create output path
            rel_path = os.path.relpath(pdf_file, input_path)
            new_output_path = os.path.join(output_path, rel_path)

            # Process the PDF
            if add_page_numbers(
                pdf_file, new_output_path, position, fontname, fontsize, verbose
            ):
                successful_files += 1
                if open_output:
                    subprocess.call(["open", new_output_path])

        return successful_files

    # Process a single PDF file
    elif input_path.lower().endswith(".pdf"):
        if os.path.isdir(output_path):
            # If output is a directory, use the input filename inside that directory
            output_file = os.path.join(output_path, os.path.basename(input_path))
        else:
            output_file = output_path

        if add_page_numbers(
            input_path, output_file, position, fontname, fontsize, verbose
        ):
            if open_output:
                subprocess.call(["open", output_file])
            return 1

    else:
        print(f"Error: {input_path} is not a PDF file or directory.")

    return 0


def parse_arguments():
    """
    Parse command line arguments using argparse.

    Returns:
        argparse.Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Add page numbers to PDF files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-i", "--input", required=True, help="Input PDF file or directory"
    )

    parser.add_argument(
        "-o", "--output", required=True, help="Output PDF file or directory"
    )

    parser.add_argument(
        "-p",
        "--position",
        choices=["bottom", "top", "bottomright", "bottomleft", "topright", "topleft"],
        default="bottom",
        help="Position of the page numbers",
    )

    parser.add_argument(
        "-f", "--font", default="helv", help="Font to use for page numbers"
    )

    parser.add_argument(
        "-s", "--size", type=int, default=12, help="Font size in points"
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    parser.add_argument(
        "--open", action="store_true", help="Open the output PDF file(s) when done"
    )

    return parser.parse_args()


def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Process the input files
    print(f"Adding page numbers to {args.input}...")
    successful_files = process_pdf(
        args.input,
        args.output,
        args.position,
        args.font,
        args.size,
        args.verbose,
        args.open,
    )

    # Print summary
    if successful_files > 0:
        print(f"\nSuccessfully added page numbers to {successful_files} PDF file(s).")
    else:
        print("\nFailed to process any PDF files.")
        print("Make sure you have PyMuPDF installed. Run: pip install pymupdf")


if __name__ == "__main__":
    main()
