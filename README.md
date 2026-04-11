# AI-Medical-Report-Analyzer
Built a Streamlit-based application to extract and analyze medical reports (PDF) using LLMs and regex-based parsing. Implemented hybrid system combining rule-based anomaly detection (vitals, BP, glucose, cholesterol) with LLM-generated explanations using Groq API

Overview
This project analyzes medical reports (PDF) and provides:
-Detection of abnormal values (vitals & lab parameters)
-Simple explanations using AI

Tech Stack
-Python
-Streamlit
-Regex (data extraction)
-LLM API via Groq

Features
-PDF text extraction
-Rule-based anomaly detection (Temperature, BP, Glucose, Cholesterol, BMI)
-AI-powered medical explanation
-Clean UI with highlighted risk indicators

Key Concept
This project uses a hybrid approach:
-Rule-based logic → ensures correctness
-LLM → provides interpretation

How to Run- 
  pip install -r requirements.txt
  streamlit run app.py
