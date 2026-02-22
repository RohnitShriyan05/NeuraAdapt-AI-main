import json
import os
import uuid
from typing import Dict, List

from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session

from config import settings
from cv_pipeline.analysis import analyze_video
from db import SessionLocal
from models import ConfusionEvent, HeatmapBin, Note, Session as SessionModel
from services.notes import generate_notes
from services.transcription import transcribe_video
from storage import get_storage


analysis_bp = Blueprint("analysis", __name__)


def _save_session_records(
    db: Session,
    session: SessionModel,
    heatmap: List[Dict[str, float]],
    events: List[Dict[str, float]],
    notes: List[Dict[str, str]],
) -> None:
    for event in events:
        db.add(
            ConfusionEvent(
                session_id=session.id,
                start_ts=event["start"],
                end_ts=event["end"],
                score=event["score"],
            )
        )

    for bin_item in heatmap:
        db.add(
            HeatmapBin(
                session_id=session.id,
                bucket_start=bin_item["start"],
                bucket_end=bin_item["end"],
                avg_engagement=bin_item["avg_engagement"],
            )
        )

    for note in notes:
        db.add(
            Note(
                session_id=session.id,
                timestamp=note["timestamp"],
                text=note["text"],
                source_segment=note.get("source_segment"),
            )
        )


@analysis_bp.route("/analyze", methods=["POST"])
def analyze_route():
    if "video" not in request.files:
        return jsonify({"error": "No video file uploaded"}), 400

    video = request.files["video"]
    session_id = uuid.uuid4()
    filename = f"{session_id}_{video.filename}"
    temp_path = os.path.join("output", filename)
    os.makedirs("output", exist_ok=True)
    video.save(temp_path)

    db = SessionLocal()
    session_record = SessionModel(
        id=session_id,
        video_filename=video.filename,
        status="processing",
    )
    db.add(session_record)
    db.commit()

    try:
        output_dir = os.path.join("output", "sessions", str(session_id))
        scored, heatmap, events = analyze_video(temp_path, output_dir)

        transcript_segments = transcribe_video(temp_path)
        notes = generate_notes(events, transcript_segments)

        avg_engagement = sum(s.engagement for s in scored) / len(scored) if scored else 0.0
        summary = {
            "avg_engagement": avg_engagement,
            "confusion_events": len(events),
            "duration_seconds": scored[-1].features.timestamp if scored else 0.0,
        }

        storage = get_storage()
        artifacts_path = f"{session_id}"
        storage.write_json(f"{artifacts_path}/heatmap.json", heatmap)
        storage.write_json(f"{artifacts_path}/events.json", events)
        storage.write_json(f"{artifacts_path}/notes.json", notes)
        storage.write_json(f"{artifacts_path}/summary.json", summary)

        features_path = os.path.join(output_dir, "features.csv")
        if os.path.exists(features_path):
            with open(features_path, "r", encoding="utf-8") as handle:
                storage.write_text(f"{artifacts_path}/features.csv", handle.read())

        _save_session_records(db, session_record, heatmap, events, notes)

        session_record.status = "completed"
        session_record.summary_json = json.dumps(summary)
        session_record.artifacts_path = artifacts_path
        if scored:
            session_record.duration_seconds = scored[-1].features.timestamp
        db.commit()

        return jsonify({
            "session_id": str(session_id),
            "summary": summary,
            "heatmap": heatmap,
            "events": events,
            "notes": notes,
        })
    except Exception as exc:
        session_record.status = "failed"
        db.commit()
        return jsonify({"error": str(exc)}), 500
    finally:
        db.close()
        if os.path.exists(temp_path):
            os.remove(temp_path)


@analysis_bp.route("/sessions/<session_id>", methods=["GET"])
def session_route(session_id: str):
    db = SessionLocal()
    try:
        try:
            parsed_id = uuid.UUID(session_id)
        except ValueError:
            return jsonify({"error": "Invalid session id"}), 400

        session_record = db.query(SessionModel).filter(SessionModel.id == parsed_id).first()
        if not session_record:
            return jsonify({"error": "Session not found"}), 404

        return jsonify(
            {
                "session_id": str(session_record.id),
                "status": session_record.status,
                "summary": json.loads(session_record.summary_json) if session_record.summary_json else None,
                "artifacts_path": session_record.artifacts_path,
            }
        )
    finally:
        db.close()
