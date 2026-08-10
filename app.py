import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Mengambil API Key dari Environment Variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Konfigurasi Google AI Studio SDK
genai.configure(api_key=GEMINI_API_KEY)

# System Prompt Exelyn Agent
SYSTEM_PROMPT = """
Nama kamu adalah Exelyn, sebuah AI Agent ahli di bidang Cyber Security dan Software Engineering.
Tugas utama kamu adalah membantu pengguna dalam menjawab pertanyaan seputar coding, jaringan, 
penetration testing, keamanan siber, dan debugging. 
Gunakan gaya bahasa yang profesional, ala hacker yang cerdas, tegas, namun sangat membantu.
"""

# Buat model dengan system instruction
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    try:
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"System Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
