from flask import Flask, request, jsonify
from src.DataAnalysis.Data_Analysis import DocumentAnalyzer 
import traceback
from utils.pdf_handler import PDFHandler

app = Flask(__name__)

# Load analyzer once (important for performance)

analyzer = DocumentAnalyzer()

@app.route("/")
def home():
    return {"message": "Document Analyzer API is running"}

@app.route("/analyze", methods=["POST"])
def analyze_document():
    try:
        data = request.get_json()


        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        document_text = data["text"]

        result = analyzer.analyze_document(document_text)

        return jsonify({
            "status": "success",
            "metadata": result
        })

    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500


@app.route("/upload", methods=["POST"])
def upload_pdf():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "Only PDF allowed"}), 400

        # Extract text
        text = PDFHandler.extract_text(file)

        if not text.strip():
            return jsonify({"error": "Could not extract text from PDF"}), 400

        # Analyze
        result = analyzer.analyze_document(text)

        return jsonify({
            "status": "success",
            "metadata": result
        })

    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
