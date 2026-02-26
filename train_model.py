import pandas as pd
import joblib
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Training dataset
data = {
    "text": [
        "Find hospital",
        "Show hospital list",
        "Nearest hospital",
        "Government office",
        "Show govt office",
        "Tourist place",
        "Best tourist place",
        "Electricity office",
        "Water supply office"
    ],
    "intent": [
        "find_hospital",
        "find_hospital",
        "find_hospital",
        "find_govt_office",
        "find_govt_office",
        "find_tourist_place",
        "find_tourist_place",
        "find_utility",
        "find_utility"
    ]
}

df = pd.DataFrame(data)

# Vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["text"])

# Label Encoding
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["intent"])

# Model Training
model = LogisticRegression()
model.fit(X, y)

# Create model folder if not exists
os.makedirs("model", exist_ok=True)

# Save files
joblib.dump(model, "model/model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")
joblib.dump(label_encoder, "model/label_encoder.pkl")

print("✅ Model created successfully inside 'model' folder.")