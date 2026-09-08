import streamlit as st
from ivr_engine import process_query
from speech_to_text import transcribe_audio
from text_to_speech import speak_text

st.set_page_config(page_title="Agri Voice IVR", page_icon="🌾", layout="wide")

# Optional browser microphone component
try:
    from streamlit_mic_recorder import speech_to_text as browser_speech_to_text
    MIC_AVAILABLE = True
except Exception:
    MIC_AVAILABLE = False

if "history" not in st.session_state:
    st.session_state.history = []
if "query" not in st.session_state:
    st.session_state.query = ""
if "last_result" not in st.session_state:
    st.session_state.last_result = None

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; max-width: 1150px;}
.ivr-card {padding: 18px; border: 1px solid #ddd; border-radius: 14px; background: rgba(128,128,128,.06);}
.small {font-size: .9rem; opacity: .75;}
</style>
""", unsafe_allow_html=True)

st.title("🌾 Agri Voice IVR Simulator")
st.caption("SIH Agriculture Platform • Simulator Mode • English + Tamil")

with st.sidebar:
    st.header("⚙️ IVR Settings")
    language = st.selectbox("Language / மொழி", ["English", "தமிழ்"])
    st.divider()
    st.subheader("IVR Menu")
    menu = {
        "English": [
            ("1", "Crop Disease", "crop disease"),
            ("2", "Weather", "weather"),
            ("3", "Market Price", "tomato market price"),
            ("4", "Government Schemes", "government schemes"),
            ("5", "Irrigation Advice", "tomato irrigation"),
            ("6", "Fertilizer Advice", "tomato fertilizer"),
            ("7", "Farmer Help", "help"),
        ],
        "தமிழ்": [
            ("1", "பயிர் நோய்", "பயிர் நோய்"),
            ("2", "வானிலை", "வானிலை"),
            ("3", "சந்தை விலை", "தக்காளி சந்தை விலை"),
            ("4", "அரசு திட்டங்கள்", "அரசு திட்டங்கள்"),
            ("5", "பாசன ஆலோசனை", "தக்காளி பாசனம்"),
            ("6", "உர ஆலோசனை", "தக்காளி உரம்"),
            ("7", "விவசாயி உதவி", "உதவி"),
        ],
    }
    for n, label, example in menu[language]:
        if st.button(f"{n}  {label}", use_container_width=True, key=f"menu_{n}_{language}"):
            st.session_state.query = example

left, right = st.columns([1.35, .65])

with left:
    st.subheader("🎙️ Speak or type your question")

    if MIC_AVAILABLE:
        st.success("🎤 Browser microphone enabled")
        spoken = browser_speech_to_text(
            language="ta-IN" if language == "தமிழ்" else "en-US",
            start_prompt="🎤 Start speaking",
            stop_prompt="⏹️ Stop recording",
            use_container_width=True,
            just_once=True,
            key="browser_mic",
        )
        if spoken:
            st.session_state.query = spoken
    else:
        st.info("Browser microphone component is unavailable. You can still upload audio below.")

    query = st.text_area(
        "Question / கேள்வி",
        value=st.session_state.query,
        height=90,
        placeholder="Example: What is the tomato market price today? / தக்காளி விலை என்ன?",
        key="query_box",
    )
    st.session_state.query = query

    audio = st.file_uploader(
        "Or upload a voice recording",
        type=["wav", "mp3", "m4a", "ogg", "webm"],
        help="Used as a fallback when browser microphone is not available.",
    )
    if audio and st.button("📝 Convert uploaded audio", use_container_width=True):
        with st.spinner("Converting speech to text..."):
            try:
                text = transcribe_audio(audio)
                st.session_state.query = text
                st.success("Speech converted successfully")
                st.rerun()
            except Exception as e:
                st.error(f"Speech recognition failed: {e}")

    ask = st.button("🌾 Ask Agriculture Assistant", type="primary", use_container_width=True)

    if ask:
        if not st.session_state.query.strip():
            st.warning("Please speak, type a question, or choose an IVR menu option.")
        else:
            result = process_query(st.session_state.query, language)
            st.session_state.last_result = result
            st.session_state.history.append({
                "query": st.session_state.query,
                "response": result["response"],
                "intent": result["intent"],
                "language": language,
            })

with right:
    st.subheader("📞 Simulator Status")
    st.markdown('<div class="ivr-card">', unsafe_allow_html=True)
    st.metric("Mode", "SIMULATOR")
    st.metric("Language", language)
    st.metric("Calls / Queries", len(st.session_state.history))
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("This version is designed so the same IVR engine can later be connected to a real telephony/SIP provider.")

if st.session_state.last_result:
    result = st.session_state.last_result
    st.divider()
    st.subheader("🤖 Agriculture Assistant Response")
    st.success(result["response"])
    st.caption(f"Detected intent: `{result['intent']}`")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔊 Play voice response", use_container_width=True):
            try:
                audio_bytes = speak_text(result["response"], language)
                st.audio(audio_bytes, format="audio/mp3", autoplay=False)
            except Exception as e:
                st.warning(f"TTS could not be generated: {e}")
    with col2:
        if st.button("🧹 Clear current question", use_container_width=True):
            st.session_state.query = ""
            st.session_state.last_result = None
            st.rerun()

if st.session_state.history:
    st.divider()
    st.subheader("🗣️ Conversation History")
    for item in reversed(st.session_state.history[-10:]):
        with st.expander(f"👨‍🌾 {item['query']}"):
            st.write(item["response"])
            st.caption(f"Intent: {item['intent']} • {item['language']}")

st.divider()
st.caption("⚠️ Demo weather and market values are not live data. Replace them with verified official APIs before production deployment.")
st.caption("Model 1 = Streamlit IVR simulator | Model 2 = Real telephone IVR integration")
