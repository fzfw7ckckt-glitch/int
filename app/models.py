from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    investigations = relationship("Investigation", back_populates="owner")

class Investigation(Base):
    __tablename__ = "investigations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    target_identifier = Column(String, index=True)
    status = Column(String, default="pending")  # pending, running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner = relationship("User", back_populates="investigations")
    evidence = relationship("Evidence", back_populates="investigation")

class Evidence(Base):
    __tablename__ = "evidence"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    investigation_id = Column(String, ForeignKey("investigations.id"), nullable=False)
    source = Column(String)  # tool name
    data = Column(Text)  # JSON data
    metadata_json = Column(Text, nullable=True) # Додаткові метадані
    hash_sha256 = Column(String)  # for integrity
    created_at = Column(DateTime, default=datetime.utcnow)
    
    investigation = relationship("Investigation", back_populates="evidence")
