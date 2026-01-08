import cv2
import os
import time

# Get the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define absolute path to the video clips folder
video_dir = os.path.join(script_dir, "../output/video_clips")

# Normalize and resolve the path
video_dir = os.path.abspath(video_dir)

print(f"🔍 Looking for videos in: {video_dir}")

# Check if directory exists
if not os.path.exists(video_dir):
    print("❌ Video clips directory not found!")
    exit()

# List video files
video_files = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]

if not video_files:
    print("❌ No video clips found!")
    exit()

# Play videos
for video_file in video_files:
    video_path = os.path.join(video_dir, video_file)

    # Delete existing file before writing a new one (optional)
    if os.path.exists(video_path):
        os.remove(video_path)  # Ensures no overwrite prompt
        print(f"🗑️ Deleted existing file: {video_file}")

    # Optionally rename file with a timestamp
