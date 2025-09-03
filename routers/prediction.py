from fastapi import APIRouter, Request, Form, Depends, status, Query, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from mail_config import fm
from database import get_db
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from fastapi.responses import RedirectResponse
import os, numpy as np, pandas as pd, pickle
from oauth import get_current_user
from schemas import EmailSchema
import models
import ast

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Load CSV data and the ML model
sym_des = pd.read_csv("datasets/symtoms_df.csv")
precautions = pd.read_csv("datasets/precautions_df.csv")
workout = pd.read_csv("datasets/workout_df.csv")
description = pd.read_csv("datasets/description.csv")
medications = pd.read_csv("datasets/medications.csv")
diets = pd.read_csv("datasets/diets.csv")
doctors = pd.read_csv("datasets/doctors.csv")
svc = pickle.load(open("models/svc.pkl", "rb"))


# Utility function to fetch details for a disease
def helper(dis):
    desc = " ".join(description[description['Disease'] == dis]['Description'])
    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    med_raw = medications[medications['Disease'] == dis]['Medication'].values
    med = []
    for m in med_raw:
        if isinstance(m, str):
            try:
                parsed = ast.literal_eval(m)  # convert "['a','b']" -> ['a','b']
                if isinstance(parsed, list):
                    med.extend(parsed)
                else:
                    med.append(parsed)
            except Exception:
                med.append(m)
        else:
            med.append(m)
    diet_raw = diets[diets['Disease'] == dis]['Diet'].values
    die = []
    for d in diet_raw:
        if isinstance(d, str):
            try:
                parsed = ast.literal_eval(d)
                if isinstance(parsed, list):
                    die.extend(parsed)
                else:
                    die.append(parsed)
            except Exception:
                die.append(d)
        else:
            die.append(d)
    wrkout = workout[workout['disease'] == dis]['workout']
    doc_data = doctors[doctors['Disease'].str.strip().str.lower() == dis.strip().lower()][
        ['DoctorName', 'Specialization', 'Hospital']
    ].to_dict(orient="records")
    return desc, [col for col in pre.values], med, die, wrkout, doc_data


# Dictionaries for mapping symptoms to indices and disease predictions
symptoms_dict = {
    'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3,
    'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8,
    'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12,
    'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16,
    'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20,
    'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24,
    'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28,
    'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32,
    'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36,
    'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40,
    'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44,
    'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47,
    'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51,
    'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55,
    'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58,
    'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61,
    'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65,
    'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69,
    'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72,
    'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75,
    'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78,
    'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81,
    'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84,
    'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87,
    'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90,
    'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93,
    'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97,
    'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100,
    'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103,
    'increased_appetite': 104, 'polyuria': 105, 'family_history': 106,
    'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109,
    'visual_disturbances': 110, 'receiving_blood_transfusion': 111,
    'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114,
    'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116,
    'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119,
    'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122,
    'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126,
    'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129,
    'red_sore_around_nose': 130, 'yellow_crust_ooze': 131
}
diseases_list = {
    15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis',
    14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ',
    17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine',
    7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice',
    29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A',
    19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E',
    3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia',
    13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins',
    26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis',
    5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne',
    38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'
}


def get_predicted_value(patient_symptoms):
    vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([vector])[0]]


# Create a PDF report with clear formatting
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

    # Insert favicon logo if available
    logo_path = "static/favicon.png"
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=50, height=50)
        elements.append(logo)
        elements.append(Spacer(1, 12))

    elements.append(Paragraph("MediSense AI - Health Report", styleTitle))
    elements.append(Spacer(1, 24))

    # Display provided symptoms
    elements.append(Paragraph("Symptoms Provided:", styleHeading))
    symptoms_text = ", ".join(symptoms) if isinstance(symptoms, list) else symptoms
    elements.append(Paragraph(symptoms_text, styleNormal))
    elements.append(Spacer(1, 12))

    # Show prediction and details
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
            Paragraph(f"- {doc_info['DoctorName']} ({doc_info['Specialization']}) - {doc_info['Hospital']}", styleNormal))
    elements.append(Spacer(1, 12))

    doc.build(elements)
    return pdf_path

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db),
                username: str = Form(...), password: str = Form(...)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid Credentials"})
    if not Hash.verify(password, user.password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Incorrect Password"})

    response = RedirectResponse(url="/predict", status_code=status.HTTP_303_SEE_OTHER)
    return response

# Endpoint for predicting disease and generating the PDF
@router.get("/predict", response_class=HTMLResponse)
async def predict_get(request: Request, msg: str = Query(None)):
    alert_message = None
    if msg == "feedback_success":
        alert_message = "✅ Thank you for your feedback!"

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "alert_message": alert_message}
    )


@router.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    symptoms: str = Form(...)
):
    # Case 1: Placeholder or empty string
    if not symptoms.strip() or symptoms.strip().lower() == "symptoms":
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "alert_message": "⚠️ Please enter at least one valid symptom."}
        )

    # Step 1: Split and clean input
    user_symptoms_raw = [s.strip() for s in symptoms.split(',') if s.strip()]

    if not user_symptoms_raw:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "alert_message": "⚠️ Please enter valid symptoms."}
        )

    # Step 2: Normalize + validate against dataset
    valid_symptoms = []
    invalid_symptoms = []

    for sym in user_symptoms_raw:
        normalized = sym.lower().replace(" ", "_")
        if normalized in symptoms_dict:
            valid_symptoms.append(normalized)
        else:
            invalid_symptoms.append(sym)  # keep original as typed by user

    # Step 3: If invalid symptoms found → show popup
    if invalid_symptoms:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "alert_message": f"❌ Invalid symptoms: {', '.join(invalid_symptoms)}. "
                                 f"Please enter them exactly as shown in the symptoms list."
            }
        )

    # Step 4: If no valid symptoms left → show popup
    if not valid_symptoms:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "alert_message": "⚠️ No valid symptoms detected. Please try again."}
        )

    # Step 5: Run prediction
    predicted_disease = get_predicted_value(valid_symptoms)
    dis_des, prec, meds, rec_diet, wrkout, doc_list = helper(predicted_disease)

    my_precautions = [i for i in prec[0]]
    pdf_path = generate_pdf(
        predicted_disease,
        dis_des,
        my_precautions,
        meds,
        rec_diet,
        wrkout,
        valid_symptoms,
        doc_list
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "predicted_disease": predicted_disease,
            "dis_des": dis_des,
            "my_precautions": my_precautions,
            "medications": meds,
            "my_diet": rec_diet,
            "workout": wrkout,
            "doctors": doc_list,
            "pdf_report": pdf_path,
            "symptoms": ", ".join(valid_symptoms)
        }
    )


@router.get("/download_report", response_class=FileResponse)
async def download_report():
    return FileResponse("report.pdf", media_type="application/pdf", filename="MediSense_Report.pdf")


@router.post("/send_report")
async def send_report(email: EmailSchema, background_tasks: BackgroundTasks):
    pdf_path = "report.pdf"

    if not os.path.exists(pdf_path):
        return {"error": "No report available. Please generate a report first."}

    message = MessageSchema(
        subject="Your MediSense AI Health Report",
        recipients=[email.email],
        body="Hello,\n\nPlease find the health report attached.\n\nRegards,\nMediSense AI",
        subtype=MessageType.plain,
        attachments=[pdf_path]
    )

    background_tasks.add_task(fm.send_message, message)
    return {"message": f"✉️ Report sent successfully to {email.email}"}
