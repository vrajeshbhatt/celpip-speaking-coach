import random
from prompts_generator import generator
"""
CELPIP Speaking Coach â€” Main Application
FastAPI backend with audio recording, transcription, and speech analysis.
"""

import os
import json
import uuid
import wave
import struct
import sqlite3
import asyncio
from datetime import datetime
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "recordings"
DB_PATH = BASE_DIR / "data" / "celpip_coach.db"
STATIC_DIR = BASE_DIR / "static"
TASKS_DIR = BASE_DIR / "data" / "tasks"

# Whisper model - use 'base' for 4GB VRAM safety, 'small' for better accuracy
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "auto")  # auto detects GPU

# ---------------------------------------------------------------------------
# Global model reference (loaded once at startup)
# ---------------------------------------------------------------------------
whisper_model = None


def init_db():
    """Initialize SQLite database for session tracking."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            task_type TEXT NOT NULL,
            task_number INTEGER,
            prompt TEXT,
            transcript TEXT,
            audio_path TEXT,
            scores TEXT,
            feedback TEXT,
            created_at TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_runs (
            id TEXT PRIMARY KEY,
            mode TEXT NOT NULL,
            total_score REAL,
            dimension_scores TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def load_whisper():
    """Load faster-whisper model (once at startup)."""
    global whisper_model
    try:
        from faster_whisper import WhisperModel
        device = WHISPER_DEVICE
        if device == "auto":
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"
        whisper_model = WhisperModel(
            WHISPER_MODEL,
            device=device,
            compute_type=compute_type
        )
        print(f"[OK] Whisper '{WHISPER_MODEL}' loaded on {device} ({compute_type})")
    except Exception as e:
        print(f"[WARN] Whisper load failed: {e}")
        print("  Transcription will be unavailable. Install: pip install faster-whisper")
        whisper_model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    # Startup
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "data").mkdir(parents=True, exist_ok=True)
    init_db()
    load_whisper()
    print("=" * 55)
    print(" CELPIP Speaking Coach -- Ready")
    print(f" http://localhost:8000")
    print("=" * 55)
    yield
    # Shutdown
    print("CELPIP Speaking Coach â€” Shutting down")


# ---------------------------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="CELPIP Speaking Coach",
    description="AI-powered CELPIP Speaking test preparation tool",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Static files & frontend
# ---------------------------------------------------------------------------
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the main application page."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return HTMLResponse("<h1>CELPIP Speaking Coach</h1><p>Frontend not found. Place index.html in /static/</p>")


# ---------------------------------------------------------------------------
# Task Management API
# ---------------------------------------------------------------------------
@app.get("/api/tasks")
async def get_all_tasks():
    """Get all available CELPIP speaking tasks."""
    from data.celpip_tasks import CELPIP_TASKS
    return {"tasks": CELPIP_TASKS}


@app.get("/api/tasks/full-test")
async def get_full_test():
    """Get all 8 tasks for a full test simulation."""
    from data.celpip_tasks import get_full_test_sequence
    return {"tasks": get_full_test_sequence()}

@app.get("/api/tasks/{task_number}")
async def get_task(task_number: int):
    """Get a specific CELPIP speaking task with a random prompt."""
    from data.celpip_tasks import get_task_with_prompt
    task = get_task_with_prompt(task_number)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_number} not found")
    return task


@app.post("/api/tasks/generate")
async def generate_new_tasks(task_number: int = None, topic: str = None):
    """Fetch/generate new practice prompts for the task library.
    Supports optional task_number and topic for more specific generation.
    """
    from data.celpip_tasks import CELPIP_TASKS

    # Simulate API delay for UX
    await asyncio.sleep(2)

    # Use the robust generator
    new_prompt = generator.generate_prompt(task_number, topic)
    
    # Assign to a specific task (if task_number provided) or a random one
    target_task_num = task_number or random.choice([1, 2, 7])
    
    for task in CELPIP_TASKS:
        if task["number"] == target_task_num:
            task["prompts"].append(new_prompt)
            return {"status": "success", "message": f"Successfully generated a fresh practice prompt about '{new_prompt['topic']}' and added it to Task {target_task_num}: {task['name']}!"}

    return {"status": "error", "message": f"Task {target_task_num} not found to add new prompt to."}


# ---------------------------------------------------------------------------
# Audio Upload & Transcription API
# ---------------------------------------------------------------------------
@app.post("/api/audio/upload")
async def upload_audio(audio: UploadFile = File(...), task_type: str = "practice", task_number: int = 1, prompt: str = ""):
    """Upload audio recording for analysis."""
    session_id = str(uuid.uuid4())
    
    # Save the uploaded audio
    audio_filename = f"{session_id}.webm"
    audio_path = UPLOAD_DIR / audio_filename
    
    content = await audio.read()
    with open(audio_path, "wb") as f:
        f.write(content)
    
    # Convert to WAV for analysis
    wav_path = UPLOAD_DIR / f"{session_id}.wav"
    try:
        from pydub import AudioSegment
        audio_segment = AudioSegment.from_file(str(audio_path))
        audio_segment = audio_segment.set_channels(1).set_frame_rate(16000)
        audio_segment.export(str(wav_path), format="wav")
    except Exception as e:
        # If pydub fails, try to use the file directly  
        wav_path = audio_path
        print(f"[WARN] Audio conversion warning: {e}")
    
    # Transcribe
    transcript = ""
    word_timestamps = []
    if whisper_model:
        try:
            segments, info = whisper_model.transcribe(
                str(wav_path),
                beam_size=5,
                word_timestamps=True,
                language="en"
            )
            for segment in segments:
                transcript += segment.text + " "
                if segment.words:
                    for word in segment.words:
                        word_timestamps.append({
                            "word": word.word.strip(),
                            "start": round(word.start, 2),
                            "end": round(word.end, 2),
                            "probability": round(word.probability, 3)
                        })
            transcript = transcript.strip()
        except Exception as e:
            print(f"[WARN] Transcription error: {e}")
            transcript = "[Transcription failed]"
    else:
        transcript = "[Whisper model not loaded â€” install faster-whisper]"
    
    # Analyze speech
    analysis = {}
    try:
        from speech_analyzer import analyze_speech
        analysis = analyze_speech(str(wav_path), transcript, word_timestamps)
    except Exception as e:
        print(f"[WARN] Speech analysis error: {e}")
        analysis = {"error": str(e)}
    
    # Score the response
    scores = {}
    feedback = {}
    try:
        from scoring_engine import score_response
        scores, feedback = score_response(analysis, transcript, task_number, prompt)
    except Exception as e:
        print(f"[WARN] Scoring error: {e}")
        scores = {"error": str(e)}
        feedback = {"error": str(e)}
    
    # Save session to database
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sessions (id, task_type, task_number, prompt, transcript, audio_path, scores, feedback, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id, task_type, task_number, prompt, transcript,
            str(audio_path), json.dumps(scores), json.dumps(feedback),
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[WARN] Database error: {e}")
    
    return {
        "session_id": session_id,
        "transcript": transcript,
        "word_timestamps": word_timestamps,
        "analysis": analysis,
        "scores": scores,
        "feedback": feedback
    }


# ---------------------------------------------------------------------------
# Progress & History API
# ---------------------------------------------------------------------------
@app.get("/api/history")
async def get_history(limit: int = 20):
    """Get recent practice session history."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, task_type, task_number, prompt, transcript, scores, feedback, created_at
            FROM sessions ORDER BY created_at DESC LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        sessions = []
        for row in rows:
            sessions.append({
                "id": row["id"],
                "task_type": row["task_type"],
                "task_number": row["task_number"],
                "prompt": row["prompt"],
                "transcript": row["transcript"],
                "scores": json.loads(row["scores"]) if row["scores"] else {},
                "feedback": json.loads(row["feedback"]) if row["feedback"] else {},
                "created_at": row["created_at"]
            })
        return {"sessions": sessions}
    except Exception as e:
        return {"sessions": [], "error": str(e)}


@app.get("/api/progress")
async def get_progress():
    """Get progress summary with score trends."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT scores, created_at FROM sessions 
            WHERE scores IS NOT NULL 
            ORDER BY created_at ASC
        """)
        rows = cursor.fetchall()
        conn.close()
        
        progress = []
        for row in rows:
            scores = json.loads(row["scores"]) if row["scores"] else {}
            if scores and "error" not in scores:
                progress.append({
                    "date": row["created_at"],
                    "scores": scores
                })
        
        return {"progress": progress, "total_sessions": len(progress)}
    except Exception as e:
        return {"progress": [], "total_sessions": 0, "error": str(e)}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "whisper_loaded": whisper_model is not None,
        "whisper_model": WHISPER_MODEL,
        "version": "1.0.0"
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)



