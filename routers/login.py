from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import models
from database.database import get_db
from authentication.hashing import Hash
from authentication import jwt_token

router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == request.username).first()

    if not user or not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = jwt_token.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}
