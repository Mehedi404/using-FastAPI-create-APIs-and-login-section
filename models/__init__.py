
from .book import Book
from .employee import Employee
from  .student import Student
from .user import User, pwd_context
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
