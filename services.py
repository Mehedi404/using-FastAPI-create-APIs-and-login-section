from models import Book, Employee, Student
from sqlalchemy.orm import Session
from schemas import BookCreate, EmployeeCreate, StudentCreate
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = 7
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
from models import User, pwd_context
from schemas import UserCreate
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import APIKeyHeader


api_key_scheme = APIKeyHeader(name="Authorization")

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def create_book(db: Session, data: BookCreate):
    book_instance = Book(**data.model_dump())
    db.add(book_instance)
    db.commit()
    db.refresh(book_instance)
    return book_instance

def get_books(db: Session):
    return db.query(Book).all()

def update_book(db: Session, id: int, data: BookCreate):
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        return None
    for key, value in data.model_dump().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, id: int):
    book = db.query(Book).filter(Book.id == id).first()
    if not book:
        return None
    db.delete(book)
    db.commit()
    return book







def create_employee(db: Session, data: EmployeeCreate):
    emp_instance = Employee(**data.model_dump())
    db.add(emp_instance)
    db.commit()
    db.refresh(emp_instance)
    return emp_instance

def get_employees(db: Session):
    return db.query(Employee).all()

def update_employee(db: Session, id: int, data: EmployeeCreate):
    emp = db.query(Employee).filter(Employee.id == id).first()
    if not emp:
        return None
    for key, value in data.model_dump().items():
        setattr(emp, key, value)
    db.commit()
    db.refresh(emp)
    return emp

def delete_employee(db: Session, id: int):
    emp = db.query(Employee).filter(Employee.id == id).first()
    if not emp:
        return None
    db.delete(emp)
    db.commit()
    return emp









def create_student(db: Session, data: StudentCreate):
    emp_instance = Student(**data.model_dump())
    db.add(emp_instance)
    db.commit()
    db.refresh(emp_instance)
    return emp_instance

def get_students(db: Session):
    return db.query(Student).all()

def update_student(db: Session, id: int, data: StudentCreate):
    std = db.query(Student).filter(Student.id == id).first()
    if not std:
        return None
    for key, value in data.model_dump().items():
        setattr(std, key, value)
    db.commit()
    db.refresh(std)
    return std

def delete_student(db: Session, id: int):
    std = db.query(Student).filter(Student.id == id).first()
    if not std:
        return None
    db.delete(std)
    db.commit()
    return std




def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_username_or_email(db: Session, username_or_email: str):
    return db.query(User).filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()





def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username_or_email: str, password: str):
    user = get_user_by_username_or_email(db, username_or_email)
    if not user or not user.verify_password(password):
        return None
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_username_or_email(db: Session, value: str):
    return db.query(User).filter((User.username == value) | (User.email == value)).first()




def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: Optional[bool] = False