import os
from google.cloud import texttospeech, aiplatform

PROJECT = os.getenv("GCP_PROJECT")
REGION = os.getenv("GCP_REGION", "us-central1")
MODEL = os.getenv("VERTEX_LLM_MODEL", "gemini-1.5-pro")

def generate_text(prompt: str) -> str:
    model = aiplatform.TextGenerationModel.from_pretrained(MODEL)
    response = model.predict(prompt, max_output_tokens=800)
    return response.text

def synthesize_tts(locale: str, text: str) -> bytes:
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=locale)
    audio_cfg = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_cfg)
    return response.audio_content