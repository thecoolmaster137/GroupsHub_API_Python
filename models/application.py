from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Application(Base):
    __tablename__ = "applications"

    app_id = Column(Integer, primary_key=True, autoincrement=True)
    app_name = Column(String, nullable=False, unique=True)

    groups = relationship("Group", back_populates="application")
