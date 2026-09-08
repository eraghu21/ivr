# 🌾 Agriculture IVR Simulator — Upgraded Model 1

This is an upgraded Streamlit simulator for the SIH agriculture platform.

## New in this version
- Browser microphone button using `streamlit-mic-recorder`
- English + Tamil speech input
- Seven IVR menu options
- Text input fallback
- WAV/MP3/M4A/OGG/WebM upload fallback
- Cached Faster-Whisper model for repeated use
- Agriculture intent detection
- Tamil/English responses
- Text-to-speech response
- Conversation history
- Clean dashboard/status panel
- Architecture ready for a future real telephone IVR layer

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud
Set the main file to `app.py` and deploy the complete repository.

> The weather and market values are intentionally DEMO DATA. Replace them with verified live agriculture/weather APIs before production use.
