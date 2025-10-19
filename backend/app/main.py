from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import itertools

from .models import db, Story, Studiable, SentencePair
from .gemini_client import generate_text, synthesize_tts
from .tts import save_audio_bytes
from .prompts import build_new_story_prompt, build_next_chapter_prompt, build_quiz_prompt

app = FastAPI(title="Aprendia API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for audio
os.makedirs("static_audio", exist_ok=True)
app.mount("/audio", StaticFiles(directory="static_audio"), name="audio")

# Counters for IDs
story_counter = itertools.count(1)
studiable_counter = itertools.count(1)
sentence_counter = itertools.count(1)


# Request/Response Models
class CreateStoryRequest(BaseModel):
    title: str
    source_locale: str
    target_locale: str
    language_level: str
    age_level: str
    topic: str
    conversation_type: str
    min_sentence_length: int
    max_sentence_length: int


class CreateStudiableRequest(BaseModel):
    type: str  # "chapter" or "quiz"
    language_level: Optional[str] = None
    age_level: Optional[str] = None
    topic: Optional[str] = None
    conversation_type: Optional[str] = None
    min_sentence_length: Optional[int] = None
    max_sentence_length: Optional[int] = None
    parent_studiable_id: Optional[int] = None  # For quizzes, the chapter ID


# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/")
def root():
    return {"message": "Aprendia API", "version": "1.0.0"}


# Story endpoints
@app.post("/stories")
def create_story(request: CreateStoryRequest, background_tasks: BackgroundTasks):
    """
    Create a new story with chapter 1.
    This endpoint creates the story and immediately starts generating chapter 1.
    """
    story_id = next(story_counter)
    story = Story(
        id=story_id,
        title=request.title,
        source_locale=request.source_locale,
        target_locale=request.target_locale,
        metadata={
            "language_level": request.language_level,
            "age_level": request.age_level,
            "topic": request.topic,
        }
    )
    db["stories"][story_id] = story
    
    # Create chapter 1
    studiable_id = next(studiable_counter)
    studiable = Studiable(
        id=studiable_id,
        story_id=story_id,
        title="Chapter 1",
        raw_text="",
        metadata={
            "type": "chapter",
            "chapter_number": 1,
            "language_level": request.language_level,
            "age_level": request.age_level,
            "topic": request.topic,
            "conversation_type": request.conversation_type,
            "min_sentence_length": request.min_sentence_length,
            "max_sentence_length": request.max_sentence_length,
        }
    )
    db["studiables"][studiable_id] = studiable
    
    # Process chapter 1 in background
    background_tasks.add_task(
        process_chapter,
        studiable,
        story,
        request.language_level,
        request.age_level,
        request.topic,
        request.conversation_type,
        request.min_sentence_length,
        request.max_sentence_length,
        None  # No previous story for chapter 1
    )
    
    return {
        "story": story,
        "chapter_id": studiable_id,
        "status": "processing"
    }


@app.get("/stories")
def list_stories():
    """Get all stories."""
    return list(db["stories"].values())


@app.get("/stories/{story_id}")
def get_story(story_id: int):
    """Get a specific story."""
    story = db["stories"].get(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


# Studiable endpoints
@app.post("/stories/{story_id}/studiables")
def create_studiable(
    story_id: int,
    request: CreateStudiableRequest,
    background_tasks: BackgroundTasks
):
    """
    Create a new studiable (chapter or quiz) for a story.
    """
    story = db["stories"].get(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    studiable_id = next(studiable_counter)
    
    if request.type == "chapter":
        # Get existing chapters to determine chapter number
        existing_chapters = [
            s for s in db["studiables"].values()
            if s.story_id == story_id and s.metadata.get("type") == "chapter"
        ]
        chapter_number = len(existing_chapters) + 1
        
        studiable = Studiable(
            id=studiable_id,
            story_id=story_id,
            title=f"Chapter {chapter_number}",
            raw_text="",
            metadata={
                "type": "chapter",
                "chapter_number": chapter_number,
                "language_level": request.language_level,
                "age_level": request.age_level,
                "topic": request.topic,
                "conversation_type": request.conversation_type,
                "min_sentence_length": request.min_sentence_length,
                "max_sentence_length": request.max_sentence_length,
            }
        )
        db["studiables"][studiable_id] = studiable
        
        # Get previous story text for continuation
        previous_story = "\n".join([
            s.raw_text for s in existing_chapters if s.raw_text
        ])
        
        background_tasks.add_task(
            process_chapter,
            studiable,
            story,
            request.language_level,
            request.age_level,
            request.topic,
            request.conversation_type,
            request.min_sentence_length,
            request.max_sentence_length,
            previous_story if previous_story else None
        )
        
    elif request.type == "quiz":
        # Get the parent chapter
        parent_studiable = db["studiables"].get(request.parent_studiable_id)
        if not parent_studiable:
            raise HTTPException(status_code=404, detail="Parent chapter not found")
        
        studiable = Studiable(
            id=studiable_id,
            story_id=story_id,
            title=f"Quiz for {parent_studiable.title}",
            raw_text="",
            metadata={
                "type": "quiz",
                "parent_studiable_id": request.parent_studiable_id,
                "language_level": parent_studiable.metadata.get("language_level"),
            }
        )
        db["studiables"][studiable_id] = studiable
        
        background_tasks.add_task(
            process_quiz,
            studiable,
            story,
            parent_studiable
        )
    
    else:
        raise HTTPException(status_code=400, detail="Invalid studiable type")
    
    return {
        "studiable_id": studiable_id,
        "status": "processing"
    }


@app.get("/stories/{story_id}/studiables")
def list_studiables(story_id: int):
    """Get all studiables (chapters and quizzes) for a story."""
    story = db["stories"].get(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    studiables = [
        s for s in db["studiables"].values()
        if s.story_id == story_id
    ]
    
    return studiables


@app.get("/studiables/{studiable_id}")
def get_studiable(studiable_id: int):
    """Get a specific studiable with its sentences."""
    studiable = db["studiables"].get(studiable_id)
    if not studiable:
        raise HTTPException(status_code=404, detail="Studiable not found")
    
    # Get sentences for this studiable
    sentences = [
        s for s in db["sentences"].values()
        if s.id in [sent.id for sent in studiable.sentences]
    ]
    
    return {
        "id": studiable.id,
        "story_id": studiable.story_id,
        "title": studiable.title,
        "metadata": studiable.metadata,
        "sentences": sentences
    }


# Background processing functions
def process_chapter(
    studiable: Studiable,
    story: Story,
    language_level: str,
    age_level: str,
    topic: str,
    conversation_type: str,
    min_sentence_length: int,
    max_sentence_length: int,
    previous_story: Optional[str]
):
    """Process a chapter: generate text, create sentences, generate audio."""
    try:
        # Build prompt
        if previous_story:
            prompt = build_next_chapter_prompt(
                previous_story,
                story.source_locale,
                story.target_locale,
                language_level,
                age_level,
                topic,
                conversation_type,
                min_sentence_length,
                max_sentence_length
            )
        else:
            prompt = build_new_story_prompt(
                story.source_locale,
                story.target_locale,
                language_level,
                age_level,
                topic,
                conversation_type,
                min_sentence_length,
                max_sentence_length
            )
        
        # Generate story text
        result = generate_text(prompt)
        studiable.raw_text = result
        
        # Parse sentences and generate audio
        sentences = []
        for order, line in enumerate(result.splitlines()):
            line = line.strip()
            if not line or "|" not in line:
                continue
            
            parts = line.split("|", 1)
            if len(parts) != 2:
                continue
            
            src, tgt = [x.strip() for x in parts]
            if not src or not tgt:
                continue
            
            # Generate TTS audio
            src_bytes = synthesize_tts(story.source_locale, src)
            tgt_bytes = synthesize_tts(story.target_locale, tgt)
            
            # Save audio files
            src_path = save_audio_bytes(story.source_locale, src, src_bytes)
            tgt_path = save_audio_bytes(story.target_locale, tgt, tgt_bytes)
            
            # Create sentence pair
            sid = next(sentence_counter)
            sp = SentencePair(
                id=sid,
                source_text=src,
                target_text=tgt,
                source_audio=src_path,
                target_audio=tgt_path,
                order=order
            )
            db["sentences"][sid] = sp
            sentences.append(sp)
        
        studiable.sentences = sentences
        
    except Exception as e:
        print(f"Error processing chapter: {e}")
        studiable.metadata["error"] = str(e)


def process_quiz(
    studiable: Studiable,
    story: Story,
    parent_studiable: Studiable
):
    """Process a quiz: generate questions from chapter, create sentences, generate audio."""
    try:
        # Get chapter sentences
        chapter_sentences = [
            (s.source_text, s.target_text)
            for s in parent_studiable.sentences
        ]
        
        if not chapter_sentences:
            raise Exception("Parent chapter has no sentences")
        
        # Build quiz prompt
        language_level = parent_studiable.metadata.get("language_level", "A1")
        prompt = build_quiz_prompt(
            chapter_sentences,
            story.target_locale,
            language_level
        )
        
        # Generate quiz questions
        result = generate_text(prompt)
        studiable.raw_text = result
        
        # Parse questions and generate audio
        sentences = []
        for order, line in enumerate(result.splitlines()):
            line = line.strip()
            if not line or "|" not in line:
                continue
            
            parts = line.split("|", 1)
            if len(parts) != 2:
                continue
            
            question, answer = [x.strip() for x in parts]
            if not question or not answer:
                continue
            
            # Generate TTS audio (both in target language)
            question_bytes = synthesize_tts(story.target_locale, question)
            answer_bytes = synthesize_tts(story.target_locale, answer)
            
            # Save audio files
            question_path = save_audio_bytes(story.target_locale, question, question_bytes)
            answer_path = save_audio_bytes(story.target_locale, answer, answer_bytes)
            
            # Create sentence pair (question as target, answer as source for consistency)
            sid = next(sentence_counter)
            sp = SentencePair(
                id=sid,
                source_text=answer,  # Answer shown on back
                target_text=question,  # Question shown on front
                source_audio=answer_path,
                target_audio=question_path,
                order=order
            )
            db["sentences"][sid] = sp
            sentences.append(sp)
        
        studiable.sentences = sentences
        
    except Exception as e:
        print(f"Error processing quiz: {e}")
        studiable.metadata["error"] = str(e)
