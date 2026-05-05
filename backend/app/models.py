from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database import Base


class HCP(Base):
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialty = Column(String(100))
    organization = Column(String(150))
    location = Column(String(150))

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)

    hcp_name = Column(String(100), nullable=False)
    interaction_type = Column(String(50), nullable=False)
    interaction_date = Column(String(50), nullable=False)

    topics_discussed = Column(Text)
    materials_shared = Column(Text)
    samples_distributed = Column(Text)
    sentiment = Column(String(50))
    outcome = Column(Text)
    follow_up_action = Column(Text)
    summary = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())