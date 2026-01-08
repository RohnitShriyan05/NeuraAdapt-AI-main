import os
import uuid
import google.generativeai as genai
from flask import Blueprint, request, send_from_directory, jsonify
from fpdf import FPDF

# Load API key securely from environment variable
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

# Configure Gemini AI
genai.configure(api_key=API_KEY)

# Use the free model
MODEL_NAME = "gemini-1.5-flash-latest"  # Free-tier model

# Get the parent directory of the current file (routes/generateFlash.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set the upload folder in the parent directory
UPLOAD_FOLDER = os.path.join(BASE_DIR, "generated_pdfs")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Define Flask Blueprint (for modular routing)
flashcard_bp = Blueprint("flashcard", __name__)

def clean_text(text):
    """Replace problematic Unicode characters with safe alternatives"""
    replacements = {
        "\u2013": "-",  # En dash
        "\u2014": "--",  # Em dash
        "\u2018": "'", "\u2019": "'",  # Curly single quotes
        "\u201C": '"', "\u201D": '"',  # Curly double quotes
        "\u2026": "...",  # Ellipsis
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.strip()

def generate_questions(title, description):
    """Generates descriptive questions using Gemini AI"""
    prompt = f"Generate 3 detailed questions based on the topic '{title}' with the following description:\n{description}"

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    if hasattr(response, "text") and response.text:
        questions = response.text.strip().split("\n")
        return [clean_text(q) for q in questions if q.strip()]
    
    return ["No questions generated. Please try again."]

def create_pdf(title, description, questions, filename):
    """Creates a PDF containing the generated questions"""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Use built-in font to avoid font errors
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, clean_text(title), ln=True, align="C")

    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, clean_text(description))

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Descriptive Questions:", ln=True)

    pdf.set_font("Arial", size=12)
    for i, question in enumerate(questions, 1):
        pdf.multi_cell(0, 10, f"{i}. {clean_text(question)}")

    pdf.output(filename, "F")

@flashcard_bp.route("/generateFlash", methods=["POST"])
def generate_flashcard():
    """API to generate a flashcard (PDF) with questions"""
    data = request.json
    title = data.get("title")
    description = data.get("description")

    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400

    try:
        questions = generate_questions(title, description)
    except Exception as e:
        return jsonify({"error": f"Failed to generate questions: {str(e)}"}), 500

    filename = f"{uuid.uuid4()}.pdf"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    create_pdf(title, description, questions, filepath)

    return jsonify({"download_url": f"/download/{filename}"})

@flashcard_bp.route("/download/<filename>")
def download_file(filename):
    """API to download the generated PDF"""
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
