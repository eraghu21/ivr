import os
import tempfile
from faster_whisper import WhisperModel


_model = None


def get_model():
    global _model

    if _model is None:
        _model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

    return _model


def transcribe_audio(audio_data, language="ta"):
    """
    Convert microphone WAV bytes to text.

    language:
        ta = Tamil
        en = English
        None = automatic detection
    """

    if audio_data is None:
        return ""

    # Convert input to bytes
    if isinstance(audio_data, bytes):
        audio_bytes = audio_data

    elif isinstance(audio_data, bytearray):
        audio_bytes = bytes(audio_data)

    elif hasattr(audio_data, "getvalue"):
        audio_bytes = audio_data.getvalue()

    elif hasattr(audio_data, "read"):
        audio_bytes = audio_data.read()

    elif hasattr(audio_data, "getbuffer"):
        audio_bytes = bytes(audio_data.getbuffer())

    else:
        raise TypeError(
            f"Unsupported audio type: {type(audio_data)}"
        )

    if not audio_bytes:
        return ""

    temp_path = None

    try:

        # Save microphone recording
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as f:
            f.write(audio_bytes)
            temp_path = f.name

        model = get_model()

        # IMPORTANT:
        # Force Tamil or English instead of automatic detection
        segments, info = model.transcribe(
            temp_path,
            language=language,
            beam_size=5,
            best_of=5,
            temperature=0,
            vad_filter=True,
            vad_parameters=dict(
                min_silence_duration_ms=500
            ),
            condition_on_previous_text=False
        )

        result = []

        for segment in segments:
            text = segment.text.strip()

            if text:
                result.append(text)

        return " ".join(result).strip()

    except Exception as e:
        print("Speech recognition error:", e)
        return ""

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
