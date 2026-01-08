import os
import subprocess
from datetime import datetime

# Get absolute paths
base_path = os.path.dirname(os.path.abspath(__file__))
timestamps_file = os.path.join(base_path, "../output/timestamps.txt")
input_video = os.path.join(base_path, "../data/input_video.mp4")
output_dir = os.path.join(base_path, "../output/video_clips")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def time_to_seconds(time_str):
    """Convert HH:MM:SS format to total seconds using datetime"""
    try:
        time_obj = datetime.strptime(time_str, "%H:%M:%S")
        return time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}")

try:
    # Read and validate timestamps
    with open(timestamps_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    if not lines:
        print("❌ Error: Empty timestamps file!")
        exit(1)

    timestamps = []
    for line in lines:
        parts = line.split(" - ")
        if len(parts) != 2:
            print(f"❌ Invalid timestamp format in line: {line}")
            exit(1)
        timestamps.append((parts[0], parts[1]))

    # Process video clips using FFmpeg
    for idx, (start_time, end_time) in enumerate(timestamps, start=1):
        # Generate output filename with zero-padded index
        output_filename = f"clip_{idx:03d}_{start_time.replace(':', '')}.mp4"
        output_path = os.path.join(output_dir, output_filename)

        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-ss", start_time,          # Seek before input for faster processing
            "-to", end_time,            # Use end timestamp instead of duration
            "-i", input_video,
            "-c", "copy",               # Stream copy (no re-encoding)
            "-avoid_negative_ts", "1",  # Handle potential timestamp issues
            "-map", "0",                # Include all streams
            output_path
        ]

        print(f"\n🔹 Processing clip {idx}: {start_time} - {end_time}")
        print(f"   Command: {' '.join(ffmpeg_cmd)}")
        
        result = subprocess.run(
            ffmpeg_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"❌ FFmpeg error for clip {idx}:")
            print(result.stderr)
            exit(1)

        print(f"✅ Successfully created: {output_filename}")

    print("\n🎉 All clips extracted successfully!")

except FileNotFoundError as e:
    print(f"❌ File not found error: {str(e)}")
except ValueError as e:
    print(f"❌ Validation error: {str(e)}")
except Exception as e:
    print(f"❌ Unexpected error: {str(e)}")
