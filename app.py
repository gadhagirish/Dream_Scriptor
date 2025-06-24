# Complete refactored app.py with Story, Visual, Poem, Emotion, and Voice

import streamlit as st
import google.generativeai as genai
import pyrebase
from fpdf import FPDF
import base64
import random
import requests
from PIL import Image
from io import BytesIO
import openai
import unicodedata
from gtts import gTTS
import os

# -------------- Load Custom Starry Night CSS ------------------
def load_custom_css():
    st.markdown("""
        <style>
        body {
            background: #0d0d2b;
            color: #f2f2f2;
            font-family: 'Poppins', sans-serif;
            overflow-x: hidden;
        }

        .stApp {
            background-color: transparent;
        }

        .css-18ni7ap, .css-1d391kg {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 8px 30px rgba(255,255,255,0.1);
        }

        h1, h2, h3 {
            color: #ffd700;
            text-shadow: 0 0 8px #ffffff44;
        }

        button, .stButton>button {
            background-color: #6c63ff;
            color: white;
            border-radius: 10px;
            padding: 0.6em 1.5em;
            font-weight: bold;
            box-shadow: 0 0 10px rgba(108, 99, 255, 0.3);
        }

        button:hover {
            background-color: #574b90;
        }

        /* Dreamy background with stars and a girl */
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: url('https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXA4ZGtqc2c3MXoxN2ozNWh3ejVsYW5rdHJzNm5xczJnbm1kaXJhdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/nWPLGmsjvdQ4g/giphy.gif') no-repeat center center fixed;
            background-size: cover;
            opacity: 0.2;
            z-index: -1;
        }
        
        /* Make the sidebar transparent */
        section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.3) !important;  /* Slightly transparent black */
        backdrop-filter: blur(6px);  /* Optional: adds a glassmorphism blur effect */
        border-right: 1px solid rgba(255, 255, 255, 0.1);  /* Optional subtle border */
    }

    /* Make widgets inside sidebar also blend */
       .stTextInput > div > div,
       .stSelectbox > div > div,
       .stButton > button {
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: #ffffff !important;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
    }

        .stButton > button:hover {
            background-color: rgba(108, 99, 255, 0.4) !important;
    }
        </style>
    """, unsafe_allow_html=True)


# Call this function early in your app
load_custom_css()

# ---------------- Firebase Config -----------------
firebase_config = {
    "apiKey": "AIzaSyAefpQhRImuE2j7uHWCSC_FQ5Kd0mlwkWc",
    "authDomain": "dreamscriptor-b6416.firebaseapp.com",
    "databaseURL": "https://dreamscriptor-b6416-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "dreamscriptor-b6416",
    "storageBucket": "dreamscriptor-b6416.appspot.com",
    "messagingSenderId": "103478142760",
    "appId": "1:103478142760:web:e347ee17637bc51a0f921d"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

# ---------------- Gemini Configuration -----------------
genai.configure(api_key="AIzaSyA76wNUHaTtAHhetOk2Mx5l49CDquuQnt8")
text_model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# ---------------- OpenAI TTS -----------------
openai.api_key = "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"

# ---------------- Streamlit UI -----------------
st.set_page_config(page_title="DreamScriptor", page_icon="🌙")
st.title(" 🌙 Welcome to DreamScriptor")
st.markdown("Turn your late-night dreams into stories and poems 🎭")

# ---------------- Sidebar -----------------
st.sidebar.title("🔐 Login or Register")
choice = st.sidebar.selectbox("Choose an option", ["Login", "Register"])
email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

user = None
if choice == "Register":
    if st.sidebar.button("Create Account"):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            st.sidebar.success("Account created. Please login.")
        except:
            st.sidebar.error("Account creation failed.")
elif choice == "Login":
    if st.sidebar.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.user = user
            st.sidebar.success("Login successful!")
        except:
            st.sidebar.error("Login failed.")

# ---------------- Init Session State -----------------
if "story" not in st.session_state:
    st.session_state.story = ""
if "poem" not in st.session_state:
    st.session_state.poem = ""
if "audio_file" not in st.session_state:
    st.session_state.audio_file = ""

# ---------------- PDF Helpers -----------------
def clean_text(text):
    return unicodedata.normalize("NFKD", text).encode("latin1", "replace").decode("latin1")

def create_pdf(story):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in clean_text(story).split('\n'):
        pdf.multi_cell(0, 10, line)
    return pdf.output(dest="S").encode("latin1")

def get_pdf_download_link(pdf_data, filename):
    b64 = base64.b64encode(pdf_data).decode("utf-8")
    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📄 Download as PDF</a>'


# ---------------- Main App Logic -----------------
if "user" in st.session_state:
    user = st.session_state.user
    st.success("You are logged in!")

    
    dream_input = st.text_area("📝 Describe your dream:")

    if st.button("✨ Generate Story ", key="gen_story"):
        with st.spinner("Generating dream story..."):
            prompt = f"Write a dreamy, poetic story based on this dream: {dream_input}"
            response = text_model.generate_content(prompt)
            story = response.text if hasattr(response, 'text') else response.candidates[0].content.parts[0].text
            st.session_state.story = story

            uid = user["localId"]
            db.child("users").child(uid).push({"dream": dream_input, "story": story})

            st.subheader("📖 Your Dream Story")
            st.write(story)

            pdf_data = create_pdf(story)
            st.markdown(get_pdf_download_link(pdf_data, "dream_story.pdf"), unsafe_allow_html=True)

    if st.session_state.story:
        if st.button("🎭 Generate Dream as Poem", key="gen_poem"):
            prompt = f"Turn the following story into a beautiful poem:\n{st.session_state.story}"
            response = text_model.generate_content(prompt)
            poem = response.text if hasattr(response, 'text') else response.candidates[0].content.parts[0].text
            st.session_state.poem = poem
            st.subheader("📝 Dream Poem")
            st.write(poem)
            pdf_data = create_pdf(poem)
            st.markdown(get_pdf_download_link(pdf_data, "dream_story.pdf"), unsafe_allow_html=True)

        if st.button("🎧 Listen to Story", key="listen_story"):
            tts = gTTS(st.session_state.story)
            audio_path = "story_audio.mp3"
            tts.save(audio_path)
            st.session_state.audio_file = audio_path
            audio_bytes = open(audio_path, 'rb').read()
            st.audio(audio_bytes, format='audio/mp3')

        if st.button("🧠 Analyze Dream Mood", key="analyze_mood"):
            mood_prompt = f"Analyze the mood and emotions of this dream story: {st.session_state.story}"
            mood_response = text_model.generate_content(mood_prompt)
            mood = mood_response.text if hasattr(mood_response, 'text') else mood_response.candidates[0].content.parts[0].text
            st.subheader("🔍 Dream Mood & Emotion")
            st.write(mood)
            pdf_data = create_pdf(mood)
            st.markdown(get_pdf_download_link(pdf_data, "dream_story.pdf"), unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🕰️ Your Past Dreams")
    uid = user["localId"]
    saved_dreams = db.child("users").child(uid).get()
    if saved_dreams.each():
        for item in saved_dreams.each():
            dream_id = item.key()
            dream = item.val()['dream']
            story = item.val()['story']
            st.markdown(f"**Dream:** {dream}")
            st.markdown(f"**Story:** {story}")

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("📝 Edit", key=f"edit_{dream_id}"):
                    new_dream = st.text_area("Edit Dream", dream, key=f"input_{dream_id}")
                    new_story = st.text_area("Edit Story", story, key=f"input_story_{dream_id}")
                    if st.button("💾 Save", key=f"save_{dream_id}"):
                        db.child("users").child(uid).child(dream_id).update({"dream": new_dream, "story": new_story})
                        st.success("Updated successfully. Please refresh the page.")
            with col2:
                if st.button("🗑️ Delete", key=f"del_{dream_id}"):
                    db.child("users").child(uid).child(dream_id).remove()
                    st.warning("Deleted successfully. Please refresh the page.")
            st.markdown("---")
    else:
        st.info("No previous dream stories found.")
else:
    st.warning("Please login or register to use DreamScriptor.")

