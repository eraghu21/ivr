import os
import tempfile
import streamlit as st

@st.cache_resource(show_spinner=False)
def _load_model():
    from faster_whisper import WhisperModel
    return WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(uploaded_file):
    model = _load_model()
    suffix = os.path.splitext(getattr(uploaded_file, "name", ""))[1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
        f.write(uploaded_file.getbuffer())
        path = f.name
    try:
        segments, _ = model.transcribe(path, language=None, vad_filter=True)
        return " ".join(s.text.strip() for s in segments).strip()
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
