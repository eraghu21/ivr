import streamlit as st

from ivr_engine import process_query
from speech_to_text import transcribe_audio
from text_to_speech import speak_text


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Agri Voice IVR",
    page_icon="🌾",
    layout="wide"
)


# ============================================================
# MICROPHONE COMPONENT
# ============================================================

try:
    from streamlit_mic_recorder import mic_recorder

    MIC_AVAILABLE = True

except Exception:
    MIC_AVAILABLE = False


# ============================================================
# SESSION STATE
# ============================================================

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


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.5rem;
        max-width: 1150px;
    }

    .ivr-card {
        padding: 18px;
        border: 1px solid #ddd;
        border-radius: 14px;
        background: rgba(128,128,128,.06);
        margin-bottom: 15px;
    }

    .voice-card {
        padding: 20px;
        border: 2px solid #ddd;
        border-radius: 15px;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    .small {
        font-size: .9rem;
        opacity: .75;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.title("🌾 Agri Voice IVR Simulator")

st.caption(
    "SIH Agriculture Platform • Simulator Mode • English + Tamil"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ IVR Settings")

    language = st.selectbox(
        "Language / மொழி",
        ["English", "தமிழ்"]
    )

    st.divider()

    st.subheader("📞 IVR Menu")

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

    for number, label, example in menu[language]:

        if st.button(
            f"{number}  {label}",
            use_container_width=True,
            key=f"menu_{number}_{language}"
        ):

            st.session_state.query = example

            st.session_state.voice_question = None


# ============================================================
# MAIN COLUMNS
# ============================================================

left, right = st.columns(
    [1.35, 0.65]
)


# ============================================================
# LEFT COLUMN
# ============================================================

with left:

    st.subheader(
        "🎙️ Speak or type your question"
    )


    # ========================================================
    # VOICE RECORDING
    # ========================================================

    st.markdown(
        '<div class="voice-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### 🎤 Voice Question"
    )

    st.caption(
        "Step 1: Start speaking → Step 2: Stop → "
        "Step 3: Check recording → Step 4: Send"
    )


    if MIC_AVAILABLE:

        # ----------------------------------------------------
        # RECORD BUTTON
        # ----------------------------------------------------

        recorded = mic_recorder(

            start_prompt="🎤 Start Speaking",

            stop_prompt="⏹️ Stop Recording",

            just_once=True,

            use_container_width=True,

            format="wav",

            key="agri_voice_recorder"
        )


        # ----------------------------------------------------
        # SAVE RECORDING
        # ----------------------------------------------------

        if recorded:

            if isinstance(recorded, dict):

                audio_bytes = recorded.get("bytes")

            else:

                audio_bytes = recorded


            if audio_bytes:

                st.session_state.recorded_audio = audio_bytes

                st.session_state.voice_question = None


        # ----------------------------------------------------
        # CHECK RECORDED AUDIO
        # ----------------------------------------------------

        if st.session_state.recorded_audio:

            st.success(
                "✅ Voice recording completed"
            )

            st.markdown(
                "#### 🔊 Check your recording"
            )

            st.audio(
                st.session_state.recorded_audio,
                format="audio/wav"
            )

            st.caption(
                "Listen to the recording above. "
                "If it is clear, click Send Voice Question."
            )


            # ------------------------------------------------
            # ACTION BUTTONS
            # ------------------------------------------------

            col_voice_1, col_voice_2 = st.columns(2)


            with col_voice_1:

                send_voice = st.button(

                    "📤 Send Voice Question",

                    type="primary",

                    use_container_width=True,

                    key="send_voice_question"
                )


            with col_voice_2:

                record_again = st.button(

                    "🔄 Record Again",

                    use_container_width=True,

                    key="record_again"
                )


            # ------------------------------------------------
            # RECORD AGAIN
            # ------------------------------------------------

            if record_again:

                st.session_state.recorded_audio = None

                st.session_state.voice_question = None

                st.rerun()


            # ------------------------------------------------
            # SEND VOICE QUESTION
            # ------------------------------------------------

            if send_voice:

                with st.spinner(
                    "🧠 Converting your voice into text..."
                ):

                    try:

                        text = transcribe_audio(
                            st.session_state.recorded_audio
                        )


                        # ------------------------------------
                        # CHECK RESULT
                        # ------------------------------------

                        if text and text.strip():

                            text = text.strip()

                            st.session_state.query = text

                            st.session_state.voice_question = text


                            st.success(
                                "✅ Voice question received"
                            )


                            st.markdown(
                                "### 🗣️ You asked"
                            )

                            st.info(text)


                            st.rerun()


                        else:

                            st.warning(
                                "⚠️ I could not understand "
                                "the recording."
                            )

                            st.info(
                                "Please click Record Again "
                                "and speak clearly."
                            )


                    except Exception as e:

                        st.error(
                            "❌ Speech recognition failed"
                        )

                        st.exception(e)


    else:

        st.warning(
            "🎤 Browser microphone component "
            "is not available."
        )

        st.info(
            "Please install streamlit-mic-recorder "
            "or use the audio upload option below."
        )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # SHOW RECOGNIZED VOICE QUESTION
    # ========================================================

    if st.session_state.voice_question:

        st.success(
            "🗣️ Recognized Voice Question"
        )

        st.write(
            st.session_state.voice_question
        )


    # ========================================================
    # TEXT QUESTION
    # ========================================================

    query = st.text_area(

        "Question / கேள்வி",

        value=st.session_state.query,

        height=90,

        placeholder=(
            "Example: What is the tomato market price today? "
            "/ தக்காளி விலை என்ன?"
        ),

        key="query_box"
    )


    st.session_state.query = query


    # ========================================================
    # AUDIO UPLOAD FALLBACK
    # ========================================================

    st.markdown(
        "### 📁 Alternative: Upload Voice Recording"
    )

    audio = st.file_uploader(

        "Upload an audio recording",

        type=[
            "wav",
            "mp3",
            "m4a",
            "ogg",
            "webm"
        ],

        help=(
            "Use this option if the browser microphone "
            "does not work."
        ),

        key="audio_upload"
    )


    if audio:

        if st.button(
            "📝 Convert Uploaded Audio",
            use_container_width=True,
            key="convert_uploaded_audio"
        ):

            with st.spinner(
                "🧠 Converting speech to text..."
            ):

                try:

                    text = transcribe_audio(audio)

                    if text and text.strip():

                        st.session_state.query = text.strip()

                        st.success(
                            "✅ Speech converted successfully"
                        )

                        st.write(
                            "**You said:**",
                            text
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "⚠️ No speech could be detected."
                        )

                except Exception as e:

                    st.error(
                        f"❌ Speech recognition failed: {e}"
                    )


    # ========================================================
    # ASK BUTTON
    # ========================================================

    ask = st.button(

        "🌾 Ask Agriculture Assistant",

        type="primary",

        use_container_width=True,

        key="ask_agriculture"
    )


    if ask:

        current_query = st.session_state.query.strip()


        if not current_query:

            st.warning(
                "Please speak, type a question, "
                "or choose an IVR menu option."
            )


        else:

            with st.spinner(
                "🤖 Processing your agriculture question..."
            ):

                try:

                    result = process_query(
                        current_query,
                        language
                    )


                    st.session_state.last_result = result


                    st.session_state.history.append({

                        "query": current_query,

                        "response": result.get(
                            "response",
                            ""
                        ),

                        "intent": result.get(
                            "intent",
                            "unknown"
                        ),

                        "language": language,

                    })


                except Exception as e:

                    st.error(
                        f"❌ IVR processing failed: {e}"
                    )


# ============================================================
# RIGHT COLUMN - IVR STATUS
# ============================================================

with right:

    st.subheader(
        "📞 Simulator Status"
    )


    st.markdown(
        '<div class="ivr-card">',
        unsafe_allow_html=True
    )


    st.metric(
        "Mode",
        "SIMULATOR"
    )


    st.metric(
        "Language",
        language
    )


    st.metric(
        "Calls / Queries",
        len(st.session_state.history)
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    st.info(
        "The same IVR engine can later be connected "
        "to a real telephone/SIP provider."
    )


    # ========================================================
    # CURRENT QUERY STATUS
    # ========================================================

    if st.session_state.query:

        st.markdown(
            '<div class="ivr-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### 📝 Current Question"
        )

        st.write(
            st.session_state.query
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ============================================================
# AGRICULTURE RESPONSE
# ============================================================

if st.session_state.last_result:

    result = st.session_state.last_result


    st.divider()


    st.subheader(
        "🤖 Agriculture Assistant Response"
    )


    response_text = result.get(
        "response",
        "No response available."
    )


    st.success(
        response_text
    )


    st.caption(
        "Detected intent: "
        f"`{result.get('intent', 'unknown')}`"
    )


    # ========================================================
    # RESPONSE BUTTONS
    # ========================================================

    response_col1, response_col2 = st.columns(2)


    with response_col1:

        if st.button(
            "🔊 Play Voice Response",
            use_container_width=True,
            key="play_voice_response"
        ):

            try:

                with st.spinner(
                    "🔊 Generating voice response..."
                ):

                    audio_bytes = speak_text(
                        response_text,
                        language
                    )


                st.audio(
                    audio_bytes,
                    format="audio/mp3",
                    autoplay=False
                )


            except Exception as e:

                st.warning(
                    f"⚠️ TTS could not be generated: {e}"
                )


    with response_col2:

        if st.button(
            "🧹 Clear Current Question",
            use_container_width=True,
            key="clear_question"
        ):

            st.session_state.query = ""

            st.session_state.last_result = None

            st.session_state.recorded_audio = None

            st.session_state.voice_question = None

            st.rerun()


# ============================================================
# CONVERSATION HISTORY
# ============================================================

if st.session_state.history:

    st.divider()


    st.subheader(
        "🗣️ Conversation History"
    )


    for item in reversed(
        st.session_state.history[-10:]
    ):

        with st.expander(
            f"👨‍🌾 {item['query']}"
        ):

            st.write(
                item["response"]
            )

            st.caption(
                f"Intent: {item['intent']} • "
                f"Language: {item['language']}"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(
    "⚠️ Demo weather and market values are not live data. "
    "Replace them with verified official APIs before production deployment."
)


st.caption(
    "Model 1 = Streamlit IVR Simulator | "
)

