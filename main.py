from flask import Flask, jsonify
from flask_cors import CORS

from db import init_db
from routes.analyze import analysis_bp
from routes.generateFlash import flashcard_bp
from routes.transcribe import transcription_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(flashcard_bp)
app.register_blueprint(transcription_bp)
app.register_blueprint(analysis_bp)


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})


init_db()


if __name__ == "__main__":
    app.run(debug=True)

