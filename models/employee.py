from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    Employee_name = Column(String)
    Employee_phone = Column(String)
    Employee_address = Column(String)
    Employee_age = Column(Integer)
