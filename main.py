import argparse
from converter import md_to_pdf

def main():
    parser = argparse.ArgumentParser(description="Converts Markdown or Text files to PDF")
    parser.add_argument("input", help="Input file (.md or .txt)")
    parser.add_argument("--output", help="Output PDF file", default="output.pdf")
    parser.add_argument("--font", help="Custom font for the PDF", default="Helvetica")
    parser.add_argument("--page-size", help="Page size for the PDF", default="letter")
    args = parser.parse_args()

    page_size = getattr(__import__('reportlab.lib.pagesizes', fromlist=[args.page_size]), args.page_size)
    md_to_pdf(args.input, args.output, font=args.font, page_size=page_size)

if __name__ == "__main__":
    main()