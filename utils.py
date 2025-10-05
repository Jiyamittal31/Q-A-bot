import PyPDF2, docx

def load_pdf(filepath):
    text = ""
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + " "
    return text

def load_docx(filepath):
    doc = docx.Document(filepath)
    return " ".join([para.text for para in doc.paragraphs])

def load_txt(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def load_file(file):
    if file.name.endswith(".pdf"):
        return load_pdf(file)
    elif file.name.endswith(".docx"):
        return load_docx(file)
    elif file.name.endswith(".txt"):
        return load_txt(file)
    else:
        return ""
