# Requirements: CELPIP Speaking Coach

**Defined:** 2026-03-17
**Core Value:** Accurately simulate the CELPIP Speaking exam and provide real feedback on every official scoring dimension to help achieve 10+

## v1 Requirements

### Foundation

- [ ] **FOUND-01**: Backend API server starts and serves frontend on localhost
- [ ] **FOUND-02**: Audio recording works in browser with microphone permission handling
- [ ] **FOUND-03**: Audio is sent to backend and saved as WAV file
- [ ] **FOUND-04**: Speech-to-text transcription works locally using faster-whisper

### Task Engine

- [ ] **TASK-01**: All 8 CELPIP speaking tasks are available with correct instructions
- [ ] **TASK-02**: Each task displays appropriate preparation time countdown (30-60s)
- [ ] **TASK-03**: Each task displays response recording time countdown (60-90s)
- [ ] **TASK-04**: Task prompts are realistic and varied (multiple prompts per task type)
- [ ] **TASK-05**: Practice mode allows selecting any individual task to drill
- [ ] **TASK-06**: Full test mode runs all 8 tasks sequentially with correct timing

### Speech Analysis

- [ ] **SPCH-01**: Pronunciation quality is assessed from audio signal (not just transcript)
- [ ] **SPCH-02**: Fluency is measured — speech rate, pause frequency, filler words
- [ ] **SPCH-03**: Intonation and pitch patterns are analyzed
- [ ] **SPCH-04**: Vocabulary range and accuracy are evaluated from transcript
- [ ] **SPCH-05**: Content coherence and idea organization are evaluated from transcript
- [ ] **SPCH-06**: Task fulfillment is evaluated — relevance, completeness, tone

### Scoring

- [ ] **SCOR-01**: Responses scored on 4 CELPIP dimensions (Content/Coherence, Vocabulary, Listenability, Task Fulfillment)
- [ ] **SCOR-02**: Each dimension scored on CELPIP scale (M, 1-12)
- [ ] **SCOR-03**: Overall composite score calculated
- [ ] **SCOR-04**: CLB level equivalent displayed alongside scores
- [ ] **SCOR-05**: Score benchmarked against CLB 10 descriptors

### Feedback

- [ ] **FEED-01**: Specific feedback provided for each scoring dimension
- [ ] **FEED-02**: Feedback includes what was done well and what to improve
- [ ] **FEED-03**: Improvement tips are actionable (specific, not generic)
- [ ] **FEED-04**: Model answer examples provided for each task type
- [ ] **FEED-05**: Transcript displayed alongside feedback for reference

### Frontend UI

- [ ] **UI-01**: Clean, intuitive interface that mirrors test-taking experience
- [ ] **UI-02**: Visual countdown timers for prep and response time
- [ ] **UI-03**: Audio recording indicator (microphone active/inactive)
- [ ] **UI-04**: Score dashboard with dimension breakdown
- [ ] **UI-05**: Responsive design that works on desktop browsers

### Progress Tracking

- [ ] **PROG-01**: Session scores saved to local database
- [ ] **PROG-02**: Score history viewable across sessions
- [ ] **PROG-03**: Progress trends visualized with charts
- [ ] **PROG-04**: Per-dimension progress tracking over time

## v2 Requirements

### LLM Integration

- **LLM-01**: Pluggable LLM interface for enhanced content analysis
- **LLM-02**: Gemini API integration for coaching feedback
- **LLM-03**: AI-generated personalized study plans

### Advanced Analysis

- **ADV-01**: Phoneme-level pronunciation analysis
- **ADV-02**: Grammar error detection and correction
- **ADV-03**: Vocabulary suggestion engine

### Deployment

- **DEPL-01**: Deployable as web service
- **DEPL-02**: User authentication and accounts
- **DEPL-03**: Cloud-based speech processing option

## Out of Scope

| Feature | Reason |
|---------|--------|
| Listening/Reading/Writing sections | Speaking-only tool, clear scope boundary |
| Mobile app | Web-first, mobile responsive later |
| Video recording | CELPIP is audio-only |
| Multi-user/social features | Personal prep tool |
| Real-time streaming analysis | Analyze after recording completes (simpler, more reliable) |
| Paid API dependency | Core must work free/locally |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| FOUND-01 | Phase 1 | Pending |
| FOUND-02 | Phase 1 | Pending |
| FOUND-03 | Phase 1 | Pending |
| FOUND-04 | Phase 1 | Pending |
| TASK-01 | Phase 2 | Pending |
| TASK-02 | Phase 2 | Pending |
| TASK-03 | Phase 2 | Pending |
| TASK-04 | Phase 2 | Pending |
| TASK-05 | Phase 2 | Pending |
| TASK-06 | Phase 2 | Pending |
| SPCH-01 | Phase 3 | Pending |
| SPCH-02 | Phase 3 | Pending |
| SPCH-03 | Phase 3 | Pending |
| SPCH-04 | Phase 3 | Pending |
| SPCH-05 | Phase 3 | Pending |
| SPCH-06 | Phase 3 | Pending |
| SCOR-01 | Phase 4 | Pending |
| SCOR-02 | Phase 4 | Pending |
| SCOR-03 | Phase 4 | Pending |
| SCOR-04 | Phase 4 | Pending |
| SCOR-05 | Phase 4 | Pending |
| FEED-01 | Phase 4 | Pending |
| FEED-02 | Phase 4 | Pending |
| FEED-03 | Phase 4 | Pending |
| FEED-04 | Phase 4 | Pending |
| FEED-05 | Phase 4 | Pending |
| UI-01 | Phase 5 | Pending |
| UI-02 | Phase 5 | Pending |
| UI-03 | Phase 5 | Pending |
| UI-04 | Phase 5 | Pending |
| UI-05 | Phase 5 | Pending |
| PROG-01 | Phase 6 | Pending |
| PROG-02 | Phase 6 | Pending |
| PROG-03 | Phase 6 | Pending |
| PROG-04 | Phase 6 | Pending |

**Coverage:**
- v1 requirements: 33 total
- Mapped to phases: 33
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-17*
*Last updated: 2026-03-17 after initial definition*
