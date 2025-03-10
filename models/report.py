from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Report(Base):
    __tablename__ = "reports"

    report_id = Column(Integer, primary_key=True, autoincrement=True)
    report_reason = Column(String, nullable=False)
    report_desc = Column(String, nullable=False)

    # Relationship
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    group = relationship("Group", back_populates="reports")
