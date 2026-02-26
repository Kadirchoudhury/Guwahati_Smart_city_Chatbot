import pickle
import os

# Get current directory (model folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load saved files
model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")
label_encoder_path = os.path.join(BASE_DIR, "label_encoder.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)

with open(label_encoder_path, "rb") as f:
    label_encoder = pickle.load(f)


def predict_intent(text):
    # Convert text to vector
    text_vector = vectorizer.transform([text])

    # Predict
    prediction = model.predict(text_vector)

    # Convert label back to tag
    tag = label_encoder.inverse_transform(prediction)

    return tag[0]