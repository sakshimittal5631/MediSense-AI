from fastapi import Form, Depends, APIRouter
from sqlalchemy.orm import Session
from database.database import get_db
from fastapi.responses import RedirectResponse
from database import models

router = APIRouter()


@router.post("/feedback")
async def submit_feedback(
    symptoms: str = Form(...),
    predicted_disease: str = Form(...),
    user_feedback: str = Form(...),
    comments: str = Form(""),
    db: Session = Depends(get_db)
):
    fb = models.Feedback(
        symptoms=symptoms,
        predicted_disease=predicted_disease,
        user_feedback=user_feedback,
        comments=comments
    )
    db.add(fb)
    db.commit()

    return RedirectResponse(url="/predict?msg=feedback_success", status_code=303)
