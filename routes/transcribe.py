import os
import subprocess
import json
import whisper
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
from flask import Blueprint, request, jsonify

def extract_audio(video_path, audio_path="audio.wav"):
    if os.path.exists(audio_path):
        os.remove(audio_path)
    command = [
        "ffmpeg", "-y", "-i", video_path, "-ac", "1", "-ar", "16000", audio_path
    ]
    subprocess.run(command, check=True)
    return audio_path

def transcribe_audio(audio_path, model_name="base"):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path, verbose=False)
    return result

def cluster_topics(segments):
    texts = [seg["text"] for seg in segments]
    topic_model = BERTopic(verbose=True)
    topics, _ = topic_model.fit_transform(texts)
    for seg, topic in zip(segments, topics):
        seg["topic"] = topic
    return topic_model, segments

def group_segments_into_paragraphs(segments):
    if not segments:
        return []
    paragraphs = []
    segments.sort(key=lambda s: s["start"])
    current = {"topic": segments[0]["topic"], "text": segments[0]["text"], "start": segments[0]["start"], "end": segments[0]["end"]}
    for seg in segments[1:]:
        if seg["topic"] == current["topic"]:
            current["text"] += " " + seg["text"]
            current["end"] = seg["end"]
        else:
            paragraphs.append(current)
            current = {"topic": seg["topic"], "text": seg["text"], "start": seg["start"], "end": seg["end"]}
    paragraphs.append(current)
    return paragraphs

def transcribe_video(video_path, model_name="base", num_large_topics=3):
    audio_file = extract_audio(video_path)
    transcription = transcribe_audio(audio_file, model_name=model_name)
    segments = transcription.get("segments", [])
    _, segments_with_topics = cluster_topics(segments)
    paragraphs = group_segments_into_paragraphs(segments_with_topics)
    return [{"start": p["start"], "end": p["end"], "text": p["text"]} for p in paragraphs]

# Flask Blueprint for modular integration
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