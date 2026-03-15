import os
import json
import boto3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# 1. Initialize
load_dotenv()
app = Flask(__name__)
CORS(app) # Fixes the 'flask_cors' error and allows browser access

# 2. AWS Clients
# These use the Keys you added to Railway's 'Variables' tab
bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
rekognition = boto3.client(service_name='rekognition', region_name='us-east-1')

def get_ai_report(text, scan_type):
    """Calls Amazon Nova Lite for expert threat analysis"""
    prompt = f"""
    Act as a Tier-1 Cybersecurity Analyst. 
    Analyze this {scan_type} for scams or phishing: "{text}"

    You MUST return ONLY a JSON object with this exact structure:
    {{
        "risk": (number 0-100),
        "level": "SAFE" | "SUSPICIOUS" | "CRITICAL",
        "reasons": ["[CATEGORY] description (max 10 words)"]
    }}

    Categories to use: [IMPERSONATION], [URGENCY], [LINK_RISK], [THREAT], [SENSITIVE_DATA].
    """

    body = json.dumps({
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "inferenceConfig": { "max_new_tokens": 500, "temperature": 0 }
    })

    try:
        response = bedrock.invoke_model(modelId="amazon.nova-lite-v1:0", body=body)
        res_body = json.loads(response.get('body').read())
        ai_text = res_body['output']['message']['content'][0]['text']
        
        # Strip potential markdown code blocks
        clean_json = ai_text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"AI ERROR: {e}")
        return {
            "risk": 0, 
            "level": "AI_OFFLINE", 
            "reasons": ["[SYSTEM] Error connecting to AWS Bedrock Engine"]
        }

# --- ROUTES ---

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/logo.png")
def favicon():
    return send_from_directory(".", "logo.png")

@app.route("/api/scan", methods=["POST"])
def scan():
    """Handles both Message and URL scans"""
    data = request.json
    content = data.get("content", "")
    scan_type = data.get("type", "text")
    report = get_ai_report(content, scan_type)
    return jsonify(report)

@app.route("/api/upload", methods=["POST"])
def upload():
    """Uses AWS Rekognition to extract text, then Nova Lite to analyze"""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    image_bytes = file.read() # Read image directly into memory
    
    try:
        # 1. Visual OCR using AWS Rekognition
        response = rekognition.detect_text(Image={'Bytes': image_bytes})
        
        extracted_text = ""
        for detection in response['TextDetections']:
            if detection['Type'] == 'LINE':
                extracted_text += detection['DetectedText'] + " "
        
        if not extracted_text.strip():
            return jsonify({
                "risk": 0, "level": "CLEAN", 
                "reasons": ["[SYSTEM] No text detected in image"], 
                "extracted": ""
            })

        # 2. Heuristic Analysis using Nova Lite
        report = get_ai_report(extracted_text, "extracted screenshot text")
        report['extracted'] = extracted_text.strip()
        
        return jsonify(report)

    except Exception as e:
        print(f"OCR ERROR: {e}")
        return jsonify({"error": "AWS OCR Service Failed"}), 500

if __name__ == "__main__":
    # Railway automatically provides the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
