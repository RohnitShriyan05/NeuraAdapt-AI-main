import os
from flask import Blueprint, request, jsonify

from services.transcription import transcribe_video

transcription_bp = Blueprint("transcription", __name__)

@transcription_bp.route("/transcribe", methods=["POST"])
def transcribe_route():
    if "video" not in request.files:
        return jsonify({"error": "No video file uploaded"}), 400
    
    video = request.files["video"]
    video_path = "temp_video.mp4"
    video.save(video_path)
    
    try:
        result = transcribe_video(video_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(video_path)