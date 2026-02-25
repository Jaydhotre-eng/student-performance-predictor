from flask import Flask, request, render_template
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load model from the same directory as this file
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"model.pkl not found at {MODEL_PATH}. Put model.pkl in the Student_Pass folder.")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    study_hours = float(request.form["study_hours"])
    sleep_hours = float(request.form["sleep_hours"])
    # read marks from form to compute derived features (default 0 if missing)
    marks = float(request.form.get("marks", 0))

    # compute derived features expected by the model
    # study_efficiency was computed as marks / study_hours in training
    study_efficiency = marks / study_hours if study_hours != 0 else 0.0
    # study_sleep_ratio is study_hours divided by sleep_hours
    study_sleep_ratio = study_hours / sleep_hours if sleep_hours != 0 else 0.0
    # encode sleep category similarly to training: Low=0, Optimal=1, High=2
    if sleep_hours >= 9:
        sleep_category_encoded = 2
    elif 6 <= sleep_hours <= 8:
        sleep_category_encoded = 1
    else:
        sleep_category_encoded = 0

    # arrange features in the same order the model was trained on
    features = np.array([[study_hours, sleep_hours, study_efficiency, study_sleep_ratio, sleep_category_encoded]])
    prediction = model.predict(features)

    result = "Pass" if prediction[0] == 1 else "Fail"

    return render_template("index.html", prediction_text=f"Result: {result}")

if __name__ == "__main__":
    app.run(debug=True)