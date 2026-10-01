from flask import Flask, request, jsonify
from flask_cors import CORS
from services.password_analyzer import PasswordAnalyzer
from services.password_generator import PasswordGenerator
from models.database import init_db, log_analysis, get_dashboard_stats

app = Flask(__name__)
CORS(app)

init_db()
analyzer = PasswordAnalyzer("data/common_passwords.txt")

@app.route("/api/analyze", methods=["POST"])
def analyze_password():
    data = request.get_json() or {}
    password = data.get("password", "")
    context = data.get("context", {})

    if not isinstance(password, str):
        return jsonify({"error": "Invalid input type"}), 400

    result = analyzer.analyze(password, context)

    # Log safe aggregate metadata only (Never log the password)
    log_analysis(
        score=result["score"],
        classification=result["classification"],
        length=result["metrics"]["length"],
        unique_ratio=result["metrics"]["unique_character_ratio"],
        weakness_count=len(result["findings"])
    )

    return jsonify(result)

@app.route("/api/generate", methods=["POST"])
def generate_password():
    data = request.get_json() or {}
    length = int(data.get("length", 16))
    pwd = PasswordGenerator.generate(length=length)
    return jsonify({"generated_password": pwd})

@app.route("/api/dashboard/stats", methods=["GET"])
def dashboard_stats():
    stats = get_dashboard_stats()
    return jsonify(stats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
