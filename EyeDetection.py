import cv2
import dlib
import numpy as np
import csv
import time
import os
import urllib.request
import bz2
from collections import deque

def download_predictor():
    predictor_path = "shape_predictor_68_face_landmarks.dat"
    if not os.path.isfile(predictor_path):
        print("Downloading facial landmark predictor...")
        url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
        bz2_file = predictor_path + ".bz2"
        urllib.request.urlretrieve(url, bz2_file)
        print("Extracting...")
        with open(predictor_path, 'wb') as new_file, bz2.BZ2File(bz2_file, 'rb') as file:
            new_file.write(file.read())
        os.remove(bz2_file)
        print("Facial landmark predictor downloaded and extracted.")
    return predictor_path

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

class EyeBlinkDetector:
    def __init__(self, output_file="blinks_movements.csv", ear_threshold=0.25, camera_id=0, display=True):
        self.output_file = output_file
        self.ear_threshold = ear_threshold
        self.camera_id = camera_id
        self.display = display

        self.detector = dlib.get_frontal_face_detector()
        predictor_path = download_predictor()
        self.predictor = dlib.shape_predictor(predictor_path)

        self.left_eye_indices = list(range(36, 42))
        self.right_eye_indices = list(range(42, 48))

        self.blink_count = 0
        self.frequent_movement_count = 0
        self.eye_positions = deque(maxlen=30)  # Store last 30 frames' eye positions
        self.movement_threshold = 5  # Adjust this value for sensitivity
        self.start_time = 0  # Start timer from 0

    def get_eye_landmarks(self, landmarks, indices):
        return np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in indices], dtype=np.float32)

    def get_eye_center(self, eye):
        return np.mean(eye, axis=0)

    def log_blinks(self):
        """Logs the number of blinks and frequent eye movements in a 10-second interval."""
        end_time = self.start_time + 10  # Increment time in seconds
        start_time_str = f"{self.start_time}s"
        end_time_str = f"{end_time}s"

        # Save data to CSV file
        with open(self.output_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([f"{start_time_str} - {end_time_str}", self.blink_count, self.frequent_movement_count])

        print(f"{start_time_str} - {end_time_str} | Blinks: {self.blink_count}, Eye Movements: {self.frequent_movement_count}")

        # Reset counters for the next 10-second interval
        self.blink_count = 0
        self.frequent_movement_count = 0
        self.eye_positions.clear()
        self.start_time = end_time  # Move to the next interval

    def run(self):
        cap = cv2.VideoCapture(self.camera_id)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return

        # Initialize CSV file with headers
        with open(self.output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Time Interval", "Blinks", "Eye Movements"])

        start_real_time = time.time()  # Track real elapsed time

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture frame.")
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.detector(gray)

                if faces:
                    landmarks = self.predictor(gray, faces[0])
                    left_eye = self.get_eye_landmarks(landmarks, self.left_eye_indices)
                    right_eye = self.get_eye_landmarks(landmarks, self.right_eye_indices)
                    left_ear = eye_aspect_ratio(left_eye)
                    right_ear = eye_aspect_ratio(right_eye)
                    ear = (left_ear + right_ear) / 2.0

                    # Detect blinks
                    if ear < self.ear_threshold:
                        self.blink_count += 1
                        time.sleep(0.2)  # Prevent double counting

                    # Detect frequent eye movements
                    left_center = self.get_eye_center(left_eye)
                    right_center = self.get_eye_center(right_eye)
                    eye_center = (left_center + right_center) / 2.0  # Average of both eye centers
                    self.eye_positions.append(eye_center)

                    if len(self.eye_positions) >= 2:
                        movement = np.linalg.norm(self.eye_positions[-1] - self.eye_positions[-2])
                        if movement > self.movement_threshold:
                            self.frequent_movement_count += 1  # Increase count if movement is excessive

                # Log data every 10 seconds
                if time.time() - start_real_time >= 10:
                    self.log_blinks()
                    start_real_time = time.time()  # Reset real-time tracker

                # Display the results
                if self.display:
                    cv2.putText(frame, f"Blinks: {self.blink_count}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.putText(frame, f"Eye Moves: {self.frequent_movement_count}", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.imshow('Eye Blink & Movement Detector', frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

        finally:
            cap.release()
            if self.display:
                cv2.destroyAllWindows()

# Run the detector
if __name__ == "__main__":
    detector = EyeBlinkDetector()
    detector.run()
