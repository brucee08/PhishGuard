
from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import os

from detector.feature_extractor import extract_features
from detector.risk_engine import calculate_risk, generate_explanation


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)


# =========================================================
# LOAD MODEL
# =========================================================

MODEL_PATH = os.path.join(
    "model",
    "phishing_model.pkl"
)

try:
    model = joblib.load(MODEL_PATH)
    print("PhishGuard model loaded successfully.")

except Exception as e:
    model = None
    print("Error loading model:", e)


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# SCAN
# =========================================================

@app.route("/scan")
def scan():
    return render_template("scan.html")


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# =========================================================
# HISTORY
# =========================================================

@app.route("/history")
def history():
    return render_template("history.html")


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
def about():
    return render_template("about.html")


# =========================================================
# ANALYZE URL
# =========================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    # -----------------------------------------------------
    # Check whether model is loaded
    # -----------------------------------------------------

    if model is None:
        return jsonify({
            "success": False,
            "error": "Phishing model could not be loaded."
        }), 500

    try:

        # -------------------------------------------------
        # Check request content
        # -------------------------------------------------

        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Request must contain JSON data."
            }), 400


        # -------------------------------------------------
        # Get JSON data safely
        # -------------------------------------------------

        data = request.get_json(silent=True)


        if data is None:
            return jsonify({
                "success": False,
                "error": "Invalid JSON data received."
            }), 400


        # -------------------------------------------------
        # Get URL
        # -------------------------------------------------

        url = data.get("url", "")


        if not isinstance(url, str):
            return jsonify({
                "success": False,
                "error": "URL must be a text value."
            }), 400


        url = url.strip()


        # -------------------------------------------------
        # Check empty URL
        # -------------------------------------------------

        if not url:
            return jsonify({
                "success": False,
                "error": "Please enter a URL."
            }), 400


        # -------------------------------------------------
        # Extract Features
        # -------------------------------------------------

        features = extract_features(url)


        # -------------------------------------------------
        # Convert features to DataFrame
        # -------------------------------------------------

        features_df = pd.DataFrame([features])


        # -------------------------------------------------
        # Machine Learning Prediction
        # -------------------------------------------------

        prediction = model.predict(features_df)[0]

        prediction_text = str(prediction).lower()


        # -------------------------------------------------
        # Prediction Probability
        # -------------------------------------------------

        probability = None


        if hasattr(model, "predict_proba"):

            probabilities = model.predict_proba(
                features_df
            )[0]

            classes = list(model.classes_)


            if "phishing" in classes:

                phishing_index = classes.index(
                    "phishing"
                )

                probability = (
                    float(
                        probabilities[phishing_index]
                    ) * 100
                )

            else:

                probability = (
                    float(
                        max(probabilities)
                    ) * 100
                )


        # -------------------------------------------------
        # Classification Result
        # -------------------------------------------------

        if prediction_text == "phishing":

            result = "Phishing"
            status = "danger"

        else:

            result = "Legitimate"
            status = "safe"


        # -------------------------------------------------
        # Calculate Risk
        # -------------------------------------------------

        risk_score = calculate_risk(
            features,
            prediction
        )


        # -------------------------------------------------
        # Generate Explanation
        # -------------------------------------------------

        explanation = generate_explanation(
            features,
            prediction,
            risk_score
        )


        # -------------------------------------------------
        # Send Response
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "url": url,

            "prediction": result,

            "status": status,

            "probability": (
                round(probability, 2)
                if probability is not None
                else None
            ),

            "score": risk_score,

            "risk_score": risk_score,

            "explanation": explanation,

            "features": features

        })


    # =====================================================
    # ERROR
    # =====================================================

    except Exception as e:

        print(
            "Error while analyzing URL:",
            repr(e)
        )

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "running",

        "model_loaded":
            model is not None

    })


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("          PHISHGUARD SERVER")
    print("======================================")
    print("URL: http://127.0.0.1:5000")
    print("======================================")
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
