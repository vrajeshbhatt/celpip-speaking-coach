# CELPIP Speaking Coach

A local-first, AI-powered CELPIP Speaking test preparation tool that acts as a full instructor and invigilator. It simulates all 8 CELPIP Speaking tasks with realistic timing, records and directly analyzes speech audio, transcribes for content evaluation, scores on all official CELPIP criteria, and provides actionable coaching feedback to help achieve a 10+ score.

## 🎯 Core Value
Accurately simulate the CELPIP Speaking exam experience and provide real, constructive feedback on every official scoring dimension so users can identify weaknesses and systematically improve to CLB 10+.

## ✨ Features
- **Full Test Simulation:** Simulates all 8 CELPIP Speaking tasks + 1 practice task with exact official timing (prep time and speaking time).
- **Stricter, Official Scoring:** AI grading aligns with official CELPIP level descriptors (3-12) evaluating Content/Coherence, Vocabulary, Listenability, and Task Fulfillment.
- **Deep Speech Analysis:** Analyzes pronunciation, fluency, intonation, speech rhythm, self-corrections, and categorized pauses.
- **Academic Vocabulary Tracking:** Detects academic word list (AWL) usage and discourse marker sophistication.
- **Actionable Coaching:** Provides level-specific advice and calculates the point gap to reach CLB 10.
- **Local-First Architecture:** Ensures privacy by running transcription (Whisper) and analysis locally without paid APIs.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- FFmpeg (for audio processing)

### Installation & Running

Use the provided one-click launcher (Windows):
```bat
run.bat
```
*This will automatically setup the virtual environment, install dependencies from `requirements.txt`, and start the FastAPI server.*

Alternatively, run manually:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open `http://localhost:8000` in your web browser to start practicing.

## 🏗️ Architecture
See [ARCHITECTURE.md](ARCHITECTURE.md) for a deep dive into the technical stack, speech analysis pipeline, and scoring engine design.

## 📝 Roadmap
- [x] Phase 1-2: Foundation & Audio Pipeline
- [x] Phase 3: Speech Analysis Engine
- [x] Phase 4: Scoring & Feedback Engine
- [x] Phase 5: Frontend UI & Experience
- [x] Phase 6: Progress Tracking
- [x] Phase 7: Fetch New Tasks API
- [ ] Phase 8: LLM API Integration (Optional future enhancement)

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

## 📄 License
This project is for educational and personal use.
