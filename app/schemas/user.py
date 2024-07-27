from pydantic import BaseModel, EmailStr, constr

class UserRegisterModel(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=6)

class UserLoginModel(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
