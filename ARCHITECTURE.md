# CELPIP Speaking Coach - Architecture

## Technology Stack
- **Backend**: FastAPI (Python 3.10+)
- **Audio Processing**: FFmpeg, pydub, librosa, parselmouth (Praat)
- **Speech-to-Text**: faster-whisper (local, no paid API)
- **Database**: SQLite (local session and progress tracking)
- **Frontend**: Vanilla JavaScript + CSS (Glassmorphism UI, Responsive)

## System Flow

1. **Frontend Capture**: The browser records user audio (WebM) during simulated task timings.
2. **Audio Conversion**: The FastAPI backend converts WebM to 16kHz WAV format using `pydub`.
3. **Transcription**: The audio is transcribed locally using `faster-whisper`, extracting the full text and word-level timestamps.
4. **Speech Analysis Pipeline**:
    - **Fluency & Rhythm**: `librosa` and `parselmouth` analyze the waveform to calculate articulation rate, speech rhythm regularity, and categorize pauses (short/medium/long).
    - **Syntax & Grammar**: `speech_analyzer.py` parses the transcript for structural complexity (subordinate clauses, conditionals, passive voice, sentence starters) and self-corrections using regex.
    - **Pronunciation**: Word confidence from Whisper serves as a baseline proxy for pronunciation clarity.
5. **Scoring Engine**:
    - `scoring_engine.py` applies a strict rubric aligned with official CELPIP level descriptors (CLB 3-12).
    - **Content/Coherence**: Evaluates length, vocabulary diversity, and discourse marker sophistication (basic/intermediate/advanced tiers).
    - **Vocabulary**: Detects usage of words from the Academic Word List (AWL) and calculates Type-Token Ratio (TTR).
    - **Listenability**: Penalizes excessive filler words, long pauses, and rewards strong rhythm and articulation rate.
    - **Task Fulfillment**: Checks the transcript against task-specific must-have and bonus action keywords.
6. **Feedback Generation**: Generates explicit coaching advice, highlighting improvement priorities out of 10.
7. **Storage**: The session, transcript, scores, and feedback are saved in `data/celpip_coach.db`.

## Extensibility
The architecture is designed to be local-first for privacy and cost reasons. However, a single integration point exists in the scoring pipeline to plug in an LLM API (like Gemini or OpenAI) to provide semantic grading on top of the lexical rules engine if desired in the future.
