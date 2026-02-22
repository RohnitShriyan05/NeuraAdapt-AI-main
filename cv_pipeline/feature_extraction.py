from dataclasses import dataclass
from typing import Optional, Tuple

import cv2
import numpy as np


@dataclass
class FrameFeatures:
    timestamp: float
    yaw: float
    pitch: float
    roll: float
    gaze_x: float
    gaze_y: float
    blink: float
    mouth_open: float
    face_confidence: float


def _eye_aspect_ratio(eye: np.ndarray) -> float:
    a = np.linalg.norm(eye[1] - eye[5])
    b = np.linalg.norm(eye[2] - eye[4])
    c = np.linalg.norm(eye[0] - eye[3])
    return (a + b) / (2.0 * c + 1e-6)


def _mouth_aspect_ratio(mouth: np.ndarray) -> float:
    a = np.linalg.norm(mouth[2] - mouth[10])
    b = np.linalg.norm(mouth[4] - mouth[8])
    c = np.linalg.norm(mouth[0] - mouth[6])
    return (a + b) / (2.0 * c + 1e-6)


def _solve_head_pose(image_size: Tuple[int, int], image_points: np.ndarray) -> Tuple[float, float, float]:
    model_points = np.array(
        [
            (0.0, 0.0, 0.0),         # Nose tip
            (0.0, -330.0, -65.0),    # Chin
            (-225.0, 170.0, -135.0), # Left eye corner
            (225.0, 170.0, -135.0),  # Right eye corner
            (-150.0, -150.0, -125.0),# Left mouth corner
            (150.0, -150.0, -125.0), # Right mouth corner
        ],
        dtype=np.float32,
    )

    focal_length = image_size[1]
    center = (image_size[1] / 2, image_size[0] / 2)
    camera_matrix = np.array(
        [[focal_length, 0, center[0]], [0, focal_length, center[1]], [0, 0, 1]], dtype=np.float32
    )
    dist_coeffs = np.zeros((4, 1), dtype=np.float32)

    success, rotation_vec, _ = cv2.solvePnP(
        model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE
    )
    if not success:
        return 0.0, 0.0, 0.0

    rotation_mat, _ = cv2.Rodrigues(rotation_vec)
    sy = np.sqrt(rotation_mat[0, 0] ** 2 + rotation_mat[1, 0] ** 2)
    singular = sy < 1e-6

    if not singular:
        pitch = np.arctan2(rotation_mat[2, 1], rotation_mat[2, 2])
        yaw = np.arctan2(-rotation_mat[2, 0], sy)
        roll = np.arctan2(rotation_mat[1, 0], rotation_mat[0, 0])
    else:
        pitch = np.arctan2(-rotation_mat[1, 2], rotation_mat[1, 1])
        yaw = np.arctan2(-rotation_mat[2, 0], sy)
        roll = 0.0

    return float(np.degrees(yaw)), float(np.degrees(pitch)), float(np.degrees(roll))


def extract_features(
    frame_bgr: np.ndarray,
    face_landmarks: np.ndarray,
    timestamp: float,
    face_confidence: float,
) -> Optional[FrameFeatures]:
    image_h, image_w = frame_bgr.shape[:2]

    def to_np(idx_list):
        return np.array([(face_landmarks[i][0], face_landmarks[i][1]) for i in idx_list], dtype=np.float32)

    # Eye landmarks for EAR
    left_eye_idx = [33, 160, 158, 133, 153, 144]
    right_eye_idx = [362, 385, 387, 263, 373, 380]
    left_eye = to_np(left_eye_idx)
    right_eye = to_np(right_eye_idx)

    left_ear = _eye_aspect_ratio(left_eye)
    right_ear = _eye_aspect_ratio(right_eye)
    blink = (left_ear + right_ear) / 2.0

    # Mouth landmarks
    mouth_idx = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308]
    mouth = to_np(mouth_idx)
    mouth_open = _mouth_aspect_ratio(mouth)

    # Head pose landmarks: nose tip, chin, left/right eye, left/right mouth
    pose_idx = [1, 152, 33, 263, 61, 291]
    image_points = to_np(pose_idx)
    yaw, pitch, roll = _solve_head_pose((image_h, image_w), image_points)

    # Gaze proxy from iris center relative to eye corners
    left_iris_idx = [468, 469, 470, 471]
    right_iris_idx = [473, 474, 475, 476]

    left_iris = to_np(left_iris_idx)
    right_iris = to_np(right_iris_idx)

    left_center = left_iris.mean(axis=0)
    right_center = right_iris.mean(axis=0)

    left_eye_left = face_landmarks[33]
    left_eye_right = face_landmarks[133]
    right_eye_left = face_landmarks[362]
    right_eye_right = face_landmarks[263]

    left_range = max(1e-6, left_eye_right[0] - left_eye_left[0])
    right_range = max(1e-6, right_eye_right[0] - right_eye_left[0])

    gaze_x = ((left_center[0] - left_eye_left[0]) / left_range + (right_center[0] - right_eye_left[0]) / right_range) / 2.0
    gaze_y = ((left_center[1] - left_eye_left[1]) / left_range + (right_center[1] - right_eye_left[1]) / right_range) / 2.0

    return FrameFeatures(
        timestamp=timestamp,
        yaw=yaw,
        pitch=pitch,
        roll=roll,
        gaze_x=float(gaze_x),
        gaze_y=float(gaze_y),
        blink=float(blink),
        mouth_open=float(mouth_open),
        face_confidence=float(face_confidence),
    )
