from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received:", data)

        if data is None:
            return jsonify({"error": "No data received"}), 400

        followers = data.get('followers', 0)
        following = data.get('following', 0)
        tweets = data.get('tweets', 0)
        account_age = data.get('account_age', 1)

        # Simple logic
        if followers < 50:
            result = "Bot"
        else:
            result = "Real"

        return jsonify({
            "prediction": result,
            "confidence": 0.85
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Starting API...")
    app.run(debug=True)