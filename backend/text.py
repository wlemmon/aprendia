
from src.prompts import build_new_story_prompt, build_translation_prompt

print(build_new_story_prompt(
    'en-us',
    'es-co',
    'a1',
    '2',
    'cats',
    'monologue',
    3,
    10
))

from src.gemini_client import generate_text
src = generate_text(build_new_story_prompt(
    'en-us',
    'es-co',
    'a1',
    '2',
    'cats',
    'monologue',
    3,
    10
))
print(src)
tgt = generate_text(build_translation_prompt(src, 
    'en-us',
    'es-co',
    
))
print(tgt)