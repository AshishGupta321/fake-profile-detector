from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model
model = joblib.load("models/model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # Convert input to dataframe
    df = pd.DataFrame([data])

    # Prediction
    prediction = model.predict(df)[0]

    return jsonify({
        "prediction": int(prediction)
    })

if __name__ == "__main__":
    app.run(debug=True)