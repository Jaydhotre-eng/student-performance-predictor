## Student Performance Predictor

A simple Flask web app that uses a machine-learning model to predict whether a student is likely to **Pass** or **Fail** based on:
- Study hours per day
- Marks (%)
- Sleep hours per day

The UI is a single-page form with a styled card interface and a result display.

---

## 1. Project Structure

- `app.py` – Flask application and prediction endpoint
- `templates/index.html` – Frontend UI (form + result)
- `model.pkl` – Trained ML model (must be placed in the `Student_Pass` folder)
- `featured_data.csv` – Feature-engineered dataset used to train/evaluate the model
- `requirments.txt` – Python dependencies (Flask, NumPy, etc.)

---

## 2. Prerequisites

- **Python** 3.8+ installed
- **pip** (Python package manager)

Optional but recommended:
- A virtual environment tool such as `venv`

---

## 3. Environment Setup

From the `Student_Pass` folder:

```bash
# (Optional) create and activate virtual environment
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirments.txt
```

> Note: Make sure `model.pkl` is inside the `Student_Pass` directory at the same level as `app.py`.

---

## 4. Running the App

From the `Student_Pass` folder (with the virtual environment activated, if you created one):

```bash
python app.py
```

By default, Flask will start in debug mode on:

- `http://127.0.0.1:5000/` (or `http://localhost:5000/`)

Open that URL in your browser to use the app.

---

## 5. Project Workflow (End to End)

High-level flow of the whole project:

1. **Data collection**  
   - Raw data is stored in CSV files such as `data_with_nulls.csv`.

2. **Data cleaning**  
   - Missing or inconsistent values are cleaned and saved into `cleaned_data.csv`.

3. **Feature engineering**  
   - Additional columns such as `study_efficiency`, `sleep_category`, `sleep_category_encoded`, and `study_sleep_ratio` are computed.
   - The processed dataset is saved as `featured_data.csv` and is used for training and evaluation.

4. **Model training**  
   - The notebook `Fail_Student_Predition_model.ipynb` loads `featured_data.csv`, explores the data, and trains a classification model to predict **Pass** vs **Fail**.
   - The trained model is exported to `model.pkl` and placed in the `Student_Pass` folder next to `app.py`.

5. **Serving the model (backend)**  
   - `app.py` is a Flask app that loads `model.pkl` at startup.
   - It exposes:
     - `/` – renders the HTML UI (`templates/index.html`)
     - `/predict` – accepts form data (POST), prepares features, gets a prediction from the model, and passes the result back to the template.

6. **User interaction (frontend)**  
   - `templates/index.html` shows a single-page UI with a form.
   - The user enters **Study hours**, **Marks (%)**, and **Sleep hours**, then clicks **Predict Result**.
   - The page is re-rendered with a **Pass** or **Fail** badge based on the model’s prediction.

---

## 6. How the Inputs Work

The form asks for:

- **Study hours per day** – Average hours the student studies per day (e.g. `3.5`)
- **Marks (%)** – Percentage score (0–100, e.g. `72`)
- **Sleep hours per day** – Average hours of sleep per night (e.g. `7.5`)

Inside `app.py`, the app computes:

- Study efficiency = `marks / study_hours` (if study_hours > 0)
- Study–sleep ratio = `study_hours / sleep_hours` (if sleep_hours > 0)
- Sleep category:
  - `< 6` hours → Low sleep
  - `6–8` hours → Optimal sleep
  - `>= 9` hours → High sleep

Those features are passed to the trained model, which predicts **Pass** or **Fail**.

---

## 7. Example Inputs – Fail Cases

These examples match patterns that were labeled **Fail** in the training data (`featured_data.csv`). If you enter values close to these, the model is very likely to return **Fail** (though not guaranteed, since ML models use decision boundaries, not strict rules).

### Fail Example 1
- **Study hours**: `2`
- **Marks (%)**: `33`
- **Sleep hours**: `8`

### Fail Example 2
- **Study hours**: `4`
- **Marks (%)**: `34`
- **Sleep hours**: `5`

### Fail Example 3
- **Study hours**: `8`
- **Marks (%)**: `35`
- **Sleep hours**: `4`

### Fail Example 4
- **Study hours**: `7`
- **Marks (%)**: `32`
- **Sleep hours**: `6.41`

These all combine **low marks (low 30s)** with patterns of study and sleep that the model has learned to associate with failing.

---

## 8. Example Inputs – Pass Cases

Here are some example inputs likely to produce a **Pass** prediction, based on rows labeled Pass in the dataset.

### Pass Example 1
- **Study hours**: `3`
- **Marks (%)**: `94`
- **Sleep hours**: `9`

### Pass Example 2
- **Study hours**: `5`
- **Marks (%)**: `72`
- **Sleep hours**: `6`

### Pass Example 3
- **Study hours**: `1`
- **Marks (%)**: `87`
- **Sleep hours**: `9`

### Pass Example 4
- **Study hours**: `4`
- **Marks (%)**: `64`
- **Sleep hours**: `8`

---

## 9. Interpretation Notes

- The model was trained on relatively small, synthetic-looking data; treat predictions as **educational/demo only**, not official academic decisions.
- In the dataset, students with marks **≈ 40% and below** often appear as **Fail**, while marks **above ~40%** are usually **Pass**, especially if study efficiency is reasonable.
- Sleep helps the model a bit, but **marks and study efficiency** are the strongest signals.

