from dataclasses import dataclass
from typing import List

import numpy as np

from cv_pipeline.feature_extraction import FrameFeatures


@dataclass
class ScoredFrame:
    features: FrameFeatures
    engagement: float
    confusion: float


def _normalize(value: float, max_value: float) -> float:
    return min(abs(value) / max_value, 1.0)


def score_frame(features: FrameFeatures) -> ScoredFrame:
    yaw_norm = _normalize(features.yaw, 30.0)
    pitch_norm = _normalize(features.pitch, 20.0)
    gaze_dev = _normalize(features.gaze_x - 0.5, 0.5) + _normalize(features.gaze_y - 0.5, 0.5)
    blink_penalty = 1.0 if features.blink < 0.18 else 0.0
    mouth_penalty = _normalize(features.mouth_open, 0.7)

    attention = 1.0 - (0.35 * yaw_norm + 0.25 * pitch_norm + 0.25 * gaze_dev + 0.10 * blink_penalty + 0.05 * mouth_penalty)
    attention = float(np.clip(attention, 0.0, 1.0))

    confusion = float(np.clip(0.35 * (1.0 - attention) + 0.30 * mouth_penalty + 0.20 * blink_penalty + 0.15 * gaze_dev, 0.0, 1.0))
    return ScoredFrame(features=features, engagement=attention, confusion=confusion)


def smooth_scores(scores: List[ScoredFrame], window: int) -> List[ScoredFrame]:
    if window <= 1:
        return scores

    engagements = np.array([s.engagement for s in scores])
    confusions = np.array([s.confusion for s in scores])

    kernel = np.ones(window) / window
    smoothed_engagement = np.convolve(engagements, kernel, mode="same")
    smoothed_confusion = np.convolve(confusions, kernel, mode="same")

    smoothed = []
    for idx, score in enumerate(scores):
        smoothed.append(
            ScoredFrame(
                features=score.features,
                engagement=float(smoothed_engagement[idx]),
                confusion=float(smoothed_confusion[idx]),
            )
        )
    return smoothed
