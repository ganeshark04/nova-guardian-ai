import os
import json
import boto3
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- AWS CLIENTS ---
# These automatically use the keys from your Railway Variables or .env
bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
rekognition = boto3.client(service_name='rekognition', region_name='us-east-1')

def get_ai_report(text, scan_type):
    """Sends text to Amazon Nova Lite with professional tagging"""
    prompt = f"""
    Analyze this {scan_type} for scams/phishing: "{text}"
    Return ONLY JSON: {{
        "risk": 0-100, 
        "level": "SAFE"|"SUSPICIOUS"|"CRITICAL", 
        "reasons": ["[CATEGORY] reason (max 10 words)"]
    }}
    Tags: [IMPERSONATION], [URGENCY], [LINK_RISK], [THREAT], [SENSITIVE_DATA].
    """
    body = json.dumps({"messages": [{"role": "user", "content": [{"text": prompt}]}]})
    try:
        response = bedrock.invoke_model(modelId="amazon.nova-lite-v1:0", body=body)
        res_body = json.loads(response.get('body').read())
        ai_text = res_body['output']['message']['content'][0]['text']
        return json.loads(ai_text.replace("```json", "").replace("```", "").strip())
    except:
        return {"risk": 0, "level": "OFFLINE", "reasons": ["[SYSTEM] AI Connection Error"]}

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/logo.png")
def logo():
    return send_from_directory(".", "logo.png")

@app.route("/api/scan", methods=["POST"])
def scan():
    data = request.json
    report = get_ai_report(data.get("content"), data.get("type", "text"))
    return jsonify(report)

@app.route("/api/upload", methods=["POST"])
def upload():
    """Uses AWS Rekognition to extract text from image"""
    if 'file' not in request.files: return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    image_bytes = file.read() # Get image data
    
    try:
        # --- 1. AWS REKOGNITION (OCR) ---
        response = rekognition.detect_text(Image={'Bytes': image_bytes})
        
        extracted_text = ""
        for item in response['TextDetections']:
            if item['Type'] == 'LINE':
                extracted_text += item['DetectedText'] + " "
        
        if not extracted_text.strip():
            extracted_text = "No text detected in image."

        # --- 2. NOVA LITE (AI ANALYSIS) ---
        report = get_ai_report(extracted_text, "extracted screenshot text")
        report['extracted'] = extracted_text.strip()
        
        return jsonify(report)
        
    except Exception as e:
        print(f"AWS Error: {e}")
        return jsonify({"error": "AWS Service Error"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)