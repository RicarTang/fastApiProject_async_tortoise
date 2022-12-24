from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional, List


class BaseOut(BaseModel):
    success: bool = Field(default=True)


class TestIn(BaseModel):
    description: str = Field(max_length=20)


class TestTo(TestIn):
    c_time: datetime

    class Config:
        orm_mode = True


class TestOut(BaseOut):
    data: TestTo


class User(BaseModel):
    username: str = Field(max_length=12, min_length=1)
    email: EmailStr


class UserIn(User):
    password: str = Field(max_length=30, min_length=6)


class UserTo(User):
    disable: Optional[bool] = None
    create_time: datetime = Field(description="创建时间")
    update_time: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserOut(BaseOut):
    data: UserTo


class UsersOut(BaseOut):
    data: List[UserTo]


class TokenIn(BaseModel):
    username: str
    password: str


class TokenTo(UserTo):
    access_token: str


class TokenOut(BaseOut):
    data: TokenTo
