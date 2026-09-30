
import joblib
import pandas as pd
import os

from detector.feature_extractor import extract_features


# Load model
MODEL_PATH = os.path.join(
    "model",
    "phishing_model.pkl"
)

print("Loading model...")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully!")
print("Model type:", type(model))

print()


# Test URL
url = "https://google.com"


# Extract features
features = extract_features(url)

print("Extracted features:")
print(features)

print()


# Convert to DataFrame
features_df = pd.DataFrame([features])

print("DataFrame:")
print(features_df)

print()


# Show model information
if hasattr(model, "feature_names_in_"):

    print("Model expects these features:")

    print(model.feature_names_in_)

    print()


# Prediction
prediction = model.predict(features_df)[0]

print("Prediction:")
print(prediction)

print()


# Probability
if hasattr(model, "predict_proba"):

    probabilities = model.predict_proba(
        features_df
    )[0]

    print("Probabilities:")

    print(probabilities)

    print()

    print("Classes:")

    print(model.classes_)

print()

print("================================")
print("MODEL TEST COMPLETED SUCCESSFULLY")
print("================================")
