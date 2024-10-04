import os
import re
import PyPDF2
import docx
from datetime import datetime

def extract_text_from_pdf(pdf_path):
  try:
    with open(pdf_path, 'rb') as pdf_file:
      pdf_reader = PyPDF2.PdfReader(pdf_file)
      text = ""
      for page in pdf_reader.pages:
        text += page.extract_text()
    return text
  except Exception as e:
      print(f"Error extracting text from {pdf_path}: {e}")
      return None
  
def extract_text_from_docx(docx_path):
  try:
    doc = docx.Document(docx_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])
  except Exception as e:
    print(f"Error extracting text from {docx_path}: {e}")
    return None
  
def extract_name_and_job_title(text):
  # Attempt to find a name
  name_pattern = re.compile(r"(Name:\s*)([A-Za-z]+\s[A-Za-z]+)")
  name_match = name_pattern.search(text)
  name = name_match.group(2) if name_match else "UnknownName"

  # Attempt to find a job title or experience level
  title_pattern = re.compile(r"(Title:\s*)([A-Za-z\s]+)")
  title_match = title_pattern.search(text)
  job_title = title_match.group(2).replace(" ", "_") if title_match else "UnknownTitle"

  return name, job_title

def rename_files_in_directory(input_dir):
  for filename in os.listdir(input_dir):
    file_path = os.path.join(input_dir, filename)
    if filename.endswith(".pdf"):
      text = extract_text_from_pdf(file_path)
    elif filename.endswith(".docx"):
      text = extract_text_from_docx(file_path)
    else:
      continue # Skip non-PDF/DOCX files

    if text:
      name, job_title = extract_name_and_job_title(text)
      # Create a new filename based on extracted content
      timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
      new_filename = f"{name}_{job_title}_{timestamp}.pdf" if filename.endswith(".pdf") else f"{name}_{job_title}_{timestamp}.docx"
      new_file_path = os.path.join(input_dir, new_filename)

      os.rename(file_path, new_file_path)
      print(f"Renamed {file_path} to {new_file_path}")

# Example usage
input_directory = "resumes/" # Directory containing PDF and DOCX files
rename_files_in_directory(input_directory)