# 🛡️ Nova Guardian AI

**Nova Guardian AI** is an AI-powered cybersecurity intelligence tool designed to detect **scams, phishing messages, and malicious links** from text or screenshots.

The system combines **OCR (Optical Character Recognition)** and **AI reasoning using Amazon Bedrock Nova models** to analyze suspicious content and generate a **risk score with threat classification**.

Nova Guardian AI helps users quickly determine whether a message, link, or screenshot is **SAFE, SUSPICIOUS, or CRITICAL**.

---

# 🚀 Features

🔍 **AI Scam Detection**
Analyze suspicious messages, emails, and URLs using AI.

🖼 **Screenshot Analysis**
Upload screenshots of scam messages or phishing pages.

🧠 **AI Risk Assessment**
Uses **Amazon Nova AI** to analyze content context and intent.

📊 **Risk Score Visualization**
Displays a risk score from **0–100%**.

🧾 **Threat Explanation**
AI provides clear reasons explaining why content is suspicious.

🖥 **Modern Cybersecurity Dashboard**
Clean dark-mode UI built with **Tailwind CSS**.

---

# 🧠 Technology Architecture

Nova Guardian AI uses a modern **AI-powered cybersecurity tech stack** designed for intelligent scam detection.

---

## 1️⃣ AI & Machine Learning Layer

### Amazon Bedrock

The system uses **Amazon Bedrock**, a serverless AI platform that allows the application to access powerful foundation models without hosting them locally.

This architecture enables scalable AI analysis while keeping the system lightweight.

### Amazon Nova Lite

**Amazon Nova Lite** is the Large Language Model (LLM) used for scam detection.

The model performs **heuristic reasoning**, meaning it analyzes:

* Intent of a message
* Context of communication
* Social engineering patterns
* Suspicious links or payment requests

Instead of just matching keywords, the model behaves like a **human cybersecurity analyst**.

### Tesseract OCR

Screenshots are processed using **Tesseract OCR**, which converts image pixels into machine-readable text.

This allows Nova Guardian AI to analyze scam screenshots from:

* WhatsApp messages
* Email phishing attempts
* Telegram scams
* Social media messages
* Fake websites

---

# 🖥 Backend Architecture

### Python 3

Python is used as the core programming language due to its strong ecosystem for AI, automation, and cloud integration.

### Flask

Flask is used as a **lightweight web framework** that builds the backend REST API.

It handles:

* Message scanning requests
* Screenshot uploads
* OCR processing
* AI communication
* Returning security reports

### Boto3

Boto3 is the **official AWS SDK for Python**.

It allows the backend to securely communicate with **Amazon Bedrock AI models**.

### Pillow (PIL)

Pillow is used for **image preprocessing**, preparing screenshots before OCR scanning.

### Python-Dotenv

Sensitive credentials like AWS keys are stored securely in a **.env environment file**, following security best practices.

---

# 🎨 Frontend Architecture

### HTML5 & JavaScript (ES6)

The frontend interface is built with modern JavaScript.

It uses **asynchronous API calls (AJAX)** so scanning results appear instantly without refreshing the page.

### Tailwind CSS

Tailwind CSS provides a **modern utility-first design system** used to create the dark cybersecurity dashboard.

The design follows a **minimalist zinc-themed interface** inspired by modern security tools.

### FontAwesome

FontAwesome icons provide visual indicators such as:

* Security shields
* Threat alerts
* Scan indicators
* System activity icons

### Google Fonts

**Inter**
Used for clean, readable UI text.

**JetBrains Mono**
Used for terminal-style logs to create a cybersecurity dashboard feel.

---

# ⚙️ System Workflow

1️⃣ User enters suspicious **text or link**

2️⃣ Or uploads a **screenshot**

3️⃣ Screenshot text is extracted using **Tesseract OCR**

4️⃣ Extracted content is sent to **Amazon Bedrock Nova AI**

5️⃣ AI analyzes the message for scam indicators

6️⃣ A structured **risk report** is returned

Example AI response:

```json
{
  "risk": 72,
  "level": "SUSPICIOUS",
  "reasons": [
    "Urgent payment request",
    "Suspicious URL detected"
  ]
}
```

7️⃣ The dashboard displays:

* Risk percentage
* Threat classification
* AI explanation
* Extracted message

---

# 🛡️ Risk Classification

| Risk Score | Threat Level |
| ---------- | ------------ |
| 0 – 40     | SAFE         |
| 41 – 70    | SUSPICIOUS   |
| 71 – 100   | CRITICAL     |

---

# 📂 Project Structure

```
nova-guardian-ai
│
├── app.py
├── index.html
├── logo.png
├── uploads/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/ganeshark04/nova-guardian-ai.git

cd nova-guardian-ai
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Install Tesseract OCR

Download from:

https://github.com/tesseract-ocr/tesseract

Example Windows installation path:

```
C:\Users\USERNAME\AppData\Local\Programs\Tesseract-OCR\tesseract.exe
```

---

## 4️⃣ Create Environment Variables

Create a `.env` file in the project folder:

```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
```

⚠️ Never upload `.env` to GitHub.

---

## 5️⃣ Run the Application

```bash
python app.py
```

Open the app in your browser:

```
http://localhost:5000
```

---

# 🔍 Example Use Cases

• Detect phishing messages
• Analyze suspicious links
• Verify scam screenshots
• Identify fraud attempts in chat messages
• Cybersecurity awareness training

---

# 🌍 Future Improvements

* URL reputation scanning
* VirusTotal integration
* Browser extension
* WhatsApp / Telegram bot
* Real-time phishing detection
* Mobile application

---

# 👨‍💻 Author

**Gagan Rao K**
B.E – Artificial Intelligence & Machine Learning

Developer | AI Enthusiast | Problem Solver

GitHub:
https://github.com/ganeshark04

---

# 📜 License

This project is licensed under the **MIT License**.
