import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyCUIXkFyJ7sIQ_kEZ3ivxtxQeilRuqLpKY"))

# Initialize Gemini model
model = genai.GenerativeModel('models/gemini-1.5-flash')  # Change model name if needed

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    try:
        response = model.generate_content(prompt)
        output = response.text
        return jsonify({"response": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)