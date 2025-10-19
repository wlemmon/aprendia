import hashlib, os
from pathlib import Path

AUDIO_BASE = "./app/static_audio"

def text_hash_filename(locale: str, text: str) -> str:
    h = hashlib.sha256((locale + text).encode()).hexdigest()[:16]
    return f"{locale}_{h}.mp3"

def ensure_audio_path(locale: str):
    p = Path(AUDIO_BASE) / locale
    p.mkdir(parents=True, exist_ok=True)
    return p

def save_audio_bytes(locale: str, text: str, audio_bytes: bytes) -> str:
    p = ensure_audio_path(locale)
    fname = text_hash_filename(locale, text)
    fpath = p / fname
    with open(fpath, "wb") as f:
        f.write(audio_bytes)
    return str(fpath)