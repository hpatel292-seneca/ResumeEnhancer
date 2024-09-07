import os
from docx import Document
from PyPDF2 import PdfReader

def read_txt_file(file_path):
    with open(file_path, 'r',encoding='utf-8') as f:
        content=f.read()
    return content

def read_pdf_file(file_path):
    content=""
    with open(file_path, "rb") as f:
        reader=PdfReader(f)
        for page in range(len(reader.pages)):
            content+=reader.pages[page].extract_text()
    return content

def read_word_file(file_path):
    doc=Document(file_path)
    content="\n".join([para.text for para in doc.paragraphs])
    return content

def read_file(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension=='.txt':
        return read_txt_file(file_path)
    elif extension=='.pdf':
        return read_pdf_file(file_path)
    elif extension in ['.doc', '.docx']:
        return read_word_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {extension}")