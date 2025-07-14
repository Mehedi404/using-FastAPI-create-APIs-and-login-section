

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean


from sqlalchemy import Column, Integer, String, Boolean
Base = declarative_base()

from db import Base
from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean
from sqlalchemy.orm import relationship



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    email_token = Column(String, nullable=True)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    user_departments = relationship("UserDepartment", back_populates="user")
    login_history = relationship("LoginHistory", back_populates="user")
    uploads = relationship("FileUpload", back_populates="user")


    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)
