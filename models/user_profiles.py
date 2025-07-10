from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from db import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    firstname = Column(String)
    lastname = Column(String)
    date_of_birth = Column(Date)

    user = relationship("User", back_populates="profile")
