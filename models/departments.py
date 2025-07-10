from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean
from sqlalchemy.orm import relationship
from db import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    user_departments = relationship("UserDepartment", back_populates="department")

