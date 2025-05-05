#!/usr/bin/env python3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os


def create_test_pdf(filename, num_pages, page_content):
    """Create a test PDF with specified content on each page."""
    c = canvas.Canvas(filename, pagesize=letter)

    for page_num in range(1, num_pages + 1):
        c.drawString(100, 750, f"This is page {page_num} of {filename}")
        c.drawString(100, 700, page_content)
        c.showPage()

    c.save()
    print(f"Created test PDF: {filename}")


def main():
    # Create test directory if it doesn't exist
    test_dir = "test_pdfs"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # Create 3 different test PDFs in the test directory
    create_test_pdf(
        os.path.join(test_dir, "document1.pdf"),
        3,
        "First page should be extracted from document1",
    )

    create_test_pdf(
        os.path.join(test_dir, "document2.pdf"),
        2,
        "First page should be extracted from document2",
    )

    create_test_pdf(
        os.path.join(test_dir, "document3.pdf"),
        4,
        "First page should be extracted from document3",
    )

    print(f"Created 3 test PDFs in {test_dir} directory")


if __name__ == "__main__":
    main()
