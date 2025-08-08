import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests
from together import Together
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import google.generativeai as genai

app = Flask(__name__)
CORS(app)


# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")



st.set_page_config(page_title="Chat Page", page_icon="🤖")

page_bg_img = '''
<style>
.stApp {
  background-image: url("https://img.freepik.com/premium-photo/abstract-background-design-images-wallpaper-ai-generated_643360-164033.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)


# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# Together client for DeepSeek
together_client = Together(api_key=TOGETHER_API_KEY)

def call_gemini(prompt):
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Gemini Error] {e}"

def call_moonshot(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://chatbot.com",
            "X-Title": "ChatbotCompare"
        }
        payload = {
            "model": "moonshotai/kimi-dev-72b:free",
            "messages": [{"role": "user", "content": prompt}]
        }
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        data = res.json()
        return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"[Moonshot Error] {e}"

def call_deepseek(prompt):
    try:
        res = together_client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        return f"[DeepSeek Error] {e}"

def final_response_gemini_compare(question, g, m, d):
    try:
        prompt = f"""
You are an intelligent answer aggregator. Below are answers from three AI models for the same question.

Question: {question}

Gemini's Answer:
{g}

Moonshot's Answer:
{m}

DeepSeek's Answer:
{d}

Compare all three responses. Find the facts or statements that are common in at least two answers, and use them to generate a final, concise, and accurate response. Ignore hallucinations or uncommon details.

Return only the final, reliable answer with no accuracy rate with no explanation.
"""
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Final Answer Error] {e}"

# 📌 Excel File Analysis
@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = file.filename.lower()
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            return jsonify({"error": "Unsupported file format. Please upload CSV or Excel files."}), 400

        data_str = df.to_string(index=False)
        prompt = f"Analyze this data:\n{data_str}\nPlease provide insights or summary."
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Streamlit UI
# ---------- Enhanced Header Section ----------
st.markdown("""
    <div style='text-align: center; padding-top: 40px;'>
        <h1 style='font-size: 3em; color: #00ffae;'> <span style="color:#2da1ff;">AI Response Comparator</span></h1>
        <p style='font-size: 1.2em; color: #ccc;'>
            Compare responses from multiple AI models to get the most accurate and reliable answers
        </p>
    </div>
""", unsafe_allow_html=True)

# Minimal question input (no labels)
question = st.text_input("", placeholder="Enter your question here...", label_visibility="collapsed")



if st.button("Generate Response") and question.strip():
    with st.spinner("Calling Gemini..."):
        gemini = call_gemini(question)
    with st.spinner("Calling Moonshot..."):
        moonshot = call_moonshot(question)
    with st.spinner("Calling DeepSeek..."):
        deepseek = call_deepseek(question)
    with st.spinner("Generating Final Answer..."):
        final = final_response_gemini_compare(question, gemini, moonshot, deepseek)

    st.subheader("⭐ Final Best Answer")
    st.success(final)
    st.subheader("🔹 Gemini Response")
    st.write(gemini)

    st.subheader("🔹 Moonshot Response")
    st.write(moonshot)

    st.subheader("🔹 DeepSeek Response")
    st.write(deepseek)

   

