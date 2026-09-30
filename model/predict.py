import joblib
import pandas as pd

from detector.feature_extractor import extract_features


model = joblib.load(
    "model/phishing_model.pkl"
)


url = "https://gift-mymaxis.biz.id/vip"

features = extract_features(url)

X = pd.DataFrame([features])

prediction = model.predict(X)

print("Prediction:", prediction[0])
