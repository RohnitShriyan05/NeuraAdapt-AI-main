import os
from flask import Flask
from routes.generateFlash import flashcard_bp 
from routes.transcribe import transcription_bp

app = Flask(__name__)
app.register_blueprint(flashcard_bp)
app.register_blueprint(transcription_bp)

if __name__ == "__main__":
    app.run(debug=True)

    print("📌 Generating Cognitive Overload Graph...")
    os.system("python3 visualization/plot_graph.py")

    print("\n📌 Extracting Overload Timestamps...")
    os.system("python3 video_processing/extract_timestamps.py")

    print("\n📌 Extracting ±5 Min Video Clips...")
    os.system("python3 video_processing/extract_video_clips.py")

    print("\n📌 Extracting Keyframes...")
    os.system("python3 video_processing/extract_keyframes.py")

    print("\n✅ Process Complete!")

