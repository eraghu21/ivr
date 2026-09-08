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
# HEADER
# =========================================================

st.title("🌾 Agriculture IVR Assistant")

st.markdown(
    """
    **Voice-based Agriculture Information System**

    Ask questions about:
    - 🌦️ Weather
    - 💰 Market Prices
    - 🌱 Fertilizer
    - 💧 Irrigation
    - 🐛 Crop Disease
    - 🏛️ Government Schemes
    - 🌾 Crop Information
    """
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("⚙️ IVR Settings")

    language = st.selectbox(
        "Select Language",
        [
            "English",
            "தமிழ்"
        ]
    )

    st.divider()

    st.subheader("📞 IVR Menu")

    menu = st.radio(
        "Select Service",
        [
            "🌦️ Weather",
            "💰 Market Price",
            "🌱 Fertilizer",
            "💧 Irrigation",
            "🐛 Crop Disease",
            "🏛️ Government Schemes",
            "🌾 Crop Information"
        ]
    )

    st.divider()

    st.info(
        """
        Demo Version

        Weather and market-price values are currently demo data.
        Live agriculture APIs can be connected later.
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

    st.subheader("🎤 Voice Question")

    st.write(
        "Click **Start Speaking**, ask your agriculture question, "
        "then stop recording."
    )

    # -----------------------------------------------------
    # MICROPHONE
    # -----------------------------------------------------

    recorded = mic_recorder(
        start_prompt="🎤 Start Speaking",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        use_container_width=True,
        format="wav",
        key="agri_voice_recorder"
    )

    # -----------------------------------------------------
    # Store recording
    # -----------------------------------------------------

    if recorded:

        audio_bytes = None

        # mic_recorder returns a dictionary
        if isinstance(recorded, dict):

            audio_bytes = recorded.get("bytes")

        # Safety fallback
        elif isinstance(recorded, bytes):

            audio_bytes = recorded

        if audio_bytes:

            st.session_state.recorded_audio = audio_bytes

            st.session_state.voice_question = None

    # -----------------------------------------------------
    # PLAY RECORDING
    # -----------------------------------------------------

    if st.session_state.recorded_audio:

        st.success("✅ Voice recorded successfully")

        st.audio(
            st.session_state.recorded_audio,
            format="audio/wav"
        )

        st.write("Listen to your recording before sending it.")

        # -------------------------------------------------
        # Buttons
        # -------------------------------------------------

        send_col, retry_col = st.columns(2)

        with send_col:

            send_voice = st.button(
                "📤 Send Voice Question",
                use_container_width=True,
                type="primary"
            )

        with retry_col:

            retry_voice = st.button(
                "🔄 Record Again",
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

            with st.spinner(
                "🎙️ Converting your voice to text..."
            ):

                try:

                    # -------------------------------------
                    # Select Whisper language
                    # -------------------------------------

                    whisper_language = (
                        "ta"
                        if language == "தமிழ்"
                        else "en"
                    )

                    # -------------------------------------
                    # Speech recognition
                    # -------------------------------------

                    text = transcribe_audio(
                        st.session_state.recorded_audio,
                        language=whisper_language
                    )

                    # -------------------------------------
                    # Recognition result
                    # -------------------------------------

                    if text:

                        st.session_state.query = text

                        st.session_state.voice_question = text

                        st.success(
                            "✅ Voice converted successfully"
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "⚠️ I could not understand the recording."
                        )

                        st.info(
                            "Please speak clearly, keep the microphone "
                            "close, and try again."
                        )

                except Exception as e:

                    st.error(
                        f"Voice recognition error: {e}"
                    )


# =========================================================
# TEXT QUESTION SECTION
# =========================================================

with col2:

    st.subheader("⌨️ Type Your Question")

    text_question = st.text_area(
        "Agriculture Question",
        value=st.session_state.query,
        height=150,
        placeholder=(
            "Example:\n"
            "What is today's rice price?\n\n"
            "தமிழில்:\n"
            "நெல்லுக்கு என்ன உரம் போட வேண்டும்?"
        )
    )

    if st.button(
        "📝 Ask Agriculture Assistant",
        use_container_width=True,
        type="primary"
    ):

        if text_question.strip():

            st.session_state.query = text_question.strip()

            st.session_state.voice_question = None

            st.rerun()

        else:

            st.warning(
                "Please enter an agriculture question."
            )


# =========================================================
# RECOGNIZED VOICE QUESTION
# =========================================================

if st.session_state.voice_question:

    st.divider()

    st.subheader("🎙️ Recognized Voice Question")

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

        st.subheader("🌾 Agriculture Assistant")

        # -------------------------------------------------
        # Process IVR request
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
                f"IVR processing error: {e}"
            )

            result = None

        # -------------------------------------------------
        # Display result
        # -------------------------------------------------

        if result:

            # Some versions return dictionary
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
            # Response
            # -------------------------------------------------

            st.success("🤖 Agriculture IVR Response")

            st.write(response)

            # -------------------------------------------------
            # Text to Speech
            # -------------------------------------------------

            try:

                audio_response = text_to_speech(
                    response,
                    language="ta"
                    if language == "தமிழ்"
                    else "en"
                )

                if audio_response:

                    st.audio(
                        audio_response,
                        format="audio/mp3"
                    )

            except Exception as e:

                st.warning(
                    f"Text-to-speech unavailable: {e}"
                )

            # -------------------------------------------------
            # History
            # -------------------------------------------------

            st.session_state.history.append(
                {
                    "question": query,
                    "response": response
                }
            )

        else:

            st.warning(
                "Sorry, I could not generate an agriculture response."
            )


# =========================================================
# CONVERSATION HISTORY
# =========================================================

if st.session_state.history:

    st.divider()

    st.subheader("🗣️ Conversation History")

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
    "🌾 Agriculture IVR Simulator | "
    "Tamil + English Voice Assistant"
)
