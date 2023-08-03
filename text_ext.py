import pdfplumber
import re
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]  
        text = page.extract_text()
        return text

pdf_path = 'sample_medical_report.pdf'
extracted_text = extract_text_from_pdf(pdf_path)



def parse_medical_report(text):
    name_match = re.search(r'Name:\s*(\w+\s*\w+)', text)
    name = name_match.group(1) if name_match else "N/A"

    age_match = re.search(r'Age:\s*(\d+)', text)
    age = int(age_match.group(1)) if age_match else 0

    bp_matches = re.findall(r'Blood Pressure:\s*(\d+/\d+)', text)
    bp = "/".join(bp_matches) if bp_matches else "N/A"

    glucose_match = re.search(r'Glucose Level:\s*(\d+\.\d+)', text)
    glucose_level = float(glucose_match.group(1)) if glucose_match else 0.0

    cholesterol_match = re.search(r'Cholesterol Level:\s*(\d+\.\d+)', text)
    cholesterol_level = float(cholesterol_match.group(1)) if cholesterol_match else 0.0

    bmi_match = re.search(r'BMI:\s*(\d+\.\d+)', text)
    bmi = float(bmi_match.group(1)) if bmi_match else 0.0

    return name, age, bp, glucose_level, cholesterol_level, bmi

name, age, bp, glucose_level, cholesterol_level, bmi = parse_medical_report(extracted_text)
print(name)
print(age)
print(bp)
print(glucose_level)
print(cholesterol_level)
