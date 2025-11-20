from flask import Flask, render_template, request
from pathlib import Path
import joblib

# ඔයාගේ helper functions import කරන්න
# (clean_text, get_full_analysis, etc.)
import importlib
get_full_analysis = None
try:
    module = importlib.import_module("your_helper_module")
    get_full_analysis = getattr(module, "get_full_analysis")
except Exception:
    # Fallback minimal implementation to avoid import errors during development/testing.
    def get_full_analysis(text):
        # Simple placeholder analysis — replace with your real implementation/module.
        return {
            "length": len(text),
            "preview": text[:200],
            "words": len(text.split())
        }

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html", input_text="", result="")

@app.route("/predict", methods=["POST"])
def predict():
    text = request.form.get("text_input", "").strip()

    if not text:
        return render_template("index.html", input_text="", result="⚠️ Please enter text!")

    try:
        # Use your structured analysis function
        analysis = get_full_analysis(text)

        # Format HTML safe output
        formatted_result = ""
        for k, v in analysis.items():
            formatted_result += f"- {k}: {v}<br>"

    except Exception as e:
        formatted_result = f"Prediction error: {e}"

    return render_template("index.html", input_text=text, result=formatted_result)

if __name__ == "__main__":
    app.run(debug=True)
