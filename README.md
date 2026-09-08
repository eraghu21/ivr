# 🌾 Agriculture IVR Simulator

A Streamlit prototype for an SIH agriculture platform. It simulates an IVR/voice assistant using:

- English + Tamil menu
- Text-based IVR queries
- Optional speech-to-text using faster-whisper
- Text-to-speech using gTTS
- Demo modules for weather, market price, schemes, irrigation, fertilizer and crop disease
- Conversation history

## Run locally

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

## Streamlit Cloud

1. Upload all files to a GitHub repository.
2. Open Streamlit Community Cloud.
3. Select the repository and `app.py`.
4. Deploy.
5. The first Whisper transcription can take time because the model may need to download.

## Important

The weather and market values in `agriculture_data.py` are DEMO DATA. They are not live agricultural prices/weather and must be replaced by verified official/current APIs before real deployment.

## Suggested next version

For the real telephone IVR, keep `ivr_engine.py` and `agriculture_data.py` as the core logic, and replace the Streamlit microphone/upload layer with a telephony/SIP layer.
