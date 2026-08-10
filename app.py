import time
import streamlit as st
import os
from google import genai
from google.genai import types

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="EXELYN // AI Cyber Security Agent",
    page_icon="📟",
    layout="centered"
)

# 2. Styling CSS Modern Hacker + Animasi Hujan Biner (Canvas Background)
st.markdown("""
    <style>
    /* Background & Font Utama */
    .stApp {
        background-color: #030803 !important;
        color: #00ff66 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }

    /* Animasi Canvas Biner di Background */
    #binary-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        pointer-events: none;
        opacity: 0.15;
    }

    /* Mengangkat konten Streamlit di atas background */
    .main .block-container {
        position: relative;
        z-index: 1;
        background: rgba(5, 15, 5, 0.85);
        border: 1px solid #00ff66;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.3);
        margin-top: 2rem;
    }

    /* Header & Judul */
    h1 {
        color: #00ff66 !important;
        text-shadow: 0 0 10px rgba(0, 255, 102, 0.7);
        font-size: 1.8rem !important;
        border-bottom: 1px dashed #00ff66;
        padding-bottom: 10px;
    }

    /* Chat Messages */
    .stChatMessage {
        background-color: #081409 !important;
        border: 1px solid #00aa44 !important;
        border-radius: 5px !important;
        color: #ffffff !important;
        margin-bottom: 10px !important;
    }

    /* Input Chat Box */
    .stChatInputContainer textarea {
        background-color: #050f06 !important;
        color: #00ff66 !important;
        border: 1px solid #00ff66 !important;
        font-family: 'Courier New', Courier, monospace !important;
    }

    .stChatInputContainer textarea::placeholder {
        color: #00aa44 !important;
    }

    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #030803;
    }
    ::-webkit-scrollbar-thumb {
        background: #00ff66;
    }
    </style>

    <!-- Canvas HTML & JS untuk Hujan Biner -->
    <canvas id="binary-canvas"></canvas>
    <script>
    const canvas = document.getElementById('binary-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const binary = "01";
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = Array(Math.floor(columns)).fill(1);

    function drawBinary() {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00ff66';
        ctx.font = fontSize + 'px monospace';

        for (let i = 0; i < drops.length; i++) {
            const text = binary.charAt(Math.floor(Math.random() * binary.length));
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    setInterval(drawBinary, 33);
    </script>
""", unsafe_allow_html=True)

# 3. Ambil API Key dari Streamlit Secrets atau Environment Variable
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

st.title("📟 EXELYN_AGENT // Cyber Security AI")

if not api_key:
    st.error("❌ [SYSTEM ERROR]: GEMINI_API_KEY belum terpasang di Streamlit Secrets.")
    st.info("💡 Solusi: Masuk ke Streamlit Dashboard -> App Settings -> Secrets -> Tambahkan GEMINI_API_KEY = 'API_KEY_KAMU'")
    st.stop()

# 4. Inisialisasi Google Gemini Client
client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTION = """
Nama kamu adalah Exelyn, sebuah AI Agent ahli di bidang Cyber Security dan Software Engineering.
Tugas utama kamu adalah membantu pengguna dalam menjawab pertanyaan seputar coding, jaringan, 
penetration testing, keamanan siber, dan debugging. 
Gunakan gaya bahasa yang profesional, ala hacker yang cerdas, tegas, responsif, dan sangat membantu.
"""

# 5. Inisialisasi Riwayat Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "System Online. Saya Exelyn, AI Agent Cyber Security & Coding Assistant. Siap menerima perintah!"}
    ]

# Tampilkan Riwayat Chat
for msg in st.session_state.messages:
    avatar = "🤖" if msg["role"] == "assistant" else "🧑‍💻"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# 6. Area Input User & Pemrosesan AI
if user_input := st.chat_input("Ketik perintah / pertanyaan di sini..."):
    # Simpan & Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(user_input)

                # Kirim ke Gemini API dengan Fallback, Delay & Retry
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Menganalisis sistem..."):
                models_to_try = [
                    "gemini-2.0-flash",
                    "gemini-2.0-flash-lite",
                ]
                
                response_text = None
                last_error = ""
                
                for model_name in models_to_try:
                    try:
                        response = client.models.generate_content(
                            model=model_name,
                            contents=user_input,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_INSTRUCTION,
                                temperature=0.6,
                            )
                        )
                        response_text = response.text
                        break
                    except Exception as e:
                        last_error = str(e)
                        time.sleep(5)  # Beri jeda 5 detik untuk mereset rate limit per menit
                        continue
                
                if not response_text:
                    response_text = f"❌ [ERROR DETAILED]: {last_error}"

                st.write(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
