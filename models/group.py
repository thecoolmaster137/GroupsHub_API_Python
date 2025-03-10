from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Group(Base):
    __tablename__ = "groups"

    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String, nullable=False)
    group_link = Column(String, nullable=False)
    country = Column(String, nullable=False)
    language = Column(String, nullable=False)
    group_desc = Column(String, nullable=True)
    group_rules = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    group_image = Column(String, nullable=False)
    pin = Column(Boolean, default=False)

    # Relationships
    cat_id = Column(Integer, ForeignKey("categories.cat_id"))
    category = relationship("Category", back_populates="groups")

    app_id = Column(Integer, ForeignKey("applications.app_id"))
    application = relationship("Application", back_populates="groups")

    reports = relationship("Report", back_populates="group")
