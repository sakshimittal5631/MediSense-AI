import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(predicted_disease, dis_des, my_precautions, medications, my_diet, workout, symptoms, doctors_list):
    pdf_path = "report.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=60, bottomMargin=18
    )
    styles = getSampleStyleSheet()
    styleTitle = styles['Title']
    styleHeading = styles['Heading2']
    styleNormal = styles['Normal']
    elements = []

    logo_path = "static/favicon.png"
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=50, height=50)
        elements.append(logo)
        elements.append(Spacer(1, 12))

    elements.append(Paragraph("MediSense AI - Health Report", styleTitle))
    elements.append(Spacer(1, 24))

    elements.append(Paragraph("Symptoms Provided:", styleHeading))
    symptoms_text = ", ".join(symptoms) if isinstance(symptoms, list) else symptoms
    elements.append(Paragraph(symptoms_text, styleNormal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Predicted Disease: {predicted_disease}", styleHeading))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Description:", styleHeading))
    elements.append(Paragraph(dis_des, styleNormal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Precautions:", styleHeading))
    for prec in my_precautions:
        elements.append(Paragraph(f"- {prec}", styleNormal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Medications:", styleHeading))
    for med in medications:
        elements.append(Paragraph(f"- {med}", styleNormal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Diet Recommendations:", styleHeading))
    for diet in my_diet:
        elements.append(Paragraph(f"- {diet}", styleNormal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Recommended Workouts:", styleHeading))
    for wrk in workout:
        elements.append(Paragraph(f"- {wrk}", styleNormal))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Consult These Doctors:", styleHeading))
    for doc_info in doctors_list:
        elements.append(
            Paragraph(f"- {doc_info['DoctorName']} ({doc_info['Specialization']})-{doc_info['Hospital']}", styleNormal))
    elements.append(Spacer(1, 12))

    doc.build(elements)
    return pdf_path
