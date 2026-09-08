import io

def speak_text(text, language="English"):
    """
    Generates MP3 using gTTS.
    Requires internet access on the running server.
    """
    from gtts import gTTS
    lang = "ta" if language == "தமிழ்" else "en"
    buf = io.BytesIO()
    gTTS(text=text, lang=lang).write_to_fp(buf)
    buf.seek(0)
    return buf.read()
