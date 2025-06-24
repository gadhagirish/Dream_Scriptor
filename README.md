# 🌙 DreamScriptor

**Turn your late-night dreams into beautiful stories, poems, and emotions — and hear them too.**

DreamScriptor is an AI-powered storytelling platform where users can describe their dreams and watch them come to life as narrated stories, poems, and mood reflections. It also offers a personalized dashboard to view, edit, or delete saved dreams — all wrapped in a dreamy starry night interface.

---

## ✨ Features

### 🔐 User Authentication (via Firebase)
- Secure user registration and login.
- Firebase Authentication integrated with Streamlit sidebar.

### 📝 Dream to Story Converter
- Describe your dream in natural language.
- Gemini AI (Google) turns it into a vivid poetic story.
- Save dream + story securely to the Firebase Realtime Database.

### 🧠 Emotion Analyzer
- Gemini AI analyzes your story and describes the emotions and moods reflected in it (e.g., calm, fear, joy, wonder).

### 🎭 Dream to Poem Converter
- Converts the AI-generated dream story into a beautifully formatted poem.

### 🎧 AI Voice Narration
- Converts the dream story into voice using **Google TTS (gTTS)**.
- Streamlit audio player to play the generated audio.

### 📄 PDF Export
- Download dream stories, poems, or mood analysis as printable PDFs.

### 🗂️ User Dashboard
- View previously saved dreams and stories.
- Edit or delete saved dreams from your Firebase account.

### 🎨 Custom UI Theme
- Night sky background with a girl gazing at the stars (animated via Giphy).
- Transparent login panel (glassmorphism effect).
- Floating stars, glowing buttons, and soft shadow effects.

---

## 🚀 Tech Stack

| Component          | Technology                          |
|-------------------|--------------------------------------|
| **Frontend**       | Streamlit, HTML/CSS (custom theme)  |
| **AI Story/Poem**  | Gemini 1.5 Flash (Google AI Studio) |
| **TTS Engine**     | gTTS (Google Text-to-Speech)        |
| **Database**       | Firebase Realtime Database          |
| **Auth**           | Firebase Authentication             |
| **PDF Export**     | fpdf (Python)                       |
| **Image/Audio**    | Giphy, Streamlit media players      |

---

## 📂 Project Structure

DreamScriptor/
├── app.py # Main Streamlit app
├── requirements.txt # Python dependencies
├── .streamlit/
│ └── config.toml # (optional) page setup
└── README.md # You're reading it!


📜 License
MIT License © 2025 @gadhagirish
