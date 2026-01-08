import cv2
import os

# Get absolute paths
script_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.abspath(os.path.join(script_dir, "../output/video_clips"))
output_dir = os.path.abspath(os.path.join(script_dir, "../output/keyframes"))

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

try:
    video_files = [f for f in os.listdir(input_dir) if f.endswith(".mp4")]
    
    if not video_files:
        print("❌ No video clips found!")
        exit()

    for video_file in video_files:
        video_path = os.path.join(input_dir, video_file)
        cap = cv2.VideoCapture(video_path)
        count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if count % 30 == 0:  # Extract every 30th frame
                frame_filename = f"{os.path.splitext(video_file)[0]}_frame{count}.jpg"
                frame_path = os.path.join(output_dir, frame_filename)
                cv2.imwrite(frame_path, frame)
            
            count += 1
        
        cap.release()
    
    print("✅ Keyframes extracted and saved in", output_dir)

except Exception as e:
    print(f"❌ Unexpected Error: {e}")