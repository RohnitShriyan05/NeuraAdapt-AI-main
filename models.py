import datetime as dt
import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
    video_filename = Column(String(512), nullable=False)
    duration_seconds = Column(Float, nullable=True)
    fps = Column(Float, nullable=True)
    status = Column(String(32), default="created", nullable=False)
    summary_json = Column(Text, nullable=True)
    artifacts_path = Column(String(512), nullable=True)

    confusion_events = relationship("ConfusionEvent", back_populates="session", cascade="all, delete-orphan")
    heatmap_bins = relationship("HeatmapBin", back_populates="session", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="session", cascade="all, delete-orphan")


class ConfusionEvent(Base):
    __tablename__ = "confusion_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    start_ts = Column(Float, nullable=False)
    end_ts = Column(Float, nullable=False)
    score = Column(Float, nullable=False)

    session = relationship("Session", back_populates="confusion_events")


class HeatmapBin(Base):
    __tablename__ = "heatmap_bins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    bucket_start = Column(Float, nullable=False)
    bucket_end = Column(Float, nullable=False)
    avg_engagement = Column(Float, nullable=False)

    session = relationship("Session", back_populates="heatmap_bins")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False)
    timestamp = Column(Float, nullable=False)
    text = Column(Text, nullable=False)
    source_segment = Column(Text, nullable=True)

    session = relationship("Session", back_populates="notes")
