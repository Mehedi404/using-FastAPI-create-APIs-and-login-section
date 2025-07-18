from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String)
    student_age = Column(String)
    student_address = Column(String)
    student_phone = Column(Integer)



