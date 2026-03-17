# Stack Research: CELPIP Speaking Coach

## Recommended Stack (2025)

### Backend — Python + FastAPI
- **FastAPI** — async web framework with native WebSocket support for real-time audio streaming
- **Python 3.14** — already installed on target system
- **PyTorch 2.10** — already installed, needed for ML models
- **Uvicorn** — ASGI server for FastAPI
- **Confidence:** ★★★★★ (mature, well-documented, perfect fit)

### Speech-to-Text — faster-whisper
- **faster-whisper** (CTranslate2-based) — 4x faster than vanilla Whisper, uses significantly less VRAM
- **Model:** `small` or `base` for GTX 1050 Ti (4GB VRAM) — `small` is ~2GB VRAM, good accuracy
- **Alternative:** `distil-whisper` for even faster inference with minimal accuracy loss
- **NOT:** vanilla openai-whisper (too slow and memory-hungry for 4GB VRAM)
- **Confidence:** ★★★★★ (proven on similar hardware)

### Audio Analysis — Parselmouth + librosa
- **Parselmouth** (Python wrapper for Praat) — gold standard for phonetic analysis: pitch, formants, intensity, speech rate, pause detection, intonation contours
- **librosa** — audio feature extraction (MFCCs, spectral features, rhythm analysis)
- **pyAudioAnalysis** — additional audio classification and segmentation
- **Confidence:** ★★★★☆ (requires custom scoring logic on top)

### Pronunciation Assessment
- **Goodness of Pronunciation (GOP)** algorithm — custom implementation using Whisper's token probabilities
- **Parselmouth** — prosody analysis (intonation, stress, rhythm)
- **Custom scoring engine** — map acoustic features to CELPIP criteria
- **Confidence:** ★★★☆☆ (novel integration, needs iterative tuning)

### Frontend — Vanilla HTML/CSS/JS
- **HTML5 + CSS3 + JavaScript** — browser-based UI
- **MediaRecorder API** — browser audio capture
- **WebSocket API** — real-time audio streaming to backend
- **Chart.js** — progress tracking and score visualization
- **Confidence:** ★★★★★ (no framework overhead, direct control)

### Data Storage — SQLite
- **SQLite** — local database for session history, scores, progress tracking
- **JSON files** — CELPIP task prompts and scoring rubrics
- **Confidence:** ★★★★★ (zero-config, local-first)

### Future LLM Integration (planned)
- **Google Gemini API** (free tier) — content quality analysis, coaching feedback generation
- **Ollama + local LLM** — alternative local option for content analysis
- **Architecture:** Abstract LLM interface to swap between local/API models

## What NOT to Use
- **React/Vue/Angular** — overkill for this use case, adds build complexity
- **vanilla Whisper** — too slow for 4GB VRAM
- **Cloud STT APIs** — violates local-first requirement
- **Django** — too heavyweight, no native WebSocket support
- **PostgreSQL/MySQL** — unnecessary for single-user local app
