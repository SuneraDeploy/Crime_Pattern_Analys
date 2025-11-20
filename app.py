# ...existing code...
import warnings
try:
    from flask import Flask, render_template, request
    import joblib
    import numpy as np
    import os
    import traceback
    # suppress sklearn version mismatch warnings (optional)
    from sklearn.base import InconsistentVersionWarning
    warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
except ModuleNotFoundError as e:
    print(f"Missing package: {e.name}")
    print("Install with:")
    print(f"    py -3 -m pip install {e.name}")
    print("Or install all requirements:")
    print("    py -3 -m pip install -r requirements.txt")
    raise
# ...existing code...
app = Flask(__name__)

# ...existing code...
# safer model loading using absolute path
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
try:
    model = joblib.load(model_path)
except Exception as e:
    model = None
    print(f"Failed to load model from {model_path}: {e}")
    traceback.print_exc()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return render_template("index.html", result="Model not loaded")

    # collect and validate form inputs
    raw_vals = [v.strip() for v in request.form.values() if v is not None]
    if not raw_vals:
        return render_template("index.html", result="No input provided")

    try:
        features = [float(x) for x in raw_vals]
    except ValueError:
        return render_template("index.html", result="Invalid input: ensure all fields are numbers")

    final = np.array(features).reshape(1, -1)
    try:
        prediction = model.predict(final)
        out = prediction[0]
    except Exception as e:
        return render_template("index.html", result=f"Prediction error: {e}")

    return render_template("index.html", result=out)

if __name__ == "__main__":
    app.run(debug=True)
# ...existing code...