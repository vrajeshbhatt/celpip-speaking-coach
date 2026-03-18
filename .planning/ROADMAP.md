# Roadmap: CELPIP Speaking Coach

**Created:** 2026-03-17
**Phases:** 6
**Requirements:** 33 mapped
**Granularity:** Standard

## Phase 1: Foundation & Audio Pipeline
**Goal:** Set up the project infrastructure, backend server, audio recording in browser, and local speech-to-text transcription.

**Requirements:** FOUND-01, FOUND-02, FOUND-03, FOUND-04

**Success Criteria:**
1. FastAPI server starts and serves a basic HTML page on localhost
2. Browser can record audio from microphone and send to backend
3. Backend receives audio, saves as WAV file
4. faster-whisper transcribes the audio and returns text
5. End-to-end: speak → record → transcribe → display transcript

---

## Phase 2: CELPIP Task Engine
**Goal:** Implement all 8 CELPIP speaking tasks with realistic prompts, official timing, and both practice and full test modes.

**Requirements:** TASK-01, TASK-02, TASK-03, TASK-04, TASK-05, TASK-06

**Success Criteria:**
1. All 8 CELPIP task types are defined with correct instructions and timing
2. Each task has at least 3 varied prompts
3. Countdown timers work for both prep time and response time
4. Practice mode lets user select and repeat individual tasks
5. Full test mode runs all 8 tasks sequentially (~20 minutes)

---

## Phase 3: Speech Analysis Engine
**Goal:** Build the audio analysis pipeline that evaluates pronunciation, fluency, intonation, vocabulary, coherence, and task fulfillment.

**Requirements:** SPCH-01, SPCH-02, SPCH-03, SPCH-04, SPCH-05, SPCH-06

**Success Criteria:**
1. Parselmouth extracts prosody features (pitch, intensity, speech rate, pauses)
2. Pronunciation quality scored from acoustic signal (not just transcript)
3. Fluency metrics calculated: words/minute, pause ratio, filler words
4. Vocabulary range and accuracy evaluated from transcript
5. Content coherence assessed: idea count, logical structure, detail quality
6. Task fulfillment measured: relevance, completeness, tone appropriateness

---

## Phase 4: Scoring & Feedback Engine
**Goal:** Map analysis results to all 4 official CELPIP scoring dimensions, generate scores on the CELPIP scale, and produce actionable feedback.

**Requirements:** SCOR-01, SCOR-02, SCOR-03, SCOR-04, SCOR-05, FEED-01, FEED-02, FEED-03, FEED-04, FEED-05

**Success Criteria:**
1. Each response scored on all 4 CELPIP dimensions (Content/Coherence, Vocabulary, Listenability, Task Fulfillment)
2. Scores mapped to CELPIP scale (M, 1-12) with CLB equivalents
3. Dimension-specific feedback explains strengths and areas to improve
4. Feedback is specific and actionable (not generic)
5. Model answer provided for comparison after each response
6. Transcript displayed alongside feedback

---

## Phase 5: Frontend UI & Experience
**Goal:** Build a polished, test-like interface with task flow, recording controls, timers, and score dashboard.

**Requirements:** UI-01, UI-02, UI-03, UI-04, UI-05

**Success Criteria:**
1. Clean interface that feels like a real test-taking experience
2. Visual countdown timers animate smoothly during prep and response
3. Recording indicator clearly shows when microphone is active
4. Score dashboard displays all 4 dimensions with visual breakdown
5. Fully responsive on desktop browsers
6. Smooth transitions between tasks, recording, and results views

---

## Phase 6: Progress Tracking & Polish
**Goal:** Add persistent score tracking, progress visualization, trend charts, and final polish for a complete coaching experience.

**Requirements:** PROG-01, PROG-02, PROG-03, PROG-04

**Success Criteria:**
1. Session scores saved to SQLite database
2. Score history page shows all past sessions
3. Charts visualize score trends over time
4. Per-dimension progress tracked separately
5. Overall coaching dashboard shows improvement areas

### Phase 7: Comprehensive CELPIP Tasks and Analysis Upgrades

**Goal:** [To be planned]
**Requirements**: TBD
**Depends on:** Phase 6
**Plans:** 0 plans

Plans:
- [ ] TBD (run /gsd-plan-phase 7 to break down)

### Phase 8: Advanced Scoring Engine Evaluation

**Goal:** [To be planned]
**Requirements**: TBD
**Depends on:** Phase 7
**Plans:** 0 plans

Plans:
- [ ] TBD (run /gsd-plan-phase 8 to break down)

---
*Roadmap created: 2026-03-17*
*Last updated: 2026-03-17 after initial creation*
