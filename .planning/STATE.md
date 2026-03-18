---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: unknown
last_updated: "2026-03-18T01:24:17.369Z"
progress:
  total_phases: 7
  completed_phases: 1
  total_plans: 3
  completed_plans: 3
---

# Project State: CELPIP Speaking Coach

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-17)

**Core value:** Accurately simulate CELPIP Speaking exam and provide real feedback on every scoring dimension
**Current focus:** Phase 4 — Scoring & Feedback Engine (Major Overhaul)

## Current Phase

**Phase 4: Scoring & Feedback Engine**
- Status: In progress
- Requirements: SCOR-01 through SCOR-05, FEED-01 through FEED-05
- Plans: Rewrite scoring with official CELPIP rubric alignment, make stricter

## Phase History

### Phase 1: Foundation & Audio Pipeline ✓
- FastAPI backend with Whisper transcription pipeline
- Audio upload, WAV conversion, transcription working
- Code: `app.py`

### Phase 2: CELPIP Task Engine ✓
- All 8 tasks with correct timing and 33 prompts
- Practice mode and full test mode implemented
- Code: `data/celpip_tasks.py`

### Phase 3: Speech Analysis Engine ✓
- Parselmouth prosody analysis, librosa spectral features
- Fluency analysis, content analysis, pronunciation scoring
- Code: `speech_analyzer.py`

### Phase 4: Scoring & Feedback Engine — IN PROGRESS
- Initial scoring engine exists but too lenient
- Overhauling with official CELPIP rubric research
- Code: `scoring_engine.py`

### Phase 5: Frontend UI — Code exists, needs review
- HTML/CSS/JS frontend with task flow, timers, recording
- Code: `static/`

### Phase 6: Progress Tracking — Code exists, needs verification
- SQLite storage, history and progress APIs
- Code: Part of `app.py`

## Key Context

- System: Windows 11, GTX 1050 Ti 4GB, Python 3.14, PyTorch 2.10
- Stack: FastAPI + faster-whisper + Parselmouth + vanilla HTML/CSS/JS + SQLite
- Mode: YOLO (auto-approve)
- Granularity: Standard (6 phases)

---
*Last updated: 2026-03-17 — scoring overhaul in progress*
