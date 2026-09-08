import tempfile
import os

def transcribe_audio(uploaded_file):
    """
    Uses faster-whisper locally when installed.
    The model is downloaded on first use, so this can be slow on Streamlit Cloud.
    """
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        raise RuntimeError("faster-whisper is not installed. Install requirements.txt first.")

    suffix = os.path.splitext(uploaded_file.name)[1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
        f.write(uploaded_file.getbuffer())
        path = f.name

    try:
        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(path, language=None)
        return " ".join(segment.text.strip() for segment in segments).strip()
    finally:
        try:
            os.remove(path)
        except OSError:
            pass
