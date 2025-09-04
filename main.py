from fastapi import FastAPI
from database.database import engine
from fastapi.staticfiles import StaticFiles
from database import models
from routers.prediction import router as prediction_router
from routers.register import router as register_router
from routers.login import router as login_router
from routers.pages import router as pages_router
from routers.feedback import router as feedback_router
from routers.home import router as home_router
from routers.report import router as report_router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(home_router)
app.include_router(register_router)
app.include_router(login_router)
app.include_router(prediction_router)
app.include_router(pages_router)
app.include_router(report_router)
app.include_router(feedback_router)
