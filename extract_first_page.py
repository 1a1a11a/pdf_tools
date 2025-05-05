#!/usr/bin/env python3

"""
Script to extract the first page from each PDF in a list and save them all to a single PDF.

Usage:
    python extract_first_page.py -o output.pdf input1.pdf input2.pdf input3.pdf ...
    python extract_first_page.py -o output.pdf folder_path
"""

import os
import sys
import argparse
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path


def extract_first_page(input_pdf_path, verbose=False):
    """
    Extract the first page from a PDF file.

    Args:
        input_pdf_path (str): Path to the input PDF file

    Returns:
        page: The first page object from the PDF, or None if there was an error
    """
    try:
        # Open the input PDF file
        reader = PdfReader(input_pdf_path)

        # Check if the PDF has at least one page
        if len(reader.pages) < 1:
            print(f"Error: {input_pdf_path} has no pages.")
            return None

        # Return the first page
        if verbose:
            print(f"Extracted first page from {input_pdf_path}")
        return reader.pages[0]

    except Exception as e:
        print(f"Error processing {input_pdf_path}: {str(e)}")
        return None


def get_pdf_files_from_directory(directory_path, verbose=False):
    """
    Find all PDF files in the given directory.

    Args:
        directory_path (str): Path to the directory

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


def parse_arguments():
    """
    Parse command line arguments using argparse.

    Returns:
        argparse.Namespace: The parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Extract the first page from each PDF and combine them into a single PDF.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("-o", "--output", required=True, help="Output PDF file path")

    parser.add_argument(
        "inputs", nargs="+", help="Input PDF files or directories containing PDFs"
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    return parser.parse_args()


def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Get output path and input paths
    output_pdf_path = args.output
    input_paths = args.inputs
    verbose = args.verbose

    # Create a PDF writer object for the combined output
    writer = PdfWriter()
    successful_files = 0
    total_files_to_process = 0

    # Process each input path from command line arguments
    pdf_files = []
    for input_path in input_paths:
        if not os.path.exists(input_path):
            print(f"Error: Path {input_path} does not exist.")
            continue

        if os.path.isdir(input_path):
            # If input is a directory, find all PDF files in it
            dir_pdf_files = get_pdf_files_from_directory(input_path, verbose)
            pdf_files.extend(dir_pdf_files)
        elif input_path.lower().endswith(".pdf"):
            # If input is a PDF file
            pdf_files.append(input_path)
        else:
            print(f"Error: {input_path} is not a PDF file or directory.")

    total_files_to_process = len(pdf_files)
    if total_files_to_process == 0:
        print("No valid PDF files to process.")
        sys.exit(1)

    # Process each PDF file
    for pdf_file in pdf_files:
        # Extract the first page
        first_page = extract_first_page(pdf_file, verbose)
        if first_page:
            # Add the first page to the writer
            writer.add_page(first_page)
            successful_files += 1

    # Write all first pages to the output file
    if successful_files > 0:
        with open(output_pdf_path, "wb") as output_file:
            writer.write(output_file)
        print(f"\nAll first pages saved to {output_pdf_path}")
    else:
        print("\nNo pages were processed successfully.")
        sys.exit(1)

    # Print summary
    print(
        f"Processed {successful_files} out of {total_files_to_process} PDF files successfully."
    )


if __name__ == "__main__":
    main()
