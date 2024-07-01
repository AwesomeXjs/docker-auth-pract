from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    password: str
    email: EmailStr | None = None
    active: bool = True


class UserRegisterSchema(BaseModel):
    username: str = Field(max_length=15)
    password: str


class UserUpdateSchema(BaseModel):
    username: str = Field(max_length=15)
