import pdfplumber


def extract_text_from_pdf(pdf_file):
    pages = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                pages.append(page_text.strip())

    return "\n\n".join(pages)
