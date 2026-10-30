# 🛡️ AI Scam Detector

### Intelligent Detection of Suspicious Messages and Digital Fraud

## 📌 Project Overview

AI Scam Detector is an AI-powered web application designed to analyze suspicious messages and identify potential digital scams.

It uses **Ollama and Gemma 3:1B** to examine SMS, emails, and other text messages, assess their risk levels, identify warning signs, and provide safety recommendations.

The main goal of this project is to improve digital awareness and help users protect themselves from online fraud.

## 🎯 Objectives

- Detect potentially suspicious messages.
- Identify phishing and fraudulent content.
- Classify messages based on risk levels.
- Highlight common scam warning signs.
- Provide safety recommendations.
- Promote awareness about digital security.

## ✨ Features

- **AI-Based Message Analysis** – Analyze suspicious messages using an AI model.
- **Risk Assessment** – Classify messages as High, Medium, or Low Concern.
- **Scam Category Detection** – Identify potential phishing and other scam categories.
- **Warning Sign Identification** – Highlight suspicious links, OTP requests, urgency, and other red flags.
- **Safety Recommendations** – Provide suggestions to avoid digital fraud.
- **Analysis History** – View previously analyzed messages during the session.
- **Dashboard** – Display analysis statistics and risk-level counts.
- **Professional User Interface** – Simple and user-friendly Streamlit interface.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| Streamlit | Web Application |
| Ollama | Local AI Model Runtime |
| Gemma 3:1B | AI Message Analysis |
| Requests | API Communication |

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the Project Folder

```bash
cd AI-Scam-Detector
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

### 4. Install and Download Ollama Model

Install Ollama from:

https://ollama.com/

Download the Gemma model:

```bash
ollama pull gemma3:1b
```

### 5. Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## 📂 Project Structure

```text
AI-Scam-Detector/
│
├── app.py
├── requirements.txt
└── README.md
```

## 🔍 How It Works

1. Open the AI Scam Detector application.
2. Enter or paste a suspicious SMS or email.
3. Click the Analyze Message button.
4. The application sends the message to the Gemma 3:1B model through Ollama.
5. The AI analyzes the message and identifies potential warning signs.
6. The application displays the risk assessment, scam category, and safety recommendations.

## 📊 Risk Classification

| Risk Level | Description |
|---|---|
| 🔴 High Concern | Message contains strong indicators of a potential scam. |
| 🟠 Medium Concern | Message contains some suspicious characteristics. |
| 🟢 Low Concern | No significant scam indicators were identified. |

## 💡 Example Use Cases

- Suspicious bank messages
- Fake job recruitment messages
- Lottery and prize scams
- Phishing messages
- Messages requesting OTP or personal information

## 🔐 Safety Note

AI-generated results are advisory and may not always be accurate. The application cannot independently verify the identity of a sender, website, or financial institution.

Always verify suspicious messages through official channels. Never share passwords, banking details, or OTPs.

## 🚀 Future Enhancements

- Image-based scam detection.
- URL safety analysis.
- Email scam detection.
- Multilingual message analysis.
- Improved detection accuracy.
- Downloadable analysis reports.

## 👩‍💻 Developed By

**Keerthika M.**

B.Sc. Computer Science with Artificial Intelligence
