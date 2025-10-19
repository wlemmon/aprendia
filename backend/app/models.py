from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class SentencePair:
    id: int
    source_text: str
    target_text: str
    source_audio: str = ""
    target_audio: str = ""
    order: int = 0

@dataclass
class Studiable:
    id: int
    story_id: int
    title: str
    raw_text: str
    metadata: Dict
    sentences: List[SentencePair] = field(default_factory=list)

@dataclass
class Story:
    id: int
    title: str
    source_locale: str
    target_locale: str
    metadata: Dict

# In-memory DB
db = {
    "stories": {},  # story_id -> Story
    "studiables": {},  # studiable_id -> Studiable
    "sentences": {},  # sentence_id -> SentencePair
}

def reset_db():
    for key in db:
        db[key].clear()