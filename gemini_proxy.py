from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# API Keys از Environment Variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


@app.route('/generate', methods=['POST'])
def generate():
    """Gemini Proxy (قدیمی)"""
    data = request.json
    model = data.get('model', 'gemini-3.5-flash')
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/groq', methods=['POST'])
def groq_generate():
    """Groq Proxy (جدید)"""
    data = request.json
    prompt = data.get('prompt')
    model = data.get('model', 'llama-3.3-70b-versatile')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def health():
    return "Proxy is running!"


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
