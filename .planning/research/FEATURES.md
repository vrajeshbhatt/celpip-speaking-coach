# Features Research: CELPIP Speaking Coach

## Table Stakes (must-have or users leave)

### Test Simulation
- **All 8 CELPIP speaking tasks** with correct format and instructions
- **Official timing** — prep time (30-60s) and response time (60-90s) per task
- **Task-specific prompts** that mirror real exam scenarios
- **Audio recording** with visual countdown timer
- **Complexity:** Medium | **Dependencies:** None

### Scoring & Feedback
- **4-dimension scoring** matching official CELPIP criteria:
  - Content/Coherence — idea relevance, organization, development
  - Vocabulary — word range, accuracy, appropriateness
  - Listenability — pronunciation, intonation, rhythm, grammar
  - Task Fulfillment — completeness, tone, relevance
- **Score on CELPIP scale** (M, 1-12) for each dimension
- **Overall score** with CLB level equivalent
- **Specific feedback per dimension** — not just scores but WHY
- **Complexity:** High | **Dependencies:** Speech analysis engine

### Audio Analysis
- **Direct speech analysis** — pronunciation, fluency, pacing from audio signal
- **Transcription** for content/vocabulary evaluation
- **Pause detection** — identify unnatural silences
- **Speech rate measurement** — words per minute
- **Complexity:** High | **Dependencies:** ML models

## Differentiators (competitive advantage)

### Coaching Intelligence
- **Targeted improvement tips** based on weak dimensions
- **Example model answers** for each task type
- **Score comparison** to CLB 10 benchmark descriptors
- **Practice recommendations** — which tasks to focus on
- **Complexity:** Medium | **Dependencies:** Scoring engine

### Progress Tracking
- **Score history** across practice sessions
- **Trend visualization** — are you improving?
- **Dimension-specific progress** — track each scoring criterion
- **Session comparison** — compare recent vs. past performance
- **Complexity:** Low | **Dependencies:** Database

### Full Test Mode
- **Complete exam simulation** — all 8 tasks back-to-back
- **Continuous timing** like real test (~20 minutes)
- **End-of-test summary scorecard**
- **Complexity:** Medium | **Dependencies:** Task simulation

### Practice Mode
- **Pick individual tasks** to drill repeatedly
- **Randomized prompts** within each task type
- **Difficulty progression** based on current score
- **Complexity:** Low | **Dependencies:** Task simulation

## Anti-Features (deliberately NOT building)

- **Video recording** — CELPIP is audio-only, video adds complexity without value
- **Multiplayer/social** — personal prep tool, not a platform
- **Writing/Reading/Listening prep** — speaking only, clear scope
- **Real-time interruption** — let user complete response before analyzing
- **Gamification** — focus on practical improvement, not badges
