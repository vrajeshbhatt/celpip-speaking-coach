# Research Summary: CELPIP Speaking Coach

## Stack Decision
**Python FastAPI + faster-whisper + Parselmouth + vanilla HTML/CSS/JS + SQLite**

FastAPI provides async WebSocket support for real-time audio. faster-whisper (CTranslate2) runs the `small` model within GTX 1050 Ti's 4GB VRAM at ~4x speed vs vanilla Whisper. Parselmouth (Praat wrapper) handles prosody analysis. No frontend framework needed — vanilla JS with MediaRecorder API for audio capture. SQLite for zero-config local storage.

## Table Stakes
- All 8 CELPIP speaking tasks with official timing (30-60s prep, 60-90s response)
- Audio recording and direct speech analysis
- 4-dimension scoring matching official CELPIP criteria (Content/Coherence, Vocabulary, Listenability, Task Fulfillment)
- Specific actionable feedback per dimension
- Score on CELPIP scale (M-12) with CLB level equivalent

## Key Differentiators
- **Direct audio analysis** — not just STT but pronunciation, fluency, intonation from the audio signal
- **CLB 10 benchmark comparison** — shows exactly what 10+ performance looks like
- **Progress tracking** — score trends over time per dimension
- **Full test + practice modes** — simulate real exam or drill individual tasks

## Watch Out For
1. **4GB VRAM limit** — must use faster-whisper `small` model, load once, process in chunks
2. **Pronunciation scoring accuracy** — Whisper confidence ≠ pronunciation quality; need Parselmouth acoustic analysis
3. **Browser audio format** — MediaRecorder outputs WebM/Opus, must convert to WAV before analysis
4. **Generic feedback trap** — feedback must be specific and actionable, tied to moments in recording
5. **Not matching real CELPIP** — timing, format, instructions must mirror actual test exactly

## Architecture Insight
Pipeline architecture: Record → Save WAV → Transcribe (faster-whisper) → Analyze prosody (Parselmouth) → Extract features (librosa) → Score (custom engine) → Generate feedback → Display results. LLM interface is pluggable: starts with rule-based scoring, upgrades to API-based coaching later.
