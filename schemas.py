from pydantic import BaseModel, EmailStr
from typing import Optional


# ---------- Book ----------
class BookBase(BaseModel):
    title: str
    author: str
    description: str
    year: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Employee ----------
class EmployeeBase(BaseModel):
    Employee_name: str
    Employee_phone: str
    Employee_address: str
    Employee_age: int

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Student ----------
class StudentBase(BaseModel):
    student_name: str
    student_age: str
    student_address: str
    student_phone: int

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True


# ---------- User ----------
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    is_admin: Optional[bool] = False

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_admin: Optional[bool] = False

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# ---------- Login ----------
class LoginInput(BaseModel):
    username_or_email: str
    password: str




class EmailRequest(BaseModel):
    email: EmailStr


class PasswordResetRequest(BaseModel):
    token: str
    new_password: str

