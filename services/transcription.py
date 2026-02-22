import os
import subprocess
from typing import List, Dict

import whisper
from bertopic import BERTopic


def extract_audio(video_path: str, audio_path: str = "audio.wav") -> str:
    if os.path.exists(audio_path):
        os.remove(audio_path)
    command = ["ffmpeg", "-y", "-i", video_path, "-ac", "1", "-ar", "16000", audio_path]
    subprocess.run(command, check=True)
    return audio_path


def transcribe_audio(audio_path: str, model_name: str = "base") -> Dict:
    model = whisper.load_model(model_name)
    return model.transcribe(audio_path, verbose=False)


def cluster_topics(segments: List[Dict]) -> List[Dict]:
    texts = [seg["text"] for seg in segments]
    if not texts:
        return segments
    topic_model = BERTopic(verbose=False)
    topics, _ = topic_model.fit_transform(texts)
    for seg, topic in zip(segments, topics):
        seg["topic"] = topic
    return segments


def group_segments_into_paragraphs(segments: List[Dict]) -> List[Dict]:
    if not segments:
        return []
    segments.sort(key=lambda s: s["start"])
    paragraphs = []
    current = {
        "topic": segments[0].get("topic"),
        "text": segments[0]["text"],
        "start": segments[0]["start"],
        "end": segments[0]["end"],
    }
    for seg in segments[1:]:
        if seg.get("topic") == current.get("topic"):
            current["text"] += " " + seg["text"]
            current["end"] = seg["end"]
        else:
            paragraphs.append(current)
            current = {
                "topic": seg.get("topic"),
                "text": seg["text"],
                "start": seg["start"],
                "end": seg["end"],
            }
    paragraphs.append(current)
    return paragraphs


def transcribe_video(video_path: str, model_name: str = "base") -> List[Dict]:
    audio_file = extract_audio(video_path)
    transcription = transcribe_audio(audio_file, model_name=model_name)
    segments = transcription.get("segments", [])
    segments = cluster_topics(segments)
    paragraphs = group_segments_into_paragraphs(segments)
    return [{"start": p["start"], "end": p["end"], "text": p["text"]} for p in paragraphs]
