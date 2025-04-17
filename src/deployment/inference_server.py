
import pandas as pd
import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the model
model = joblib.load('/app/model/model.joblib')  # Adjust path if needed

@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
     it healthy if we can load the model successfully."""
    health = model is not None  # Check if the model is loaded
    status = 200 if health else 404
    return jsonify({}), status

@app.route('/invocations', methods=['POST'])
def predict():
    """Predict using the model for the given data."""
    try:
        # Get data from the POST request
        data = request.get_json()
        input_data = pd.DataFrame(data['instances'])  # Assuming input is a list of dicts

        # Make predictions
        predictions = model.predict(input_data).tolist()

        # Return predictions as JSON
        return jsonify({'predictions': predictions})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
