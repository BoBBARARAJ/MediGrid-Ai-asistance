from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

 
def create_pdf_report(data, filename="prescription_report.pdf"):

    pdf = canvas.Canvas(filename, pagesize=A4)

    y = 800

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "MediGrid AI Prescription Report")

    y -= 40

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50, y,
        f"Patient: {data.get('patient_name', 'Not available')}"
    )

    y -= 25

    pdf.drawString(
        50, y,
        f"Doctor: {data.get('doctor_name', 'Not available')}"
    )

    y -= 40

    for medicine in data.get("medicines", []):

        pdf.drawString(
            50, y,
            f"Medicine: {medicine.get('name', 'Not available')}"
        )
        y -= 20

        pdf.drawString(
            50, y,
            f"Dosage: {medicine.get('dosage', 'Not available')}"
        )
        y -= 20

        pdf.drawString(
            50, y,
            f"Frequency: {medicine.get('frequency', 'Not available')}"
        )
        y -= 20

        pdf.drawString(
            50, y,
            f"Duration: {medicine.get('duration', 'Not available')}"
        )
        y -= 30

    pdf.save()

    return os.path.abspath(filename)