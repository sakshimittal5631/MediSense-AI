from fastapi import APIRouter, Request, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datasets.data import diseases_list, symptoms_dict
from helper.helper_functions import helper
from helper.pdf_generater import generate_pdf
from helper.predicted import get_predicted_value


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/predict", response_class=HTMLResponse)
async def predict_get(request: Request, msg: str = Query(None)):
    alert_message = None
    if msg == "feedback_success":
        alert_message = "✅ Thank you for your feedback!"

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "alert_message": alert_message, "symptoms_dict": symptoms_dict,
            "diseases_list": diseases_list}
    )


@router.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    symptoms: str = Form(...)
):
    if not symptoms.strip() or symptoms.strip().lower() == "symptoms":
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "alert_message": "⚠️ Please enter at least one valid symptom."}
        )

    user_symptoms_raw = [s.strip() for s in symptoms.split(',') if s.strip()]

    if not user_symptoms_raw:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "alert_message": "⚠️ Please enter valid symptoms."}
        )

    valid_symptoms = []
    invalid_symptoms = []

    for sym in user_symptoms_raw:
        normalized = sym.lower().replace(" ", "_")
        if normalized in symptoms_dict:
            valid_symptoms.append(normalized)
        else:
            invalid_symptoms.append(sym)

    if invalid_symptoms:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "alert_message": f"❌ Invalid symptoms: {', '.join(invalid_symptoms)}. "
                                 f"Please enter them exactly as shown in the symptoms list."
            }
        )

    if not valid_symptoms:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "alert_message": "⚠️ No valid symptoms detected. Please try again."}
        )

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
            "symptoms": ", ".join(valid_symptoms),
            "symptoms_dict": symptoms_dict,
            "diseases_list": diseases_list
        }
    )
