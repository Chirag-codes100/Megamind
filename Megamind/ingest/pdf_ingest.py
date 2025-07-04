import pdfplumber

def extract_pdf_text_by_page(pdf_path):
    """
    Returns a dict {page_number: text} for the given PDF.
    """
    pdf_text = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            pdf_text[i] = text
    return pdf_text

if __name__ == "__main__":
    # Quick test
    path = input("Enter path to PDF: ")
    pages = extract_pdf_text_by_page(path)
    for pg, txt in pages.items():
        print(f"\n--- Page {pg} ---\n{txt[:500]}")  # Print first 500 chars per page
