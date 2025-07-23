from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle

app = Flask(__name__)

# Load model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_data = np.array([data['sepal_length'], data['sepal_width'], data['petal_length'], data['petal_width']])
    prediction = model.predict([input_data])[0]
    species = ['setosa', 'versicolor', 'virginica'][prediction]
    return jsonify({'prediction': species})

if __name__ == '__main__':
    app.run(debug=True)