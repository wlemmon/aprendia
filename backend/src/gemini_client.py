import os
from google.cloud import texttospeech

import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Image

# from google.oauth2 import service_account

# PROJECT = os.getenv("GCP_PROJECT")
# REGION = os.getenv("GCP_REGION", "us-central1")
import logging

# Initialize the Vertex AI SDK
vertexai.init()
def generate_text(prompt: str) -> str:
    logging.info(f"generate_text: {prompt}")
    model_name = "gemini-2.5-flash"
    model = GenerativeModel(model_name)

    response = model.generate_content(prompt)

    return response.text

def synthesize_tts(locale: str, text: str) -> bytes:
    logging.info(f"synthesize_tts: {text}")
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=locale, model_name='en-US-Chirp3-HD-Leda')
    audio_cfg = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_cfg)
    return response.audio_content


# async def async_tts_gemini(text, filename, lang='en-US'):
#     def helper():
#         return synthesize_tts(lang, text)
#     # Run the blocking TTS call in a thread
#     audio_content = await asyncio.to_thread(helper)

#     # Write the file asynchronously
#     async with aiofiles.open(filename, "wb") as f:
#         await f.write(audio_content)