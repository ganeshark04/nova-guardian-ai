import os
import json
import boto3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load keys
load_dotenv()

app = Flask(__name__)
CORS(app) # Allows the browser to talk to the server safely

# AWS Clients
bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
rekognition = boto3.client(service_name='rekognition', region_name='us-east-1')

def get_ai_report(text, scan_type):
    prompt = f"Analyze this {scan_type} for scams: '{text}'. Return ONLY JSON: {{'risk': 0-100, 'level': 'SAFE'|'SUSPICIOUS'|'CRITICAL', 'reasons': ['[TAG] reason']}}"
    body = json.dumps({"messages": [{"role": "user", "content": [{"text": prompt}]}]})
    try:
        response = bedrock.invoke_model(modelId="amazon.nova-lite-v1:0", body=body)
        res_body = json.loads(response.get('body').read())
        ai_text = res_body['output']['message']['content'][0]['text']
        return json.loads(ai_text.replace("```json", "").replace("```", "").strip())
    except:
        return {"risk": 50, "level": "AI_OFFLINE", "reasons": ["Check AWS Bedrock Model Access"]}

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/logo.png")
def logo():
    return send_from_directory(".", "logo.png")

@app.route("/api/scan", methods=["POST"])
def scan():
    data = request.json
    return jsonify(get_ai_report(data.get("content"), "text"))

@app.route("/api/upload", methods=["POST"])
def upload():
    file = request.files['file']
    image_bytes = file.read()
    try:
        # Use AWS Rekognition for Vision (Works on any platform)
        response = rekognition.detect_text(Image={'Bytes': image_bytes})
        extracted = " ".join([d['DetectedText'] for d in response['TextDetections'] if d['Type'] == 'LINE'])
        report = get_ai_report(extracted, "screenshot")
        report['extracted'] = extracted
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Get port from the cloud provider
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
