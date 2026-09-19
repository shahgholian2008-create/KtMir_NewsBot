from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# این کلید رو بعداً توی تنظیمات Render ست می‌کنی
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    model = data.get('model', 'gemini-3.5-flash')
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    # آدرس اصلی Gemini
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        # درخواست به Gemini با IP Render
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def health():
    return "Gemini Proxy is running!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)