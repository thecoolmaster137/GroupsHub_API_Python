from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from database import Base

class Admin(Base):
    __tablename__ = "admins"

    admin_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    phno = Column(BigInteger, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
