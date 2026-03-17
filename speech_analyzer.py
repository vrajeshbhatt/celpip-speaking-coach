"""
Speech Analyzer — Direct audio signal analysis for CELPIP scoring.
Uses Parselmouth (Praat) for prosody and librosa for audio features.
Analyzes pronunciation quality, fluency, intonation, and pacing from the raw audio.
"""

import os
import re
import math
from pathlib import Path

# Try to import analysis libraries — graceful degradation if missing
try:
    import parselmouth
    from parselmouth.praat import call
    HAS_PARSELMOUTH = True
except ImportError:
    HAS_PARSELMOUTH = False
    print("[WARN] Parselmouth not installed. Prosody analysis will be limited.")

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import librosa
    HAS_LIBROSA = True
except ImportError:
    HAS_LIBROSA = False
    print("[WARN] librosa not installed. Audio feature analysis will be limited.")


# ---------------------------------------------------------------------------
# Filler words and hesitation markers
# ---------------------------------------------------------------------------
FILLER_WORDS = {
    "um", "uh", "uhm", "umm", "er", "erm", "ah", "like", "you know",
    "basically", "actually", "literally", "sort of", "kind of",
    "i mean", "right", "okay", "so", "well"
}

# Common mispronunciation indicators (words often said incorrectly by ESL speakers)
COMPLEX_WORDS = {
    "particularly", "comfortable", "temperature", "February",
    "pronunciation", "environment", "restaurant", "vegetable",
    "interesting", "different", "actually", "specific",
    "development", "opportunity", "communication", "experience",
    "necessary", "especially", "unfortunately", "definitely"
}


def analyze_speech(wav_path: str, transcript: str, word_timestamps: list) -> dict:
    """
    Comprehensive speech analysis combining audio signal and transcript.
    
    Returns analysis dict with metrics for all CELPIP scoring dimensions.
    """
    result = {
        "prosody": analyze_prosody(wav_path),
        "fluency": analyze_fluency(transcript, word_timestamps),
        "content": analyze_content(transcript),
        "pronunciation": analyze_pronunciation(word_timestamps, transcript),
        "audio_features": extract_audio_features(wav_path)
    }
    
    return result


def analyze_prosody(wav_path: str) -> dict:
    """
    Analyze prosodic features from audio signal using Parselmouth.
    Measures pitch variation, intensity, speech rate, and intonation.
    """
    if not HAS_PARSELMOUTH:
        return _fallback_prosody()

    try:
        snd = parselmouth.Sound(wav_path)
        duration = snd.get_total_duration()
        
        # Pitch analysis
        pitch = call(snd, "To Pitch", 0.0, 75, 600)
        pitch_values = pitch.selected_array['frequency']
        pitch_values = pitch_values[pitch_values > 0]  # Remove unvoiced frames
        
        pitch_mean = float(np.mean(pitch_values)) if len(pitch_values) > 0 else 0
        pitch_std = float(np.std(pitch_values)) if len(pitch_values) > 0 else 0
        pitch_range = float(np.max(pitch_values) - np.min(pitch_values)) if len(pitch_values) > 0 else 0
        
        # Pitch variation coefficient (higher = more expressive)
        pitch_variation = pitch_std / pitch_mean if pitch_mean > 0 else 0
        
        # Intensity analysis
        intensity = call(snd, "To Intensity", 75, 0, "yes")
        intensity_values = [call(intensity, "Get value in frame", i + 1) for i in range(call(intensity, "Get number of frames"))]
        intensity_values = [v for v in intensity_values if v is not None and not math.isnan(v)]
        
        intensity_mean = float(np.mean(intensity_values)) if intensity_values else 0
        intensity_std = float(np.std(intensity_values)) if intensity_values else 0
        
        # Voice quality — harmonics-to-noise ratio (HNR)
        harmonicity = call(snd, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
        hnr = call(harmonicity, "Get mean", 0, 0)
        
        # Voiced/unvoiced ratio (indicates fluency)
        voiced_frames = len(pitch_values)
        total_frames = call(pitch, "Get number of frames")
        voiced_ratio = voiced_frames / total_frames if total_frames > 0 else 0
        
        return {
            "duration_seconds": round(duration, 2),
            "pitch_mean_hz": round(pitch_mean, 1),
            "pitch_std_hz": round(pitch_std, 1),
            "pitch_range_hz": round(pitch_range, 1),
            "pitch_variation_coeff": round(pitch_variation, 3),
            "intensity_mean_db": round(intensity_mean, 1),
            "intensity_std_db": round(intensity_std, 1),
            "hnr_db": round(hnr, 1) if not math.isnan(hnr) else 0,
            "voiced_ratio": round(voiced_ratio, 3),
            "intonation_quality": _evaluate_intonation(pitch_variation, pitch_range)
        }
    except Exception as e:
        print(f"[WARN] Prosody analysis error: {e}")
        return _fallback_prosody()


def analyze_fluency(transcript: str, word_timestamps: list) -> dict:
    """
    Analyze fluency from transcript and word timing.
    Measures speech rate, pause patterns, filler words, and smoothness.
    """
    words = transcript.lower().split()
    word_count = len(words)
    
    if not word_timestamps or word_count == 0:
        return _fallback_fluency(word_count)
    
    # Duration from timestamps
    total_duration = word_timestamps[-1]["end"] - word_timestamps[0]["start"] if word_timestamps else 0
    
    # Words per minute
    wpm = (word_count / total_duration * 60) if total_duration > 0 else 0
    
    # Pause analysis
    pauses = []
    long_pauses = []
    for i in range(1, len(word_timestamps)):
        gap = word_timestamps[i]["start"] - word_timestamps[i - 1]["end"]
        if gap > 0.3:  # Pause threshold
            pauses.append(gap)
        if gap > 1.0:  # Long pause
            long_pauses.append(gap)
    
    avg_pause = sum(pauses) / len(pauses) if pauses else 0
    total_pause_time = sum(pauses)
    pause_ratio = total_pause_time / total_duration if total_duration > 0 else 0
    
    # Filler words
    filler_count = 0
    for word in words:
        if word.strip(".,!?") in FILLER_WORDS:
            filler_count += 1
    
    filler_ratio = filler_count / word_count if word_count > 0 else 0
    
    # Articulation rate (excluding pauses)
    speaking_time = total_duration - total_pause_time
    articulation_rate = (word_count / speaking_time * 60) if speaking_time > 0 else 0
    
    return {
        "word_count": word_count,
        "duration_seconds": round(total_duration, 2),
        "words_per_minute": round(wpm, 1),
        "articulation_rate": round(articulation_rate, 1),
        "pause_count": len(pauses),
        "long_pause_count": len(long_pauses),
        "avg_pause_duration": round(avg_pause, 2),
        "pause_ratio": round(pause_ratio, 3),
        "filler_word_count": filler_count,
        "filler_ratio": round(filler_ratio, 3),
        "fluency_score": _calculate_fluency_score(wpm, pause_ratio, filler_ratio, len(long_pauses))
    }


def analyze_content(transcript: str) -> dict:
    """
    Analyze content quality from transcript.
    Evaluates vocabulary range, sentence complexity, coherence markers.
    """
    if not transcript or transcript.startswith("["):
        return _fallback_content()
    
    words = transcript.lower().split()
    word_count = len(words)
    
    # Unique words / type-token ratio (vocabulary diversity)
    unique_words = set(w.strip(".,!?;:'\"()") for w in words if len(w.strip(".,!?;:'\"()")) > 0)
    type_token_ratio = len(unique_words) / word_count if word_count > 0 else 0
    
    # Average word length (indicator of vocabulary sophistication)
    clean_words = [w.strip(".,!?;:'\"()") for w in words if len(w.strip(".,!?;:'\"()")) > 0]
    avg_word_length = sum(len(w) for w in clean_words) / len(clean_words) if clean_words else 0
    
    # Long words (6+ characters) — vocabulary range indicator
    long_words = [w for w in clean_words if len(w) >= 6]
    long_word_ratio = len(long_words) / len(clean_words) if clean_words else 0
    
    # Coherence markers (discourse connectors)
    coherence_markers = {
        "firstly", "secondly", "thirdly", "first", "second", "third",
        "however", "therefore", "moreover", "furthermore", "additionally",
        "consequently", "nevertheless", "meanwhile", "although", "because",
        "since", "while", "whereas", "in conclusion", "to summarize",
        "for example", "for instance", "specifically", "in addition",
        "on the other hand", "in my opinion", "i believe", "i think"
    }
    
    transcript_lower = transcript.lower()
    marker_count = sum(1 for m in coherence_markers if m in transcript_lower)
    
    # Sentence detection (rough)
    sentences = re.split(r'[.!?]+', transcript)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences)
    
    # Average sentence length
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else word_count
    
    # Idea density estimation (key points)
    idea_count = max(1, sentence_count)  # At least 1 idea per sentence
    
    return {
        "word_count": word_count,
        "unique_word_count": len(unique_words),
        "type_token_ratio": round(type_token_ratio, 3),
        "avg_word_length": round(avg_word_length, 1),
        "long_word_ratio": round(long_word_ratio, 3),
        "coherence_marker_count": marker_count,
        "sentence_count": sentence_count,
        "avg_sentence_length": round(avg_sentence_length, 1),
        "idea_count": idea_count,
        "vocabulary_range": _evaluate_vocabulary(type_token_ratio, avg_word_length, long_word_ratio),
        "coherence_quality": _evaluate_coherence(marker_count, sentence_count, avg_sentence_length)
    }


def analyze_pronunciation(word_timestamps: list, transcript: str) -> dict:
    """
    Analyze pronunciation quality from Whisper's word-level confidence.
    Low confidence often indicates pronunciation issues.
    """
    if not word_timestamps:
        return {"confidence_mean": 0, "low_confidence_words": [], "pronunciation_score": 5}
    
    confidences = [w["probability"] for w in word_timestamps]
    mean_confidence = sum(confidences) / len(confidences)
    
    # Words with low confidence (potential pronunciation issues)
    low_confidence_words = [
        {"word": w["word"], "confidence": w["probability"]}
        for w in word_timestamps
        if w["probability"] < 0.7 and len(w["word"]) > 2
    ]
    
    # Sort by confidence (lowest first)
    low_confidence_words.sort(key=lambda x: x["confidence"])
    
    # Complex words in transcript
    words_lower = transcript.lower().split()
    complex_used = [w for w in words_lower if w.strip(".,!?") in COMPLEX_WORDS]
    
    return {
        "confidence_mean": round(mean_confidence, 3),
        "confidence_min": round(min(confidences), 3) if confidences else 0,
        "low_confidence_words": low_confidence_words[:10],  # Top 10 problem words
        "complex_words_used": complex_used,
        "pronunciation_score": _calculate_pronunciation_score(mean_confidence, len(low_confidence_words), len(word_timestamps))
    }


def extract_audio_features(wav_path: str) -> dict:
    """
    Extract spectral audio features using librosa.
    """
    if not HAS_LIBROSA or not HAS_NUMPY:
        return {"available": False}
    
    try:
        y, sr = librosa.load(wav_path, sr=16000)
        
        # Spectral centroid (brightness of sound)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        
        # Zero crossing rate (noisiness indicator)
        zcr = librosa.feature.zero_crossing_rate(y)
        
        # RMS energy
        rms = librosa.feature.rms(y=y)
        
        return {
            "available": True,
            "sample_rate": sr,
            "duration": round(len(y) / sr, 2),
            "spectral_centroid_mean": round(float(np.mean(spectral_centroid)), 1),
            "zero_crossing_rate_mean": round(float(np.mean(zcr)), 4),
            "rms_energy_mean": round(float(np.mean(rms)), 4)
        }
    except Exception as e:
        return {"available": False, "error": str(e)}


# ---------------------------------------------------------------------------
# Scoring helper functions
# ---------------------------------------------------------------------------
def _evaluate_intonation(pitch_variation: float, pitch_range: float) -> str:
    """Evaluate intonation quality from pitch metrics."""
    if pitch_variation > 0.25 and pitch_range > 100:
        return "expressive"
    elif pitch_variation > 0.15 and pitch_range > 60:
        return "natural"
    elif pitch_variation > 0.08:
        return "limited"
    else:
        return "monotone"


def _calculate_fluency_score(wpm: float, pause_ratio: float, filler_ratio: float, long_pauses: int) -> float:
    """Calculate fluency score (0-10 scale)."""
    score = 10.0
    
    # WPM penalty (ideal: 120-160 WPM for English speaking)
    if wpm < 80:
        score -= 3.0
    elif wpm < 100:
        score -= 1.5
    elif wpm < 120:
        score -= 0.5
    elif wpm > 200:
        score -= 2.0
    elif wpm > 180:
        score -= 1.0
    
    # Pause ratio penalty
    if pause_ratio > 0.4:
        score -= 3.0
    elif pause_ratio > 0.3:
        score -= 2.0
    elif pause_ratio > 0.2:
        score -= 1.0
    
    # Long pause penalty
    score -= min(long_pauses * 0.5, 2.0)
    
    # Filler word penalty
    if filler_ratio > 0.1:
        score -= 2.0
    elif filler_ratio > 0.05:
        score -= 1.0
    elif filler_ratio > 0.02:
        score -= 0.5
    
    return round(max(1.0, min(10.0, score)), 1)


def _evaluate_vocabulary(ttr: float, avg_length: float, long_ratio: float) -> str:
    """Evaluate vocabulary range."""
    combined = (ttr * 3 + avg_length / 10 + long_ratio * 3) / 3
    if combined > 0.55:
        return "advanced"
    elif combined > 0.4:
        return "good"
    elif combined > 0.25:
        return "adequate"
    else:
        return "limited"


def _evaluate_coherence(markers: int, sentences: int, avg_length: float) -> str:
    """Evaluate coherence quality."""
    marker_ratio = markers / max(sentences, 1)
    if marker_ratio > 0.5 and avg_length > 8:
        return "well-organized"
    elif marker_ratio > 0.25 or avg_length > 10:
        return "adequate"
    elif markers > 0:
        return "basic"
    else:
        return "minimal"


def _calculate_pronunciation_score(mean_conf: float, low_conf_count: int, total_words: int) -> float:
    """Calculate pronunciation score from Whisper confidence."""
    base_score = mean_conf * 10
    
    # Penalty for proportion of low-confidence words
    if total_words > 0:
        problem_ratio = low_conf_count / total_words
        base_score -= problem_ratio * 5
    
    return round(max(1.0, min(10.0, base_score)), 1)


# ---------------------------------------------------------------------------
# Fallbacks when libraries are missing
# ---------------------------------------------------------------------------
def _fallback_prosody():
    return {
        "duration_seconds": 0,
        "pitch_mean_hz": 0,
        "pitch_std_hz": 0,
        "pitch_range_hz": 0,
        "pitch_variation_coeff": 0,
        "intensity_mean_db": 0,
        "intensity_std_db": 0,
        "hnr_db": 0,
        "voiced_ratio": 0,
        "intonation_quality": "unavailable",
        "note": "Install parselmouth for prosody analysis: pip install praat-parselmouth"
    }


def _fallback_fluency(word_count):
    return {
        "word_count": word_count,
        "duration_seconds": 0,
        "words_per_minute": 0,
        "pause_count": 0,
        "filler_word_count": 0,
        "fluency_score": 5.0,
        "note": "Limited analysis — timestamps not available"
    }


def _fallback_content():
    return {
        "word_count": 0,
        "vocabulary_range": "unavailable",
        "coherence_quality": "unavailable",
        "note": "Transcript not available"
    }
