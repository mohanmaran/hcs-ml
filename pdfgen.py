from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import random

def generate_sample_medical_report(name, age, no_of_pregnancies, bp, glucose, insulin, bmi):
    # Create a PDF document
    c = canvas.Canvas("sample_medical_report.pdf", pagesize=letter)

    # Set font styles
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, 10.5 * inch, "Medical Report")

    # Add a line separator
    c.setStrokeColorRGB(0, 0, 0)
    c.line(1 * inch, 10.25 * inch, 7.5 * inch, 10.25 * inch)

    # Add patient details
    c.setFont("Helvetica", 12)
    details = [
        ("Name:", name),
        ("Age:", str(age)),
        ("No. of Pregnancies:", str(no_of_pregnancies)),
        ("Blood Pressure:", str(bp)),
        ("Glucose Level:", str(glucose)),
        ("Insulin Level:", str(insulin)),
        ("BMI:", str(bmi))
    ]
    y_position = 9.5 * inch
    for label, value in details:
        c.drawString(1 * inch, y_position, label)
        c.drawString(2.5 * inch, y_position, value)
        y_position -= 0.35 * inch

    # Add a line separator
    c.line(1 * inch, 6.5 * inch, 7.5 * inch, 6.5 * inch)

    # Add a random diagnosis
    diagnoses = ["Normal", "High Blood Pressure", "High Glucose", "High Insulin", "High BMI"]
    random_diagnosis = random.choice(diagnoses)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, 6.2 * inch, "Diagnosis:")
    c.setFont("Helvetica", 12)
    c.drawString(1.5 * inch, 5.8 * inch, random_diagnosis)

    # Save the PDF document
    c.save()

if __name__ == "__main__":
    # Replace the following values with the desired sample data
    name = "Jane Doe"
    age = 35
    no_of_pregnancies = 2
    bp = 120  # Change the value to 120 as an integer
    glucose = 95.0
    insulin = 18.5
    bmi = 26.7

    generate_sample_medical_report(name, age, no_of_pregnancies, bp, glucose, insulin, bmi)
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import random

def generate_sample_medical_report(name, age, no_of_pregnancies, bp, glucose, insulin, bmi):
    # Create a PDF document
    c = canvas.Canvas("sample_medical_report.pdf", pagesize=letter)

    # Set font styles
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, 10.5 * inch, "Medical Report")

    # Add a line separator
    c.setStrokeColorRGB(0, 0, 0)
    c.line(1 * inch, 10.25 * inch, 7.5 * inch, 10.25 * inch)

    # Add patient details
    c.setFont("Helvetica", 12)
    details = [
        ("Name:", name),
        ("Age:", str(age)),
        ("No. of Pregnancies:", str(no_of_pregnancies)),
        ("Blood Pressure:", str(bp)),
        ("Glucose Level:", str(glucose)),
        ("Insulin Level:", str(insulin)),
        ("BMI:", str(bmi))
    ]
    y_position = 9.5 * inch
    for label, value in details:
        c.drawString(1 * inch, y_position, label)
        c.drawString(2.5 * inch, y_position, value)
        y_position -= 0.35 * inch

    # Add a line separator
    c.line(1 * inch, 6.5 * inch, 7.5 * inch, 6.5 * inch)

    # Add a random diagnosis
    diagnoses = ["Normal", "High Blood Pressure", "High Glucose", "High Insulin", "High BMI"]
    random_diagnosis = random.choice(diagnoses)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, 6.2 * inch, "Diagnosis:")
    c.setFont("Helvetica", 12)
    c.drawString(1.5 * inch, 5.8 * inch, random_diagnosis)

    # Save the PDF document
    c.save()

if __name__ == "__main__":
    # Replace the following values with the desired sample data
    name = "Jane Doe"
    age = 35
    no_of_pregnancies = 2
    bp = 120  # Change the value to 120 as an integer
    glucose = 95.0
    insulin = 18.5
    bmi = 26.7

    generate_sample_medical_report(name, age, no_of_pregnancies, bp, glucose, insulin, bmi)
