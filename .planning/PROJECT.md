# CELPIP Speaking Coach

## What This Is

A local-first, AI-powered CELPIP Speaking test preparation tool that acts as a full instructor and invigilator. It simulates all 8 CELPIP Speaking tasks with realistic timing, records and directly analyzes speech audio (pronunciation, fluency, intonation), transcribes for content evaluation, scores on all official CELPIP criteria, and provides actionable coaching feedback to help achieve a 10+ score.

## Core Value

Accurately simulate the CELPIP Speaking exam experience and provide real, constructive feedback on every official scoring dimension so the user can identify weaknesses and systematically improve to 10+.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Simulate all 8 CELPIP Speaking tasks with official timing and format
- [ ] Record speech audio via microphone in the browser
- [ ] Analyze speech audio directly for pronunciation, fluency, intonation, and pacing
- [ ] Transcribe speech for content/vocabulary/coherence analysis
- [ ] Score responses on all official CELPIP speaking criteria (Content/Coherence, Vocabulary, Listenability, Task Fulfillment)
- [ ] Provide detailed, constructive feedback with specific improvement tips
- [ ] Act as an invigilator — present tasks, manage timing, enforce test conditions
- [ ] Generate realistic CELPIP-style prompts for each task type
- [ ] Support full test simulation (all 8 tasks back-to-back) and individual task practice
- [ ] Track progress over time to show improvement trends
- [ ] Run entirely locally (no paid API dependencies for core functionality)
- [ ] Future-ready architecture for LLM API integration (Gemini, etc.)

### Out of Scope

- Mobile app — web-first, mobile later
- Listening/Reading/Writing sections — speaking only
- Multi-user/social features — personal prep tool
- Paid API requirement for core functionality — must work free/locally

## Context

- **Target user:** The developer themselves, preparing for CELPIP Speaking test
- **Goal score:** 10+ (out of 12) on CELPIP Speaking
- **System:** Windows 11, Intel CPU, 16GB RAM, NVIDIA GTX 1050 Ti (4GB VRAM)
- **Available tools:** Python 3.14, PyTorch 2.10, Node 22
- **CELPIP Speaking has 8 tasks:** Giving Advice, Talking about a Personal Experience, Describing a Scene, Making Predictions, Comparing and Persuading, Dealing with a Difficult Situation, Expressing Opinions, Describing an Unusual Situation
- **Each task has specific prep time (30-60s) and speaking time (60-90s)**
- **Local-first approach:** Use Whisper for transcription, local pronunciation analysis models, with architecture ready for future LLM API enhancement
- **Deployment:** Local first, with future plan to deploy as web service

## Constraints

- **GPU:** GTX 1050 Ti with 4GB VRAM — models must fit within this
- **Cost:** Free for core functionality — no paid API dependencies
- **Tech:** Python backend + web frontend, local AI models
- **Privacy:** All speech data stays local on the machine

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Local-first with future API hook | Free tool, privacy, no dependency on external services | — Pending |
| Direct audio analysis + transcription | User wants speech quality evaluation, not just text grading | — Pending |
| Web app (browser-based UI) | Natural for audio capture, cross-platform potential, easy to deploy later | — Pending |
| Whisper for transcription | Best open-source STT, runs on GTX 1050 Ti (small/medium model) | — Pending |

---
*Last updated: 2026-03-17 after initialization*
