import streamlit as st
import pandas as pd
import whisper
from gtts import gTTS
import tempfile

st.set_page_config("AI Sales Agent", layout="centered")

st.title("📞 Marathi AI Sales Agent Demo")
st.caption("Simulated Live Sales Call")

# ---------- LOAD WHISPER ----------
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# ---------- GOOGLE SHEET ----------
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1KQj3SHLWRvCrMlvFZ-BIatnqxmwgaIpTisROLBaYhFg/export?format=csv"

# ---------- SALES SCRIPT ----------
def sales_script(step):
    scripts = [
        "नमस्कार सर, मी AI विक्री सहाय्यक बोलतोय.",
        "आमची सेवा तुमचा खर्च आणि वेळ वाचवते.",
        "आपल्याला यामध्ये रस आहे का?",
        "छान सर, मी तुमची माहिती नोंदवतो.",
        "धन्यवाद सर, लवकरच संपर्क करू."
    ]
    return scripts[step]

# ---------- SESSION STATE ----------
if "call_started" not in st.session_state:
    st.session_state.call_started = False
    st.session_state.step = 0

# ---------- START CALL ----------
if st.button("▶️ START CALL"):
    st.session_state.call_started = True
    st.session_state.step = 0
    st.success("📞 Calling customer...")

# ---------- CALL FLOW ----------
if st.session_state.call_started:

    response = sales_script(st.session_state.step)

    st.info(f"🤖 Agent: {response}")

    # Speak Marathi
    tts = gTTS(response, lang="mr")
    audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(audio_file.name)
    st.audio(audio_file.name, autoplay=True)

    # Customer voice input
    audio = st.audio_input("🎙️ Customer Reply")

    if audio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio.read())
            path = f.name

        result = model.transcribe(path, language="mr")
        st.write("🧑 Customer said:", result["text"])

        st.session_state.step += 1

        if st.session_state.step >= 5:
            st.success("✅ Call Completed")
            st.session_state.call_started = False
