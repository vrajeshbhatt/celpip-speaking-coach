# Pitfalls Research: CELPIP Speaking Coach

## Pitfall 1: Overloading 4GB VRAM
**Risk:** HIGH
**Warning signs:** CUDA out-of-memory errors, model loading failures, system freezing
**Prevention:**
- Use `faster-whisper` with `small` model (not `medium` or `large`)
- Load models once at startup, reuse across requests
- Process audio in 30-second chunks (Whisper's native segment size)
- Never load multiple large models simultaneously
- Monitor VRAM usage during development
**Phase:** Phase 1 (foundation)

## Pitfall 2: Inaccurate Pronunciation Scoring
**Risk:** HIGH
**Warning signs:** Scores don't correlate with actual pronunciation quality, user frustration
**Prevention:**
- Don't rely solely on Whisper confidence scores — they measure recognizability, not pronunciation quality
- Use Parselmouth for acoustic analysis (pitch stability, formant analysis, speech rate)
- Calibrate scoring against known CELPIP level descriptors
- Build scoring rubric based on official CELPIP criteria, not generic speech metrics
- Allow manual score adjustment during calibration phase
**Phase:** Phase 3-4 (speech analysis + scoring)

## Pitfall 3: Wrong Audio Format from Browser
**Risk:** MEDIUM
**Warning signs:** Transcription errors, garbled audio, model crashes
**Prevention:**
- Browser MediaRecorder outputs WebM/Opus by default — convert to WAV/PCM before processing
- Set explicit audio constraints: mono, 16kHz sample rate
- Validate audio quality before sending to analysis pipeline
- Handle browser microphone permission denials gracefully
**Phase:** Phase 1-2 (audio pipeline + frontend)

## Pitfall 4: Generic Feedback That Doesn't Help
**Risk:** HIGH
**Warning signs:** Feedback like "improve pronunciation" without specifics, user can't act on it
**Prevention:**
- Map every feedback point to a specific moment in the recording
- Provide examples: "You said 'wor-ld' — try 'wurld' with a smooth transition"
- Include CLB 10 benchmark descriptions so users know the target
- Focus on 2-3 most impactful improvements per response, not exhaustive list
- Use template-based feedback initially (more reliable than LLM-generated)
**Phase:** Phase 4 (scoring engine)

## Pitfall 5: Not Matching Real CELPIP Experience
**Risk:** MEDIUM
**Warning signs:** Practice doesn't transfer to actual test, unfamiliar format
**Prevention:**
- Research exact CELPIP task instructions and present them verbatim-style
- Match official timing precisely (30s prep / 60-90s response)
- Include the practice task (Task 0) in full test mode
- Present tasks in the same order as the real test
- Don't add features that make it "easier" than the real test
**Phase:** Phase 2 (task engine)

## Pitfall 6: WebSocket Connection Instability
**Risk:** LOW-MEDIUM
**Warning signs:** Audio drops, partial recordings, connection timeouts
**Prevention:**
- Implement reconnection logic on the frontend
- Also record audio locally in browser as backup (save to IndexedDB)
- Send audio as complete file after recording, not streaming (simpler, more reliable)
- Add connection status indicator in UI
**Phase:** Phase 1 (audio pipeline)

## Pitfall 7: Scope Creep into Other CELPIP Sections
**Risk:** MEDIUM
**Warning signs:** "While we're at it, let's add listening practice too"
**Prevention:**
- Keep focus laser-sharp on Speaking only
- Architecture should not accommodate non-speaking features
- If user requests other sections, recommend separate project
**Phase:** All phases (discipline)
