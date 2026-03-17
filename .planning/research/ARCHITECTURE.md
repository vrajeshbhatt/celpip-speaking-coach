# Architecture Research: CELPIP Speaking Coach

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    BROWSER (Frontend)                        │
│  ┌───────────┐  ┌──────────┐  ┌───────────┐  ┌──────────┐ │
│  │ Task UI   │  │ Timer    │  │ Audio     │  │ Results  │ │
│  │ Engine    │  │ Manager  │  │ Recorder  │  │ Display  │ │
│  └─────┬─────┘  └────┬─────┘  └─────┬─────┘  └────┬─────┘ │
│        │              │              │              │       │
│        └──────────────┴──────┬───────┴──────────────┘       │
│                              │ WebSocket                    │
└──────────────────────────────┼──────────────────────────────┘
                               │
┌──────────────────────────────┼──────────────────────────────┐
│                    FASTAPI SERVER (Backend)                   │
│                              │                               │
│  ┌───────────────────────────┴───────────────────────────┐  │
│  │                   API Gateway                          │  │
│  │  /ws/record  /api/tasks  /api/results  /api/progress  │  │
│  └───┬──────────────┬─────────────┬──────────────┬───────┘  │
│      │              │             │              │           │
│  ┌───┴───┐    ┌─────┴────┐  ┌────┴────┐   ┌────┴────┐     │
│  │Speech │    │ Task     │  │Scoring  │   │Progress │     │
│  │Engine │    │ Manager  │  │ Engine  │   │Tracker  │     │
│  └───┬───┘    └──────────┘  └────┬────┘   └─────────┘     │
│      │                           │                          │
│  ┌───┴──────────────────────┐    │                          │
│  │   Audio Analysis Pipeline │    │                          │
│  │  ┌──────────┐            │    │                          │
│  │  │faster-   │ Transcribe │    │                          │
│  │  │whisper   │────────────┼────┤                          │
│  │  └──────────┘            │    │                          │
│  │  ┌──────────┐            │    │                          │
│  │  │Parsel-   │ Prosody    │    │                          │
│  │  │mouth     │────────────┼────┘                          │
│  │  └──────────┘            │                               │
│  │  ┌──────────┐            │                               │
│  │  │librosa   │ Features   │                               │
│  │  └──────────┘            │                               │
│  └──────────────────────────┘                               │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              LLM Interface (Pluggable)                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │   │
│  │  │ Local    │  │ Gemini   │  │ Custom Model     │   │   │
│  │  │ Rules   │  │ API      │  │ (future)         │   │   │
│  │  └──────────┘  └──────────┘  └──────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────┐                                           │
│  │   SQLite DB   │ Sessions, scores, progress               │
│  └──────────────┘                                           │
└──────────────────────────────────────────────────────────────┘
```

## Component Boundaries

### Frontend (Browser)
- **Task UI Engine** — renders task prompts, instructions, manages task flow
- **Timer Manager** — countdown timers for prep/response time
- **Audio Recorder** — captures microphone audio via MediaRecorder API, streams via WebSocket
- **Results Display** — shows scores, feedback, charts, progress

### Backend (FastAPI)
- **API Gateway** — REST + WebSocket endpoints
- **Speech Engine** — orchestrates audio analysis pipeline
- **Task Manager** — serves CELPIP task prompts, manages task sequences
- **Scoring Engine** — maps analysis results to CELPIP scoring criteria
- **Progress Tracker** — stores and retrieves score history
- **LLM Interface** — pluggable module for content analysis (local rules → API later)

### Audio Analysis Pipeline
- **faster-whisper** — speech-to-text transcription
- **Parselmouth** — prosody analysis (pitch, intensity, formants, speech rate)
- **librosa** — audio feature extraction (MFCCs, spectral features)
- Pipeline runs sequentially: record → transcribe → analyze → score → feedback

## Data Flow

1. Browser captures audio → streams to backend via WebSocket
2. Backend saves audio file temporarily
3. faster-whisper transcribes audio → text
4. Parselmouth analyzes audio signal → prosody features
5. librosa extracts audio features → spectral data
6. Scoring engine combines transcript + prosody + features → CELPIP scores
7. LLM interface generates feedback text
8. Results sent back to browser via REST response
9. Scores persisted to SQLite

## Suggested Build Order

1. **Phase 1:** Project foundation — backend setup, audio pipeline, basic transcription
2. **Phase 2:** CELPIP task engine — all 8 tasks with prompts and timing
3. **Phase 3:** Speech analysis — pronunciation, fluency, prosody analysis
4. **Phase 4:** Scoring engine — map analysis to CELPIP criteria, generate feedback
5. **Phase 5:** Frontend UI — task flow, recording, timer, results display
6. **Phase 6:** Progress tracking — database, history, trend visualization
7. **Phase 7:** Polish — coaching tips, model answers, full test mode
