import os
import json
import boto3
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
from dotenv import load_dotenv
import shutil

load_dotenv()
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --- SMART TESSERACT PATH ---
if os.name == 'nt': # If running on Windows (Your PC)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\GAGAN RAO K\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
else: # If running on Linux (Railway)
    # This automatically finds where Railway installed Tesseract
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract")

# AWS Bedrock Client
bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def get_ai_report(text, scan_type):
    prompt = f"Analyze this {scan_type} for scams: '{text}'. Return ONLY JSON: {{'risk': 0-100, 'level': 'SAFE'|'SUSPICIOUS'|'CRITICAL', 'reasons': ['short reason']}}"
    body = json.dumps({"messages": [{"role": "user", "content": [{"text": prompt}]}]})
    try:
        response = bedrock.invoke_model(modelId="amazon.nova-lite-v1:0", body=body)
        res_body = json.loads(response.get('body').read())
        ai_text = res_body['output']['message']['content'][0]['text']
        return json.loads(ai_text.replace("```json", "").replace("```", "").strip())
    except:
        return {"risk": 0, "level": "OFFLINE", "reasons": ["AI Connection Error"]}

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/logo.png")
def logo():
    return send_from_directory(".", "logo.png")

@app.route("/api/scan", methods=["POST"])
def scan():
    data = request.json
    content = data.get("content")
    scan_type = data.get("type", "text")
    report = get_ai_report(content, scan_type)
    return jsonify(report)

@app.route("/api/upload", methods=["POST"])
def upload():
    file = request.files['file']
    path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(path)
    text = pytesseract.image_to_string(Image.open(path).convert('RGB'))
    report = get_ai_report(text, "screenshot")
    report['extracted'] = text.strip()
    os.remove(path)
    return jsonify(report)

@app.route('/logo.png')
def favicon():
    return send_from_directory('.', 'logo.png')

if __name__ == "__main__":
    app.run(port=5000, debug=True)