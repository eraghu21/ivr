import streamlit as st
from streamlit_mic_recorder import mic_recorder
from speech_to_text import transcribe_audio
from text_to_speech import text_to_speech
from ivr_engine import process_query


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Agriculture IVR Assistant",
    page_icon="🌾",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "query" not in st.session_state:
    st.session_state.query = ""

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "recorded_audio" not in st.session_state:
    st.session_state.recorded_audio = None

if "voice_question" not in st.session_state:
    st.session_state.voice_question = None


# =========================================================
# LANGUAGE SELECTION
# =========================================================

# Keep internal values in English.
# Only the displayed text changes.

LANGUAGES = {
    "English": {
        "title": "🌾 Agriculture IVR Assistant",
        "subtitle": "**Voice-based Agriculture Information System**",

        "ask_about": "Ask questions about:",
        "weather": "🌦️ Weather",
        "market_price": "💰 Market Price",
        "fertilizer": "🌱 Fertilizer",
        "irrigation": "💧 Irrigation",
        "crop_disease": "🐛 Crop Disease",
        "government_schemes": "🏛️ Government Schemes",
        "crop_information": "🌾 Crop Information",

        "ivr_settings": "⚙️ IVR Settings",
        "select_language": "Select Language",
        "ivr_menu": "📞 IVR Menu",
        "select_service": "Select Service",

        "demo_version": "Demo Version",
        "demo_info": (
            "Weather and market-price values are currently demo data.\n\n"
            "Live agriculture APIs can be connected later."
        ),

        "voice_question": "🎤 Voice Question",
        "start_speaking": "🎤 Start Speaking",
        "stop_recording": "⏹️ Stop Recording",
        "send_voice": "📤 Send Voice Question",
        "record_again": "🔄 Record Again",

        "voice_recorded": "✅ Voice recorded successfully",
        "listen_recording": "Listen to your recording before sending it.",

        "converting_voice": "🎙️ Converting your voice to text...",
        "voice_converted": "✅ Voice converted successfully",
        "could_not_understand": "⚠️ I could not understand the recording.",
        "speak_clearly": (
            "Please speak clearly, keep the microphone close, and try again."
        ),
        "voice_error": "Voice recognition error",

        "type_question": "⌨️ Type Your Question",
        "agriculture_question": "Agriculture Question",
        "placeholder": (
            "Example:\n"
            "What is today's rice price?\n\n"
            "தமிழில்:\n"
            "நெல்லுக்கு என்ன உரம் போட வேண்டும்?"
        ),

        "ask_assistant": "📝 Ask Agriculture Assistant",
        "enter_question": "Please enter an agriculture question.",

        "recognized_voice": "🎙️ Recognized Voice Question",

        "assistant": "🌾 Agriculture Assistant",
        "processing_error": "IVR processing error",
        "response_title": "🤖 Agriculture IVR Response",
        "tts_unavailable": "Text-to-speech unavailable",
        "no_response": "Sorry, I could not generate an agriculture response.",

        "history": "🗣️ Conversation History",

        "footer": "🌾 Agriculture IVR Simulator | Tamil + English Voice Assistant"
    },

    "தமிழ்": {
        "title": "🌾 வேளாண்மை IVR உதவியாளர்",
        "subtitle": "**குரல் அடிப்படையிலான வேளாண்மை தகவல் அமைப்பு**",

        "ask_about": "பின்வரும் தலைப்புகள் குறித்து கேள்விகள் கேட்கலாம்:",
        "weather": "🌦️ வானிலை",
        "market_price": "💰 சந்தை விலை",
        "fertilizer": "🌱 உரம்",
        "irrigation": "💧 நீர்ப்பாசனம்",
        "crop_disease": "🐛 பயிர் நோய்",
        "government_schemes": "🏛️ அரசு திட்டங்கள்",
        "crop_information": "🌾 பயிர் தகவல்",

        "ivr_settings": "⚙️ IVR அமைப்புகள்",
        "select_language": "மொழியைத் தேர்ந்தெடுக்கவும்",
        "ivr_menu": "📞 IVR மெனு",
        "select_service": "சேவையைத் தேர்ந்தெடுக்கவும்",

        "demo_version": "சோதனை பதிப்பு",
        "demo_info": (
            "வானிலை மற்றும் சந்தை விலைத் தகவல்கள் தற்போது "
            "சோதனைத் தரவுகளாக உள்ளன.\n\n"
            "நேரடி வேளாண்மை API-களை பின்னர் இணைக்கலாம்."
        ),

        "voice_question": "🎤 குரல் கேள்வி",
        "start_speaking": "🎤 பேசத் தொடங்கவும்",
        "stop_recording": "⏹️ பதிவை நிறுத்தவும்",
        "send_voice": "📤 குரல் கேள்வியை அனுப்பவும்",
        "record_again": "🔄 மீண்டும் பதிவு செய்யவும்",

        "voice_recorded": "✅ குரல் வெற்றிகரமாக பதிவு செய்யப்பட்டது",
        "listen_recording": (
            "அனுப்புவதற்கு முன் உங்கள் குரல் பதிவைக் கேட்கவும்."
        ),

        "converting_voice": "🎙️ உங்கள் குரலை உரையாக மாற்றுகிறது...",
        "voice_converted": "✅ குரல் வெற்றிகரமாக உரையாக மாற்றப்பட்டது",
        "could_not_understand": "⚠️ பதிவை புரிந்துகொள்ள முடியவில்லை.",
        "speak_clearly": (
            "தெளிவாகப் பேசவும், மைக்ரோஃபோனுக்கு அருகில் பேசவும், "
            "மீண்டும் முயற்சிக்கவும்."
        ),
        "voice_error": "குரல் அடையாளம் காணும் பிழை",

        "type_question": "⌨️ உங்கள் கேள்வியைத் தட்டச்சு செய்யவும்",
        "agriculture_question": "வேளாண்மை கேள்வி",
        "placeholder": (
            "உதாரணம்:\n"
            "இன்றைய நெல் விலை என்ன?\n\n"
            "English:\n"
            "What is today's rice price?"
        ),

        "ask_assistant": "📝 வேளாண்மை உதவியாளரிடம் கேட்கவும்",
        "enter_question": "தயவுசெய்து வேளாண்மை தொடர்பான கேள்வியை உள்ளிடவும்.",

        "recognized_voice": "🎙️ அடையாளம் காணப்பட்ட குரல் கேள்வி",

        "assistant": "🌾 வேளாண்மை உதவியாளர்",
        "processing_error": "IVR செயலாக்கப் பிழை",
        "response_title": "🤖 வேளாண்மை IVR பதில்",
        "tts_unavailable": "உரை-க்கு-குரல் சேவை கிடைக்கவில்லை",
        "no_response": (
            "மன்னிக்கவும், வேளாண்மை தொடர்பான பதிலை உருவாக்க முடியவில்லை."
        ),

        "history": "🗣️ உரையாடல் வரலாறு",

        "footer": "🌾 வேளாண்மை IVR சிமுலேட்டர் | தமிழ் + ஆங்கில குரல் உதவியாளர்"
    }
}


# =========================================================
# SIDEBAR - LANGUAGE
# =========================================================

with st.sidebar:

    # Language selector
    language = st.selectbox(
        "Select Language / மொழியைத் தேர்ந்தெடுக்கவும்",
        ["English", "தமிழ்"]
    )

    # Current language dictionary
    T = LANGUAGES[language]

    st.divider()

    st.header(T["ivr_settings"])

    # Service names displayed according to language
    service_options = {
        T["weather"]: "Weather",
        T["market_price"]: "Market Price",
        T["fertilizer"]: "Fertilizer",
        T["irrigation"]: "Irrigation",
        T["crop_disease"]: "Crop Disease",
        T["government_schemes"]: "Government Schemes",
        T["crop_information"]: "Crop Information"
    }

    menu_display = st.radio(
        T["select_service"],
        list(service_options.keys())
    )

    # Internal service value
    menu = service_options[menu_display]

    st.divider()

    st.subheader(T["ivr_menu"])

    st.info(
        f"**{T['demo_version']}**\n\n{T['demo_info']}"
    )


# =========================================================
# HEADER
# =========================================================

st.title(T["title"])

st.markdown(
    f"""
    {T["subtitle"]}

    {T["ask_about"]}
    - {T["weather"]}
    - {T["market_price"]}
    - {T["fertilizer"]}
    - {T["irrigation"]}
    - {T["crop_disease"]}
    - {T["government_schemes"]}
    - {T["crop_information"]}
    """
)


# =========================================================
# MAIN COLUMNS
# =========================================================

col1, col2 = st.columns(2)


# =========================================================
# VOICE SECTION
# =========================================================

with col1:

    st.subheader(T["voice_question"])

    st.write(
        (
            "Click **Start Speaking**, ask your agriculture question, "
            "then stop recording."
        )
        if language == "English"
        else
        (
            "**பேசத் தொடங்கவும்** என்பதை அழுத்தி, "
            "உங்கள் வேளாண்மை கேள்வியைக் கேட்டு, "
            "பின்னர் பதிவை நிறுத்தவும்."
        )
    )

    # -----------------------------------------------------
    # MICROPHONE
    # -----------------------------------------------------

    recorded = mic_recorder(
        start_prompt=T["start_speaking"],
        stop_prompt=T["stop_recording"],
        just_once=True,
        use_container_width=True,
        format="wav",
        key="agri_voice_recorder"
    )

    # -----------------------------------------------------
    # STORE RECORDING
    # -----------------------------------------------------

    if recorded:

        audio_bytes = None

        if isinstance(recorded, dict):
            audio_bytes = recorded.get("bytes")

        elif isinstance(recorded, bytes):
            audio_bytes = recorded

        if audio_bytes:

            st.session_state.recorded_audio = audio_bytes
            st.session_state.voice_question = None

    # -----------------------------------------------------
    # PLAY RECORDING
    # -----------------------------------------------------

    if st.session_state.recorded_audio:

        st.success(T["voice_recorded"])

        st.audio(
            st.session_state.recorded_audio,
            format="audio/wav"
        )

        st.write(T["listen_recording"])

        # -------------------------------------------------
        # BUTTONS
        # -------------------------------------------------

        send_col, retry_col = st.columns(2)

        with send_col:

            send_voice = st.button(
                T["send_voice"],
                use_container_width=True,
                type="primary"
            )

        with retry_col:

            retry_voice = st.button(
                T["record_again"],
                use_container_width=True
            )

        # -------------------------------------------------
        # RECORD AGAIN
        # -------------------------------------------------

        if retry_voice:

            st.session_state.recorded_audio = None
            st.session_state.voice_question = None

            st.rerun()

        # -------------------------------------------------
        # SEND VOICE QUESTION
        # -------------------------------------------------

        if send_voice:

            with st.spinner(T["converting_voice"]):

                try:

                    # Whisper language
                    whisper_language = (
                        "ta"
                        if language == "தமிழ்"
                        else "en"
                    )

                    # Speech recognition
                    text = transcribe_audio(
                        st.session_state.recorded_audio,
                        language=whisper_language
                    )

                    # Recognition result
                    if text:

                        st.session_state.query = text
                        st.session_state.voice_question = text

                        st.success(T["voice_converted"])

                        st.rerun()

                    else:

                        st.warning(T["could_not_understand"])
                        st.info(T["speak_clearly"])

                except Exception as e:

                    st.error(
                        f"{T['voice_error']}: {e}"
                    )


# =========================================================
# TEXT QUESTION SECTION
# =========================================================

with col2:

    st.subheader(T["type_question"])

    text_question = st.text_area(
        T["agriculture_question"],
        value=st.session_state.query,
        height=150,
        placeholder=T["placeholder"]
    )

    if st.button(
        T["ask_assistant"],
        use_container_width=True,
        type="primary"
    ):

        if text_question.strip():

            st.session_state.query = text_question.strip()
            st.session_state.voice_question = None

            st.rerun()

        else:

            st.warning(T["enter_question"])


# =========================================================
# RECOGNIZED VOICE QUESTION
# =========================================================

if st.session_state.voice_question:

    st.divider()

    st.subheader(T["recognized_voice"])

    st.info(
        st.session_state.voice_question
    )


# =========================================================
# PROCESS QUESTION
# =========================================================

if st.session_state.query:

    query = st.session_state.query.strip()

    if query:

        st.divider()

        st.subheader(T["assistant"])

        # -------------------------------------------------
        # PROCESS IVR REQUEST
        # -------------------------------------------------

        try:

            result = process_query(
                query,
                language
            )

        except TypeError:

            # Compatibility with older ivr_engine.py
            result = process_query(query)

        except Exception as e:

            st.error(
                f"{T['processing_error']}: {e}"
            )

            result = None

        # -------------------------------------------------
        # DISPLAY RESULT
        # -------------------------------------------------

        if result:

            if isinstance(result, dict):

                response = result.get(
                    "response",
                    result.get(
                        "text",
                        str(result)
                    )
                )

            else:

                response = str(result)

            st.session_state.last_result = response

            # -------------------------------------------------
            # RESPONSE
            # -------------------------------------------------

            st.success(T["response_title"])

            st.write(response)

            # -------------------------------------------------
            # TEXT TO SPEECH
            # -------------------------------------------------

            try:

                audio_response = text_to_speech(
                    response,
                    language=(
                        "ta"
                        if language == "தமிழ்"
                        else "en"
                    )
                )

                if audio_response:

                    st.audio(
                        audio_response,
                        format="audio/mp3"
                    )

            except Exception as e:

                st.warning(
                    f"{T['tts_unavailable']}: {e}"
                )

            # -------------------------------------------------
            # HISTORY
            # -------------------------------------------------

            st.session_state.history.append(
                {
                    "question": query,
                    "response": response
                }
            )

        else:

            st.warning(T["no_response"])


# =========================================================
# CONVERSATION HISTORY
# =========================================================

if st.session_state.history:

    st.divider()

    st.subheader(T["history"])

    for item in reversed(
        st.session_state.history[-10:]
    ):

        with st.expander(
            f"❓ {item['question']}"
        ):

            st.write(
                "🤖",
                item["response"]
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    T["footer"]
)
