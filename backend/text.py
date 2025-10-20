
from src.prompts import build_new_story_prompt, build_translation_prompt

from dotenv import load_dotenv
load_dotenv()

from src.gemini_client import generate_text
src="i like cats"
print(src)
tgt = generate_text(build_translation_prompt(src, 
    'en-us',
    'es-co',
))
print(tgt)