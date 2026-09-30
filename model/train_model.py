import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

from detector.feature_extractor import extract_features


# Load dataset
df = pd.read_csv("data/phishing_dataset.csv")

print("Dataset loaded!")
print("Number of URLs:", len(df))


# Convert URLs into features
X = df["url"].apply(extract_features)

# Convert feature dictionaries into a DataFrame
X = pd.DataFrame(X.tolist())

# Get labels
y = df["label"]


# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Create the Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Train the model
model.fit(X_train, y_train)

print("Model training completed!")


# Test the model
predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Accuracy:", accuracy)


# Save the trained model
joblib.dump(
    model,
    "model/phishing_model.pkl"
)

print("Model saved successfully!")