"""
Gemini prompt templates for story chapter and quiz generation.
"""

def build_new_story_prompt(
    source_locale: str,
    target_locale: str,
    language_level: str,
    age_level: str,
    topic: str,
    conversation_type: str,
    min_sentence_length: int,
    max_sentence_length: int
) -> str:
    """
    Build a prompt for creating the first chapter of a new story.
    
    Returns a prompt that instructs Gemini to create a story chapter with
    sentences in the format: "source_text|target_text"
    """
    
    conversation_type_descriptions = {
        "internal_dialogue": "internal dialogue (thoughts of a single character)",
        "narration": "narration for observer's language acquisition (describing events)",
        "third_person": "story told from 3rd person omniscient narrator",
        "dialogue": "dialogue between two people"
    }
    
    age_level_descriptions = {
        "toddler": "toddler (ages 2-3)",
        "pre_school": "pre-school (ages 4-5)",
        "middle_school": "middle school (ages 11-14)",
        "high_school": "high school (ages 15-18)",
        "college": "college (ages 18+)"
    }
    
    conv_desc = conversation_type_descriptions.get(conversation_type, conversation_type)
    age_desc = age_level_descriptions.get(age_level, age_level)
    
    prompt = f"""Create the first chapter of a unique, interesting story for language learning.

REQUIREMENTS:
- Language level: {language_level} (CEFR)
- Target audience age: {age_desc}
- Topic: {topic}
- Story format: {conv_desc}
- Source language: {source_locale}
- Target language: {target_locale}
- Sentence length: {min_sentence_length} to {max_sentence_length} words per sentence
- The story should be grounded in real-life scenarios
- Make it engaging and suitable for spanning multiple chapters

OUTPUT FORMAT:
- Each sentence on a separate line
- Format: source_text|target_text
- Example: "Hello, how are you?|Hola, ¿cómo estás?"
- Create 8-12 sentences for this chapter
- Ensure vocabulary and grammar are appropriate for {language_level} level

Create a story that will help the learner practice new vocabulary and grammar at the {language_level} level.
"""
    
    return prompt


def build_next_chapter_prompt(
    previous_story_text: str,
    source_locale: str,
    target_locale: str,
    language_level: str,
    age_level: str,
    topic: str,
    conversation_type: str,
    min_sentence_length: int,
    max_sentence_length: int
) -> str:
    """
    Build a prompt for creating the next chapter of an existing story.
    
    Returns a prompt that instructs Gemini to continue the story.
    """
    
    conversation_type_descriptions = {
        "internal_dialogue": "internal dialogue (thoughts of a single character)",
        "narration": "narration for observer's language acquisition (describing events)",
        "third_person": "story told from 3rd person omniscient narrator",
        "dialogue": "dialogue between two people"
    }
    
    age_level_descriptions = {
        "toddler": "toddler (ages 2-3)",
        "pre_school": "pre-school (ages 4-5)",
        "middle_school": "middle school (ages 11-14)",
        "high_school": "high school (ages 15-18)",
        "college": "college (ages 18+)"
    }
    
    conv_desc = conversation_type_descriptions.get(conversation_type, conversation_type)
    age_desc = age_level_descriptions.get(age_level, age_level)
    
    prompt = f"""Continue the following story with the next chapter.

PREVIOUS STORY:
{previous_story_text}

REQUIREMENTS FOR NEXT CHAPTER:
- Language level: {language_level} (CEFR)
- Target audience age: {age_desc}
- Topic: {topic}
- Story format: {conv_desc}
- Source language: {source_locale}
- Target language: {target_locale}
- Sentence length: {min_sentence_length} to {max_sentence_length} words per sentence
- Continue the story naturally from where it left off
- Introduce new vocabulary and grammar appropriate for {language_level} level

OUTPUT FORMAT:
- Each sentence on a separate line
- Format: source_text|target_text
- Example: "Hello, how are you?|Hola, ¿cómo estás?"
- Create 8-12 sentences for this chapter
- Maintain consistency with the previous story

Create the next chapter that continues the narrative and helps the learner practice new vocabulary and grammar.
"""
    
    return prompt


def build_quiz_prompt(
    chapter_sentences: list,
    target_locale: str,
    language_level: str
) -> str:
    """
    Build a prompt for creating a quiz from a chapter.
    
    Returns a prompt that instructs Gemini to create 5 cloze-style fill-in-the-blank
    questions to test vocabulary and grammar from the chapter.
    
    Args:
        chapter_sentences: List of tuples (source_text, target_text)
        target_locale: The target language locale
        language_level: CEFR level (A1, A2, B1, B2)
    """
    
    # Format sentences for the prompt
    sentences_text = "\n".join([f"- {src} | {tgt}" for src, tgt in chapter_sentences])
    
    prompt = f"""Create a quiz to test vocabulary and grammar from the following chapter.

CHAPTER SENTENCES:
{sentences_text}

REQUIREMENTS:
- Create exactly 5 cloze-style fill-in-the-blank questions
- Questions should test NEW vocabulary or grammar introduced in this chapter
- All questions and answers must be in {target_locale} only
- Questions should closely mirror sentences from the chapter
- Make questions conversational and natural
- Language level: {language_level}

QUESTION FORMAT EXAMPLES:
1. If sentence is "Let's put the drawing on the refrigerator"
   Question: "Let's put the drawing on the what?"
   Answer: "the refrigerator"

2. If sentence is "'I'm a little busy today.' John said."
   Question: "'I'm a little busy today.' John <BLANK>."
   Answer: "said"

OUTPUT FORMAT:
- Each question-answer pair on a separate line
- Format: question|answer
- Example: "Let's put the drawing on the what?|the refrigerator"
- Create exactly 5 question-answer pairs
- Focus on testing the most important vocabulary and grammar from the chapter

Create 5 quiz questions now:
"""
    
    return prompt
