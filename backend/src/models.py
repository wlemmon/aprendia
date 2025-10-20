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
# db = {
#     "stories": {},  # story_id -> Story
#     "studiables": {},  # studiable_id -> Studiable
#     "sentences": {},  # sentence_id -> SentencePair
# }

db = {'stories': 
{1: Story(id=1, title='Cats in space', source_locale='en_us', target_locale='es_co', metadata={'language_level': 'A1', 'age_level': '2', 'topic': 'running arrands'})}, 'studiables': {1: Studiable(id=1, story_id=1, title='Chapter 1', raw_text='Leo wakes up. Hello, Leo!\nMama has a big bag.\nWe go out today.\nTime to go to the store.\nWe need some food.\nWe need milk. We need bread.\nSee the big car?\nLeo sits in the car.\nMama drives the car.\nVroom, vroom! We go now.\nHello, big store!Leo se despierta. ¡Hola, Leo!\nMamá tiene una bolsa grande.\nHoy salimos.\nEs hora de ir a la tienda.\nNecesitamos comida.\nNecesitamos leche. Necesitamos pan.\n¿Ves el carro grande?\nLeo se sienta en el carro.\nMamá maneja el carro.\n¡Brum, brum! Ya nos vamos.\n¡Hola, tienda grande!', metadata={'type': 'chapter', 'chapter_number': 1, 'language_level': 'A1', 'age_level': '2', 'topic': 'running arrands', 'conversation_type': 'narrating activities to help toddler acquire language', 'min_sentence_length': 3, 'max_sentence_length': 10}, sentences=[SentencePair(id=1, source_text='Leo wakes up. Hello, Leo!', target_text='Leo se despierta. ¡Hola, Leo!', source_audio='/audio/en_us/en_us_bbcf64896f664e3d.mp3', target_audio='/audio/es_co/es_co_db2725d767342dd6.mp3', order=0), SentencePair(id=2, source_text='Mama has a big bag.', target_text='Mamá tiene una bolsa grande.', source_audio='/audio/en_us/en_us_4217de3553e80006.mp3', target_audio='/audio/es_co/es_co_32cd6f4103c3623c.mp3', order=1), SentencePair(id=3, source_text='We go out today.', target_text='Hoy salimos.', source_audio='/audio/en_us/en_us_f4106bd67478919c.mp3', target_audio='/audio/es_co/es_co_556ba82ba99dcf7b.mp3', order=2), SentencePair(id=4, source_text='Time to go to the store.', target_text='Es hora de ir a la tienda.', source_audio='/audio/en_us/en_us_f32eecb8b8b7ca98.mp3', target_audio='/audio/es_co/es_co_69f09d282aa72d18.mp3', order=3), SentencePair(id=5, source_text='We need some food.', target_text='Necesitamos comida.', source_audio='/audio/en_us/en_us_18029daf631857b5.mp3', target_audio='/audio/es_co/es_co_1c3c2bdd84a7ad1b.mp3', order=4), SentencePair(id=6, source_text='We need milk. We need bread.', target_text='Necesitamos leche. Necesitamos pan.', source_audio='/audio/en_us/en_us_05b6a623d557d7cb.mp3', target_audio='/audio/es_co/es_co_fc995fe84ce3ffb6.mp3', order=5), SentencePair(id=7, source_text='See the big car?', target_text='¿Ves el carro grande?', source_audio='/audio/en_us/en_us_950ede652a745a36.mp3', target_audio='/audio/es_co/es_co_4764eed2c014fa67.mp3', order=6), SentencePair(id=8, source_text='Leo sits in the car.', target_text='Leo se sienta en el carro.', source_audio='/audio/en_us/en_us_6229ed47045849fc.mp3', target_audio='/audio/es_co/es_co_4bdf889fcdf8c836.mp3', order=7), SentencePair(id=9, source_text='Mama drives the car.', target_text='Mamá maneja el carro.', source_audio='/audio/en_us/en_us_6d224dfaea00eef2.mp3', target_audio='/audio/es_co/es_co_5f124f5362536125.mp3', order=8), SentencePair(id=10, source_text='Vroom, vroom! We go now.', target_text='¡Brum, brum! Ya nos vamos.', source_audio='/audio/en_us/en_us_4764981b688c1484.mp3', target_audio='/audio/es_co/es_co_8d1d9a566a49ff74.mp3', order=9), SentencePair(id=11, source_text='Hello, big store!', target_text='¡Hola, tienda grande!', source_audio='/audio/en_us/en_us_782d654356d21351.mp3', target_audio='/audio/es_co/es_co_5b639f6fa67561ce.mp3', order=10)])}, 'sentences': {1: SentencePair(id=1, source_text='Leo wakes up. Hello, Leo!', target_text='Leo se despierta. ¡Hola, Leo!', source_audio='/audio/en_us/en_us_bbcf64896f664e3d.mp3', target_audio='/audio/es_co/es_co_db2725d767342dd6.mp3', order=0), 2: SentencePair(id=2, source_text='Mama has a big bag.', target_text='Mamá tiene una bolsa grande.', source_audio='/audio/en_us/en_us_4217de3553e80006.mp3', target_audio='/audio/es_co/es_co_32cd6f4103c3623c.mp3', order=1), 3: SentencePair(id=3, source_text='We go out today.', target_text='Hoy salimos.', source_audio='/audio/en_us/en_us_f4106bd67478919c.mp3', target_audio='/audio/es_co/es_co_556ba82ba99dcf7b.mp3', order=2), 4: SentencePair(id=4, source_text='Time to go to the store.', target_text='Es hora de ir a la tienda.', source_audio='/audio/en_us/en_us_f32eecb8b8b7ca98.mp3', target_audio='/audio/es_co/es_co_69f09d282aa72d18.mp3', order=3), 5: SentencePair(id=5, source_text='We need some food.', target_text='Necesitamos comida.', source_audio='/audio/en_us/en_us_18029daf631857b5.mp3', target_audio='/audio/es_co/es_co_1c3c2bdd84a7ad1b.mp3', 
order=4), 6: SentencePair(id=6, source_text='We need milk. We need bread.', target_text='Necesitamos leche. Necesitamos pan.', source_audio='/audio/en_us/en_us_05b6a623d557d7cb.mp3', target_audio='/audio/es_co/es_co_fc995fe84ce3ffb6.mp3', order=5), 7: SentencePair(id=7, source_text='See the big car?', target_text='¿Ves el carro grande?', source_audio='/audio/en_us/en_us_950ede652a745a36.mp3', target_audio='/audio/es_co/es_co_4764eed2c014fa67.mp3', order=6), 8: SentencePair(id=8, source_text='Leo sits in the car.', target_text='Leo se sienta en el carro.', source_audio='/audio/en_us/en_us_6229ed47045849fc.mp3', target_audio='/audio/es_co/es_co_4bdf889fcdf8c836.mp3', order=7), 9: SentencePair(id=9, source_text='Mama drives the car.', target_text='Mamá maneja el carro.', source_audio='/audio/en_us/en_us_6d224dfaea00eef2.mp3', target_audio='/audio/es_co/es_co_5f124f5362536125.mp3', order=8), 10: SentencePair(id=10, source_text='Vroom, vroom! We go now.', target_text='¡Brum, brum! Ya nos vamos.', source_audio='/audio/en_us/en_us_4764981b688c1484.mp3', target_audio='/audio/es_co/es_co_8d1d9a566a49ff74.mp3', order=9), 11: SentencePair(id=11, source_text='Hello, big store!', target_text='¡Hola, tienda grande!', source_audio='/audio/en_us/en_us_782d654356d21351.mp3', target_audio='/audio/es_co/es_co_5b639f6fa67561ce.mp3', order=10)}}

def reset_db():
    for key in db:
        db[key].clear()