from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from schemas import schemas
from database import models
from database.database import get_db
from authentication.hashing import Hash

router = APIRouter(tags=["Register"])

templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(request: schemas.User, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == request.username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    if db.query(models.User).filter(models.User.email == request.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    new_user = models.User(
        name=request.name,
        email=request.email,
        username=request.username,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"detail": "Account created successfully!", "username": new_user.username}
