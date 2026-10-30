
import streamlit as st
import requests
import json
import re
from datetime import datetime

# PAGE CONFIGURATION
st.set_page_config(
    page_title="AI Scam Detector",
    page_icon="🛡️",
    layout="wide"
)

# CONFIGURATION
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:1b"

# SESSION STATE
if "history" not in st.session_state:
    st.session_state.history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# PROFESSIONAL CSS
st.markdown("""
<style>

.stApp {
    background-color: #F4F7FC;
}

.stApp p,
.stApp span,
.stApp li,
.stApp label,
.stApp div {
    color: #111111;
}

h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
    font-weight: 800 !important;
}

p, li, label {
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #000000 !important;
    font-weight: 800 !important;
}

[data-testid="stMetricLabel"] {
    color: #111111 !important;
    font-weight: 700 !important;
}

.stTextArea textarea {
    color: #000000 !important;
    background-color: #FFFFFF !important;
    font-weight: 600 !important;
}

.stButton button {
    background-color: #173B68;
    color: #FFFFFF !important;
    border-radius: 8px;
    font-weight: 700;
    border: none;
    padding: 10px 20px;
}

.stButton button p {
    color: #FFFFFF !important;
}

.stButton button:hover {
    background-color: #24558D;
}

div[data-testid="stAlert"] p {
    color: #111111 !important;
}

</style>
""", unsafe_allow_html=True)


# AI ANALYSIS FUNCTION
def analyze_message(message):

    prompt = f"""
You are an expert digital scam detection assistant.

Analyze the following message and return ONLY valid JSON.

Message:
{message}

Use this exact JSON structure:

{{
    "risk_level": "High Concern",
    "scam_category": "Phishing",
    "summary": "Explain the message briefly.",
    "warning_signs": [
        "Warning sign 1",
        "Warning sign 2"
    ],
    "recommendations": [
        "Safety recommendation 1",
        "Safety recommendation 2"
    ],
    "limitations": "Explain what cannot be verified."
}}

Rules:
- risk_level must be High Concern, Medium Concern or Low Concern.
- scam_category should identify the likely message type.
- Give clear and simple explanations.
- Never assume a message is safe only because it looks professional.
- Do not invent facts.
- Return JSON only.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.2
            }
        },
        timeout=300
    )

    response.raise_for_status()

    result = response.json()
    content = result["message"]["content"]

    # Extract JSON
    match = re.search(r"\{.*\}", content, re.DOTALL)

    if not match:
        raise ValueError("AI did not return valid JSON.")

    data = json.loads(match.group())

    # Normalize output
    risk = str(data.get("risk_level", "Medium Concern"))

    if risk.lower().startswith("high"):
        data["risk_level"] = "High Concern"
    elif risk.lower().startswith("low"):
        data["risk_level"] = "Low Concern"
    else:
        data["risk_level"] = "Medium Concern"

    data["scam_category"] = str(
        data.get("scam_category", "Unknown")
    )

    data["summary"] = str(
        data.get("summary", "No summary available.")
    )

    data["limitations"] = str(
        data.get("limitations", "AI cannot verify the sender.")
    )

    for key in ["warning_signs", "recommendations"]:
        value = data.get(key, [])

        if isinstance(value, str):
            value = [value]

        if not isinstance(value, list):
            value = []

        data[key] = [str(item) for item in value]

    return data


# SIDEBAR
st.sidebar.title("🛡️ AI Scam Detector")
st.sidebar.caption("Digital Safety Platform")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Analysis History", "About Project"]
)

st.sidebar.divider()
st.sidebar.info("Powered by Python, Streamlit, Ollama and Gemma 3:1B")


# DASHBOARD
if page == "Dashboard":

    st.title("🛡️ AI Scam Detector")
    st.write(
        "Intelligent detection of suspicious messages and digital fraud"
    )

    total = len(st.session_state.history)

    high = sum(
        1 for x in st.session_state.history
        if x["result"]["risk_level"] == "High Concern"
    )

    medium = sum(
        1 for x in st.session_state.history
        if x["result"]["risk_level"] == "Medium Concern"
    )

    low = sum(
        1 for x in st.session_state.history
        if x["result"]["risk_level"] == "Low Concern"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Analyses", total)
    c2.metric("High Concern", high)
    c3.metric("Medium Concern", medium)
    c4.metric("Low Concern", low)

    st.divider()

    st.subheader("Message Analysis")

    st.write(
        "Submit a suspicious message to receive an AI-powered risk assessment and safety report."
    )

    message = st.text_area(
        "SMS / Email / WhatsApp Message",
        height=180,
        placeholder="Paste your suspicious message here..."
    )

    if st.button("🔍 Analyze Message", use_container_width=True):

        if not message.strip():
            st.warning("Please enter a message before analysis.")

        else:
            try:
                with st.spinner(
                    "AI is examining the message. Please wait..."
                ):
                    result = analyze_message(message)

                st.session_state.last_result = result

                st.session_state.history.append({
                    "message": message,
                    "result": result,
                    "time": datetime.now().strftime(
                        "%d-%m-%Y %I:%M %p"
                    )
                })

                st.success("Analysis completed successfully!")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to Ollama. Please make sure Ollama is running."
                )

            except requests.exceptions.Timeout:
                st.error(
                    "AI response timed out. Please try again."
                )

            except Exception as e:
                st.error(f"Analysis failed: {e}")


    # DISPLAY REPORT
    if st.session_state.last_result:

        result = st.session_state.last_result

        st.divider()
        st.header("Detection Report")

        st.subheader("Risk Assessment")

        risk = result["risk_level"]

        if risk == "High Concern":
            st.error("🔴 " + risk)

        elif risk == "Medium Concern":
            st.warning("🟠 " + risk)

        else:
            st.success("🟢 " + risk)

        st.subheader("Scam Category")
        st.write("**" + result["scam_category"] + "**")

        st.subheader("Analysis Summary")
        st.write(result["summary"])

        st.subheader("⚠️ Warning Signs")

        if result["warning_signs"]:
            for item in result["warning_signs"]:
                st.markdown("- " + item)
        else:
            st.write("No specific warning signs returned.")

        st.subheader("🛡️ Safety Recommendations")

        if result["recommendations"]:
            for item in result["recommendations"]:
                st.markdown("- " + item)
        else:
            st.write("Always verify through official channels.")

        st.subheader("Investigation Limitations")
        st.write(result["limitations"])

        st.caption(
            "AI-generated results are advisory. "
            "Always verify suspicious messages through official channels."
        )


# HISTORY PAGE
elif page == "Analysis History":

    st.title("📋 Analysis History")

    if not st.session_state.history:
        st.info("No analysis records available yet.")

    else:
        for index, item in enumerate(
            reversed(st.session_state.history), 1
        ):

            with st.expander(
                f"Analysis {index} - {item['time']}"
            ):

                st.write("**Message:**")
                st.write(item["message"])

                st.write("**Risk Level:**")
                st.write(item["result"]["risk_level"])

                st.write("**Category:**")
                st.write(item["result"]["scam_category"])

        if st.button("Clear History"):
            st.session_state.history = []
            st.session_state.last_result = None
            st.rerun()


# ABOUT PAGE
elif page == "About Project":

    st.title("About AI Scam Detector")

    st.write("""
    AI Scam Detector is an intelligent application designed
    to identify potentially suspicious digital messages.

    **Main Features**

    - AI-based scam message analysis
    - Risk level identification
    - Phishing detection
    - Warning sign identification
    - Safety recommendations
    - Analysis history

    **Technologies Used**

    - Python
    - Streamlit
    - Ollama
    - Gemma 3:1B

    **Project Goal**

    To improve digital awareness and help users identify
    potentially fraudulent messages.
    """)


# FOOTER
st.divider()

st.markdown(
    "<p style='text-align:center;color:#111111;font-weight:700;'>"
    "AI SCAM DETECTOR | Powered by Python | Streamlit | Ollama | Gemma 3:1B"
    "</p>",
    unsafe_allow_html=True
)
