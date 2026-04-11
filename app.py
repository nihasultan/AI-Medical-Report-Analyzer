import streamlit as st
from groq import Groq
import re 

st.markdown("""
<style>
.big-title { font-size:28px; font-weight:bold; }
.section { margin-top:20px; }
.card {
    padding:15px;
    border-radius:10px;
    background-color:#f5f5f5;
    margin-bottom:10px;
}
.red { color:#d32f2f; font-weight:bold; }
.green { color:#2e7d32; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

client=Groq(api_key="")

st.title("🧠 AI Medical Report Analyzer")
uploaded_file=st.file_uploader("Upload your medical report(PDF)",type="pdf")


import pdfplumber
if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        text=""
        for page in pdf.pages:
            text+=page.extract_text() or ""

    st.subheader("Extracted text:")
    st.write(text[:1000])


    def detect_abnormal_values(text):
        abnormalities = []

        # Temperature
        temp_match = re.search(r"Temperature:\s*(\d+\.?\d*)", text)
        if temp_match:
            temp = float(temp_match.group(1))
            if temp > 99.5:
                abnormalities.append(f"High Fever detected ({temp}°F)")

        # Pulse Rate
        pulse_match = re.search(r"Pulse Rate:\s*(\d+)", text)
        if pulse_match:
            pulse = int(pulse_match.group(1))
            if pulse > 100:
                abnormalities.append(f"High Pulse Rate ({pulse} bpm)")
            elif pulse > 90:
                abnormalities.append(f"Elevated Pulse Rate ({pulse} bpm)")

        # Respiratory Rate
        resp_match = re.search(r"Respiratory Rate:\s*(\d+)", text)
        if resp_match:
            resp = int(resp_match.group(1))
            if resp > 20:
                abnormalities.append(f"High Respiratory Rate ({resp}/min)")
            elif resp > 16:
                abnormalities.append(f"Slightly elevated respiratory rate ({resp}/min)")

        # Blood Pressure
        bp = re.search(r"Blood Pressure:\s*(\d+)/(\d+)", text)
        if bp:
            sys = int(bp.group(1))
            dia = int(bp.group(2))
            if sys > 130 or dia > 85:
                abnormalities.append(f"High Blood Pressure ({sys}/{dia})")
            elif sys < 90 or dia < 60:
                abnormalities.append(f"Low Blood Pressure ({sys}/{dia})")

        # Glucose
        glucose = re.search(r"Glucose.*?:\s*(\d+)", text)
        if glucose:
            val = int(glucose.group(1))
            if val > 100:
                abnormalities.append(f"High Blood Sugar ({val} mg/dL)")

        # Cholesterol
        chol = re.search(r"Cholesterol.*?:\s*(\d+)", text)
        if chol:
            val = int(chol.group(1))
            if val > 200:
                abnormalities.append(f"High Cholesterol ({val} mg/dL)")

        # BMI
        bmi = re.search(r"BMI:\s*(\d+\.?\d*)", text)
        if bmi:
            val = float(bmi.group(1))
            if val >= 25:
                abnormalities.append(f"Overweight (BMI {val})")

        return abnormalities
        

    if st.button("Analyze report"):
        st.write("Analyzing...")

        clean_text = text[:2000]

        abnormalities = detect_abnormal_values(clean_text)

        st.markdown('<div class="section big-title">🩺 Detected Issues</div>', unsafe_allow_html=True)

        if abnormalities:
            for item in abnormalities:
                st.markdown(f'<div class="card red">⚠️ {item}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card green">✅ No major abnormalities detected</div>', unsafe_allow_html=True)

        prompt = f"""
            You are a medical assistant.

            ONLY use the information provided in the report below.
            DO NOT assume or add any new values.

            Tasks:
            1. Identify abnormal values (only if explicitly present)
            2. Explain them simply
            3. Mention possible risks briefly

            Report:
            {clean_text}
            """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        st.markdown('<div class="section big-title">🤖 AI Explanation</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="card">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
