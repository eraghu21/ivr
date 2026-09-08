import streamlit as st
from ivr_engine import process_query
from speech_to_text import transcribe_audio
from text_to_speech import speak_text

st.set_page_config(page_title="Agri Voice IVR Simulator", page_icon="🌾", layout="centered")

st.title("🌾 Agriculture IVR Simulator")
st.caption("SIH Prototype • Voice-based farmer assistance")

if "history" not in st.session_state:
    st.session_state.history = []

st.info("Prototype mode: type a query below, or upload an audio file for speech-to-text. "
        "For Streamlit Cloud, browser microphone capture can be added later with a custom component.")

language = st.selectbox("Language / மொழி", ["English", "தமிழ்"])

st.subheader("IVR Menu")
menu = {
    "English": [
        "1 — Crop Disease",
        "2 — Weather",
        "3 — Market Price",
        "4 — Government Schemes",
        "5 — Irrigation Advice",
        "6 — Fertilizer Advice",
        "7 — Farmer Help",
    ],
    "தமிழ்": [
        "1 — பயிர் நோய்",
        "2 — வானிலை",
        "3 — சந்தை விலை",
        "4 — அரசு திட்டங்கள்",
        "5 — பாசன ஆலோசனை",
        "6 — உர ஆலோசனை",
        "7 — விவசாயி உதவி",
    ],
}
for item in menu[language]:
    st.write(item)

st.divider()
st.subheader("🎙️ Ask the Agriculture Assistant")

query = st.text_input(
    "Type your question / உங்கள் கேள்வியை உள்ளிடவும்",
    placeholder="Example: What is the price of tomato today?"
)

audio = st.file_uploader("Optional: upload a WAV/MP3/M4A voice recording", type=["wav", "mp3", "m4a"])

if audio is not None:
    if st.button("Transcribe Audio"):
        with st.spinner("Converting speech to text..."):
            try:
                text = transcribe_audio(audio)
                st.session_state["audio_text"] = text
                st.success("Transcription completed")
            except Exception as e:
                st.error(f"Speech recognition failed: {e}")

if "audio_text" in st.session_state:
    st.text_area("Recognized speech", st.session_state["audio_text"], height=100)
    if not query:
        query = st.session_state["audio_text"]

if st.button("🌾 Ask Assistant", type="primary", use_container_width=True):
    if not query.strip():
        st.warning("Please enter a question or transcribe an audio recording.")
    else:
        result = process_query(query, language)
        st.session_state.history.append((query, result["response"], result["intent"]))

        st.success(result["response"])
        st.caption(f"Detected intent: {result['intent']}")

        if st.button("🔊 Generate Voice Response"):
            try:
                audio_bytes = speak_text(result["response"], language)
                st.audio(audio_bytes, format="audio/mp3")
            except Exception as e:
                st.warning(f"TTS could not be generated: {e}")

if st.session_state.history:
    st.divider()
    st.subheader("Conversation History")
    for q, a, intent in reversed(st.session_state.history[-10:]):
        st.markdown(f"**👨‍🌾 Farmer:** {q}")
        st.markdown(f"**🤖 Assistant:** {a}")
        st.caption(f"Intent: {intent}")
