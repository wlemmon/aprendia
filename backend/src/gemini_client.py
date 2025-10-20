import os
from google.cloud import texttospeech

import json
import tempfile

def setup_google_credentials():
    creds_json = os.getenv("GCP_CREDENTIALS_JSON")
    if creds_json:
        data = json.loads(creds_json)
        # Write to a temp file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            json.dump(data, f)
            f.flush()
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f.name
        print(f"✅ Loaded Google credentials from env into {f.name}")
    else:
        print("⚠️ GCP_CREDENTIALS_JSON not found. Using default creds (will fail outside GCP).")

setup_google_credentials()

import google.auth
creds, project = google.auth.default()
print(f"✅ Authenticated as {creds.service_account_email}, project={project}")

import vertexai
from vertexai.preview.generative_models import GenerativeModel 
import asyncio
import aiofiles
import logging
import json

# from google.oauth2 import service_account
PROJECT = os.getenv("GCP_PROJECT")
# credentials_json = os.environ.get("GCP_CREDENTIALS_JSON")

# if credentials_json:
#     # Load the JSON string into a Python object
#     info = json.loads(credentials_json)
    
#     # Create the credentials object from the info dictionary
#     credentials = service_account.Credentials.from_service_account_info(info)
   
# else:
#     cred_file=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
#     credentials = service_account.Credentials.from_service_account_file(cred_file)
# PROJECT = os.getenv("GCP_PROJECT")
REGION = os.getenv("GCP_REGION", "us-central1")
vertexai.init(project=PROJECT, location=REGION)#, credentials=credentials)



# Initialize the Vertex AI SDK
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


async def async_tts_gemini(text, filename, lang='en-US'):
    def helper():
        return synthesize_tts(lang, text)
    # Run the blocking TTS call in a thread
    audio_content = await asyncio.to_thread(helper)

    # Write the file asynchronously
    async with aiofiles.open(filename, "wb") as f:
        await f.write(audio_content)