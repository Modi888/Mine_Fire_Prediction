from flask import Flask, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS  # For enabling CORS support


# Load the models and scaler
risk_model = pickle.load(open("svm_risk_model.pkl", "rb"))
fire_model = pickle.load(open("logistic_fire_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

app = Flask(__name__)
CORS(app)  # Enable CORS


@app.route("/predict", methods=["POST"])
def predict():
    # Parse the incoming JSON payload
    data = request.json
    features = [
        data["Location"],
        data["Temperature"],
        data["ResidualGas"],
        data["WindSpeed"],
        data["O2Concentration"],
        data["COConcentration"]
    ]

    # Normalize the input data
    features_scaled = scaler.transform([features])

    # Predict the risk level
    risk_prediction = risk_model.predict(features_scaled)[0]

    # Predict the fire probability
    fire_probability = fire_model.predict_proba(features_scaled)[0][1]  # Probability of fire (class 1)

    return jsonify({
        "risk_level": int(risk_prediction),
        "fire_probability": round(fire_probability * 100, 2)  # Convert to percentage
    })

if __name__ == "__main__":
    app.run(debug=True)
