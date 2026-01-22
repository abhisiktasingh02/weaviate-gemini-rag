from pypdf import PdfReader

def extract_text(pdf_path):
    reader=PdfReader(pdf_path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        pages.append({
            "page": i + 1,
            "text": text
        })
    return pages