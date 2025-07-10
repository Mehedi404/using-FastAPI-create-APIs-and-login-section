from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean
from sqlalchemy.orm import relationship
from db import Base

class UserDepartment(Base):
    __tablename__ = "user_departments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    description = Column(Text)

    user = relationship("User", back_populates="user_departments")  # ✅ matches User model

    department = relationship("Department", back_populates="user_departments")

