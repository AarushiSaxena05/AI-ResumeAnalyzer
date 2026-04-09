import pdfplumber
import docx


def extract_text(file_path):
    try:
        if file_path.endswith(".pdf"):
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text.strip()

        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs]).strip()

    except Exception as e:
        print("Parser Error:", e)

    return ""