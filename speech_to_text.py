import os
import tempfile
from faster_whisper import WhisperModel


# ---------------------------------------------------------
# Whisper model
# ---------------------------------------------------------

_model = None


def get_model():
    """
    Load Faster-Whisper only once.
    This avoids loading the model repeatedly.
    """

    global _model

    if _model is None:
        _model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

    return _model


# ---------------------------------------------------------
# Convert audio to bytes
# ---------------------------------------------------------

def _get_audio_bytes(audio_data):
    """
    Supports:
    - bytes
    - bytearray
    - Streamlit UploadedFile
    - file-like objects
    """

    if audio_data is None:
        return None

    # mic_recorder normally returns bytes
    if isinstance(audio_data, bytes):
        return audio_data

    # bytearray
    if isinstance(audio_data, bytearray):
        return bytes(audio_data)

    # Streamlit UploadedFile / BytesIO
    if hasattr(audio_data, "getvalue"):
        return audio_data.getvalue()

    # File-like object
    if hasattr(audio_data, "read"):
        return audio_data.read()

    # Older Streamlit UploadedFile
    if hasattr(audio_data, "getbuffer"):
        return bytes(audio_data.getbuffer())

    raise TypeError(
        f"Unsupported audio input type: {type(audio_data)}"
    )


# ---------------------------------------------------------
# Speech to Text
# ---------------------------------------------------------

def transcribe_audio(audio_data, language="ta"):
    """
    Convert recorded audio into text.

    language:
        ta = Tamil
        en = English
    """

    audio_bytes = _get_audio_bytes(audio_data)

    if not audio_bytes:
        return ""

    temp_path = None

    try:

        # -------------------------------------------------
        # Save microphone audio temporarily
        # -------------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as temp_file:

            temp_file.write(audio_bytes)
            temp_path = temp_file.name

        # -------------------------------------------------
        # Load Whisper
        # -------------------------------------------------

        model = get_model()

        # -------------------------------------------------
        # Transcription
        # -------------------------------------------------

        segments, info = model.transcribe(
            temp_path,

            # Force selected language
            language=language,

            # Better recognition
            beam_size=5,
            best_of=5,

            # More stable output
            temperature=0,

            # Remove long silence
            vad_filter=True,

            vad_parameters={
                "min_silence_duration_ms": 500
            },

            # Each question is independent
            condition_on_previous_text=False
        )

        # -------------------------------------------------
        # Collect text
        # -------------------------------------------------

        result = []

        for segment in segments:

            text = segment.text.strip()

            if text:
                result.append(text)

        final_text = " ".join(result).strip()

        return final_text

    except Exception as e:

        print("Speech recognition error:", e)

        return ""

    finally:

        # -------------------------------------------------
        # Delete temporary audio
        # -------------------------------------------------

        if temp_path and os.path.exists(temp_path):

            try:
                os.remove(temp_path)

            except Exception:
                pass
