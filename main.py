from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.prediction import router as prediction_router
from routers.register import router as register_router
from routers.login import router as login_router
from routers.pages import router as pages_router
import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(register_router)
app.include_router(login_router)
app.include_router(prediction_router)
app.include_router(pages_router)
