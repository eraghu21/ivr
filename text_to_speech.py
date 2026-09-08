import io

def speak_text(text, language="English"):
    from gtts import gTTS
    lang = "ta" if language == "தமிழ்" else "en"
    buf = io.BytesIO()
    gTTS(text=text, lang=lang).write_to_fp(buf)
    return buf.getvalue()
