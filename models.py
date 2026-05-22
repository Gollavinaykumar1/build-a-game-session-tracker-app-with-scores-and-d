# models.py — table prefix: build_a_game_session_tracker_app_with_sc
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class Item(Base):
    __tablename__ = "build_a_game_session_tracker_app_with_sc_items"
    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String, index=True)
    description = Column(String, nullable=True)
    status      = Column(String, default="active")
    score       = Column(Float, default=0.0)
    team        = Column(String, nullable=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
