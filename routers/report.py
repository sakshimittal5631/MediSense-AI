from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import FileResponse
from schemas.schemas import EmailSchema
from fastapi_mail import MessageSchema, MessageType
from mail.mail_config import fm
import os

router = APIRouter()


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
