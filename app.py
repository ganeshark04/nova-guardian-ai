import os
import json
import boto3
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# 1. Load Secrets
load_dotenv()

app = Flask(__name__)

# 2. AWS Clients (Using Railway Variables)
bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
rekognition = boto3.client(service_name='rekognition', region_name='us-east-1')

def get_ai_report(text, scan_type):
    prompt = f"""
    Analyze this {scan_type} for scams: "{text}"
    Return ONLY JSON: {{
        "risk": 0-100, 
        "level": "SAFE"|"SUSPICIOUS"|"CRITICAL", 
        "reasons": ["[CATEGORY] short reason"]
    }}
    """
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
    report = get_ai_report(data.get("content"), data.get("type", "text"))
    return jsonify(report)

@app.route("/api/upload", methods=["POST"])
def upload():
    if 'file' not in request.files: return jsonify({"error": "No file"}), 400
    file = request.files['file']
    image_bytes = file.read()
    try:
        # AWS Rekognition OCR
        response = rekognition.detect_text(Image={'Bytes': image_bytes})
        extracted_text = " ".join([d['DetectedText'] for d in response['TextDetections'] if d['Type'] == 'LINE'])
        
        # AI Analysis
        report = get_ai_report(extracted_text, "screenshot")
        report['extracted'] = extracted_text.strip()
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CRITICAL FOR RAILWAY: No debug=True, No Timer, No webbrowser
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
