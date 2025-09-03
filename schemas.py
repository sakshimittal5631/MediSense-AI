from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    email: str
    username: str
    password: str

    class Config:
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    user_id: int | None = None


class EmailSchema(BaseModel):
    email: EmailStr
