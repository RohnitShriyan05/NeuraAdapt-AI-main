import csv
import os
from dataclasses import asdict
from typing import Dict, List, Tuple

import cv2
import mediapipe as mp

from config import settings
from cv_pipeline.feature_extraction import FrameFeatures, extract_features
from cv_pipeline.scoring import ScoredFrame, score_frame, smooth_scores


mp_face_mesh = mp.solutions.face_mesh


def _to_pixel_coords(landmarks, image_w: int, image_h: int):
    return [(lm.x * image_w, lm.y * image_h) for lm in landmarks]


def _compute_heatmap(scores: List[ScoredFrame], bin_size: float) -> List[Dict[str, float]]:
    if not scores:
        return []

    max_time = scores[-1].features.timestamp
    num_bins = int(max_time // bin_size) + 1
    sums = [0.0] * num_bins
    counts = [0] * num_bins

    for score in scores:
        idx = int(score.features.timestamp // bin_size)
        sums[idx] += score.engagement
        counts[idx] += 1

    heatmap = []
    for idx in range(num_bins):
        start = idx * bin_size
        end = start + bin_size
        avg = sums[idx] / counts[idx] if counts[idx] else 0.0
        heatmap.append({"start": start, "end": end, "avg_engagement": avg})

    return heatmap


def _extract_confusion_events(scores: List[ScoredFrame], threshold: float, window_sec: float) -> List[Dict[str, float]]:
    if not scores:
        return []

    events = []
    window_start = 0
    n = len(scores)

    while window_start < n:
        window_end = window_start
        start_ts = scores[window_start].features.timestamp

        while window_end < n and scores[window_end].features.timestamp - start_ts <= window_sec:
            window_end += 1

        window_scores = scores[window_start:window_end]
        if not window_scores:
            break

        avg_confusion = sum(s.confusion for s in window_scores) / len(window_scores)
        if avg_confusion >= threshold:
            events.append(
                {
                    "start": start_ts,
                    "end": window_scores[-1].features.timestamp,
                    "score": avg_confusion,
                }
            )
            window_start = window_end
        else:
            window_start += 1

    return events


def analyze_video(video_path: str, output_dir: str) -> Tuple[List[ScoredFrame], List[Dict[str, float]], List[Dict[str, float]]]:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Unable to open video")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    stride = max(1, int(round(fps / settings.sample_fps)))

    os.makedirs(output_dir, exist_ok=True)
    raw_features: List[FrameFeatures] = []

    with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as face_mesh:
        frame_idx = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if stride > 1 and frame_idx % stride != 0:
                frame_idx += 1
                continue

            if settings.max_frames and len(raw_features) >= settings.max_frames:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = face_mesh.process(rgb_frame)
            timestamp = frame_idx / fps

            if result.multi_face_landmarks:
                landmarks = result.multi_face_landmarks[0]
                coords = _to_pixel_coords(landmarks.landmark, frame.shape[1], frame.shape[0])
                features = extract_features(frame, coords, timestamp, face_confidence=1.0)
                if features:
                    raw_features.append(features)

            frame_idx += 1

    cap.release()

    scored = [score_frame(features) for features in raw_features]
    smoothed = smooth_scores(scored, window=5)

    heatmap = _compute_heatmap(smoothed, settings.heatmap_bin_sec)
    events = _extract_confusion_events(smoothed, settings.confusion_threshold, settings.confusion_window_sec)

    features_path = os.path.join(output_dir, "features.csv")
    with open(features_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "timestamp",
                "yaw",
                "pitch",
                "roll",
                "gaze_x",
                "gaze_y",
                "blink",
                "mouth_open",
                "face_confidence",
                "engagement",
                "confusion",
            ],
        )
        writer.writeheader()
        for score in smoothed:
            row = asdict(score.features)
            row["engagement"] = score.engagement
            row["confusion"] = score.confusion
            writer.writerow(row)

    return smoothed, heatmap, events
