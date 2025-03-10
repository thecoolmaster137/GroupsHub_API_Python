from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"

    cat_id = Column(Integer, primary_key=True, autoincrement=True)
    cat_name = Column(String, nullable=False, unique=True)

    groups = relationship("Group", back_populates="category")
