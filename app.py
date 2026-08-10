import streamlit as st
import time
from google import genai
from google.genai import types

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Exelyn agent V1",
    page_icon="🤖",
    layout="centered"
)

# SYSTEM INSTRUCTION UNTUK EXELYN
SYSTEM_INSTRUCTION = """
Nama kamu adalah Exelyn, sebuah AI Agent ahli di bidang Cyber Security dan Programming.
Tugas utama kamu adalah membantu pengguna dalam menjawab pertanyaan seputar penetration testing, keamanan siber, dan debugging.
Gunakan gaya bahasa yang profesional, ala hacker yang cerdas, tegas, dan responsif.
"""

# 2. Custom CSS untuk Tampilan Dark/Matrix UI Modern
st.markdown("""
    <style>
    /* Background Dark Theme */
    .stApp {
        background-color: #0b0f12;
        background-image: radial-gradient(#111a21 1px, transparent 1px);
        background-size: 20px 20px;
        color: #e0e0e0;
    }
    
    /* Sembunyikan Header Bawaan Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header Avatar & Judul */
    .main-header {
        text-align: center;
        padding-top: 20px;
        padding-bottom: 20px;
    }
    .avatar-img {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 2px solid #00ff88;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
        margin-bottom: 10px;
    }
    .title-text {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 1px;
    }

    /* Sub-header / Prompt Suggestions */
    .section-title {
        color: #8b949e;
        font-size: 14px;
        margin-top: 25px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Styling Tombol Saran */
    .stButton > button {
        width: 100%;
        text-align: left;
        background-color: #161b22;
        border: 1px solid #30363d;
        color: #c9d1d9;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        border-color: #00ff88;
        background-color: #1f242c;
        color: #00ff88;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header Utama (Logo & Nama)
st.markdown("""
    <div class="main-header">
        <img src="https://api.iconify.design/lucide:bot.svg?color=%2300ff88" class="avatar-img">
        <div class="title-text">Exelyn agent V1</div>
    </div>
""", unsafe_allow_html=True)

# 4. Inisialisasi Client Gemini
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 5. Inisialisasi Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Variable penampung saran yang diklik
prompt_selected = None

# 6. Tampilkan Suggestion Cards (Hanya jika obrolan belum dimulai)
if len(st.session_state.messages) == 0:
    st.markdown('<div class="section-title">⚡ Disarankan</div>', unsafe_allow_html=True)
    
    if st.button("🛡️ Hardening server Linux\nchecklist keamanan praktis"):
        prompt_selected = "Berikan checklist keamanan praktis untuk hardening server Linux."
    if st.button("🐍 Reverse shell Python\nbeserta teknik deteksinya"):
        prompt_selected = "Jelaskan tentang reverse shell Python beserta teknik deteksinya."
    if st.button("🔍 Analisis malware\nstatic & dynamic analysis"):
        prompt_selected = "Bagaimana alur analisis malware menggunakan static dan dynamic analysis?"

# 7. Tampilkan Riwayat Chat
for msg in st.session_state.messages:
    avatar = "🤖" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# 8. Tangkap Input dari User atau Tombol Saran
user_input = st.chat_input("Ada yang bisa saya bantu hari ini?")

# Jika user mengklik salah satu tombol saran
if prompt_selected and not user_input:
    user_input = prompt_selected

# 9. Pemrosesan Pesan oleh AI
if user_input:
    # Simpan & tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)

    # Kirim ke Gemini API
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
                    time.sleep(2)
                    continue
            
            if not response_text:
                response_text = f"❌ [ERROR DETAILED]: {last_error}"

            st.write(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
