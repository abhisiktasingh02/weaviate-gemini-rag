import pdfplumber
def extract_tables(pdf_path):
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for pageno, page in enumerate(pdf.pages):
            for table in page.extract_tables():
                tables.append({
                    "page": pageno + 1,
                    "table": table
                })
    return tables