# document_extractor.py
from docx import Document
import PyPDF2

def extract_text_from_docx(docx_path):
    try:
        # print('DOC PATH: ', docx_path)
        doc = Document(docx_path)
        # print('DOC: ', doc)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except FileNotFoundError:
        print(f"Error: File not found at {docx_path}")
        return None  # Return None to indicate failure
    except Exception as e: # Catch other potential errors
        print(f"Error processing docx file: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    except FileNotFoundError:
        print(f"Error: File not found at {pdf_path}")
        return None
    except PyPDF2.errors.PdfReadError:
        print(f"Error: Could not read pdf file at {pdf_path}. Is it a valid PDF?")
        return None
    except Exception as e:
        print(f"Error processing pdf file: {e}")
        return None