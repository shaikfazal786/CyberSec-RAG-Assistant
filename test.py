# test_pdf.py

from pypdf import PdfReader

reader = PdfReader(
    "data/cyber.pdf"
)

print(
    reader.pages[0].extract_text()
)