from gtts import gTTS
from io import BytesIO


def text_to_speech(text, language="en"):
    """
    Convert text into MP3 audio.

    language:
        en = English
        ta = Tamil
    """

    if not text:
        return None

    try:
        # Create MP3 in memory
        audio_buffer = BytesIO()

        tts = gTTS(
            text=text,
            lang=language,
            slow=False
        )

        tts.write_to_fp(audio_buffer)

        audio_buffer.seek(0)

        return audio_buffer.getvalue()

    except Exception as e:
        print("Text-to-speech error:", e)
        return None
