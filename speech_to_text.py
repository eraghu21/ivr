```python
import io
import os
import tempfile

from faster_whisper import WhisperModel


# ============================================================
# WHISPER MODEL
# ============================================================

_model = None


def get_model():
    """
    Load Whisper only once.
    This avoids loading the model for every question.
    """

    global _model

    if _model is None:

        _model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

    return _model


# ============================================================
# SPEECH TO TEXT
# ============================================================

def transcribe_audio(uploaded_file):
    """
    Convert uploaded/recorded audio to text.

    Supports:
        1. Streamlit UploadedFile
        2. bytes
        3. bytearray
        4. BytesIO
    """

    # --------------------------------------------------------
    # GET AUDIO BYTES
    # --------------------------------------------------------

    if isinstance(uploaded_file, bytes):

        audio_bytes = uploaded_file


    elif isinstance(uploaded_file, bytearray):

        audio_bytes = bytes(uploaded_file)


    elif hasattr(uploaded_file, "getvalue"):

        # Streamlit UploadedFile / BytesIO
        audio_bytes = uploaded_file.getvalue()


    elif hasattr(uploaded_file, "read"):

        audio_bytes = uploaded_file.read()


    else:

        raise TypeError(
            "Unsupported audio input type: "
            f"{type(uploaded_file)}"
        )


    if not audio_bytes:

        raise ValueError(
            "The recorded audio is empty."
        )


    # --------------------------------------------------------
    # SAVE TEMPORARY AUDIO FILE
    # --------------------------------------------------------

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as temp_file:

            temp_file.write(audio_bytes)

            temp_path = temp_file.name


        # ----------------------------------------------------
        # LOAD WHISPER
        # ----------------------------------------------------

        model = get_model()


        # ----------------------------------------------------
        # TRANSCRIBE
        # ----------------------------------------------------

        segments, info = model.transcribe(

            temp_path,

            beam_size=5,

            vad_filter=True,

            condition_on_previous_text=False
        )


        # ----------------------------------------------------
        # COMBINE SEGMENTS
        # ----------------------------------------------------

        text_parts = []

        for segment in segments:

            segment_text = segment.text.strip()

            if segment_text:

                text_parts.append(
                    segment_text
                )


        text = " ".join(text_parts).strip()


        return text


    finally:

        # ----------------------------------------------------
        # DELETE TEMP FILE
        # ----------------------------------------------------

        if temp_path and os.path.exists(temp_path):

            try:

                os.remove(temp_path)

            except Exception:

                pass
```
