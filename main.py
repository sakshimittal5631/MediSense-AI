from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.prediction import router as prediction_router
from routers.pages import router as pages_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(prediction_router)
app.include_router(pages_router)