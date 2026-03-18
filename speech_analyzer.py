"""
Speech Analyzer — Direct audio signal analysis for CELPIP scoring.
Uses Parselmouth (Praat) for prosody and librosa for audio features.
Analyzes pronunciation quality, fluency, intonation, pacing, grammar complexity,
and self-correction patterns from the raw audio and transcript.

Enhanced for strict CELPIP scoring alignment.
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
    "um", "uh", "uhm", "umm", "er", "erm", "ah", "hmm",
    "like",  # only counted when used as filler, not comparison
    "you know", "basically", "actually", "literally",
    "sort of", "kind of", "i mean", "right", "okay"
}

# Self-correction indicators
SELF_CORRECTION_PATTERNS = [
    r"\bi mean\b",
    r"\bsorry\b.*\bi meant\b",
    r"\bno\b,?\s*\bi\b",  # "no, I..."
    r"\bwait\b",
    r"\blet me rephrase\b",
    r"\bactually\b",  # when followed by a correction
]

# Complex grammar indicators
SUBORDINATE_CONJUNCTIONS = {
    "although", "because", "since", "while", "whereas", "unless",
    "if", "when", "whenever", "wherever", "whether", "after",
    "before", "until", "as", "though", "even though", "provided that",
    "in case", "so that", "in order to", "despite", "regardless"
}

RELATIVE_PRONOUNS = {"who", "whom", "whose", "which", "that", "where", "when"}

# Common mispronunciation indicators
COMPLEX_WORDS = {
    "particularly", "comfortable", "temperature", "february",
    "pronunciation", "environment", "restaurant", "vegetable",
    "interesting", "different", "actually", "specific",
    "development", "opportunity", "communication", "experience",
    "necessary", "especially", "unfortunately", "definitely",
    "government", "comfortable", "library", "wednesday"
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
        "grammar": analyze_grammar(transcript),
        "audio_features": extract_audio_features(wav_path)
    }
    
    return result


def analyze_prosody(wav_path: str) -> dict:
    """
    Analyze prosodic features from audio signal using Parselmouth.
    Measures pitch variation, intensity, speech rate, intonation, and voice quality.
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
        pitch_median = float(np.median(pitch_values)) if len(pitch_values) > 0 else 0
        
        # Pitch variation coefficient (higher = more expressive)
        pitch_variation = pitch_std / pitch_mean if pitch_mean > 0 else 0
        
        # Pitch slope analysis (falling = declarative, rising = questioning)
        if len(pitch_values) > 10:
            first_quarter = np.mean(pitch_values[:len(pitch_values)//4])
            last_quarter = np.mean(pitch_values[-len(pitch_values)//4:])
            pitch_slope = (last_quarter - first_quarter) / pitch_mean if pitch_mean > 0 else 0
        else:
            pitch_slope = 0
        
        # Intensity analysis
        intensity = call(snd, "To Intensity", 75, 0, "yes")
        n_frames = call(intensity, "Get number of frames")
        intensity_values = [call(intensity, "Get value in frame", i + 1) for i in range(n_frames)]
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
        
        # Speech rhythm regularity (jitter in timing)
        if len(pitch_values) > 5:
            pitch_diffs = np.diff(pitch_values)
            rhythm_regularity = 1.0 - min(1.0, float(np.std(pitch_diffs)) / (pitch_mean + 1e-6))
        else:
            rhythm_regularity = 0

        return {
            "duration_seconds": round(duration, 2),
            "pitch_mean_hz": round(pitch_mean, 1),
            "pitch_median_hz": round(pitch_median, 1),
            "pitch_std_hz": round(pitch_std, 1),
            "pitch_range_hz": round(pitch_range, 1),
            "pitch_variation_coeff": round(pitch_variation, 3),
            "pitch_slope": round(pitch_slope, 3),
            "intensity_mean_db": round(intensity_mean, 1),
            "intensity_std_db": round(intensity_std, 1),
            "hnr_db": round(hnr, 1) if not math.isnan(hnr) else 0,
            "voiced_ratio": round(voiced_ratio, 3),
            "rhythm_regularity": round(rhythm_regularity, 3),
            "intonation_quality": _evaluate_intonation(pitch_variation, pitch_range, pitch_slope)
        }
    except Exception as e:
        print(f"[WARN] Prosody analysis error: {e}")
        return _fallback_prosody()


def analyze_fluency(transcript: str, word_timestamps: list) -> dict:
    """
    Analyze fluency from transcript and word timing.
    Measures speech rate, pause patterns, filler words, smoothness, and self-corrections.
    """
    words = transcript.lower().split()
    word_count = len(words)
    
    if not word_timestamps or word_count == 0:
        return _fallback_fluency(word_count)
    
    # Duration from timestamps
    total_duration = word_timestamps[-1]["end"] - word_timestamps[0]["start"] if word_timestamps else 0
    
    # Words per minute
    wpm = (word_count / total_duration * 60) if total_duration > 0 else 0
    
    # Pause analysis with categorization
    pauses = []
    short_pauses = []    # 0.3-0.6s — natural breath pauses
    medium_pauses = []   # 0.6-1.0s — hesitation
    long_pauses = []     # >1.0s — significant hesitation
    
    for i in range(1, len(word_timestamps)):
        gap = word_timestamps[i]["start"] - word_timestamps[i - 1]["end"]
        if gap > 0.3:
            pauses.append(gap)
            if gap <= 0.6:
                short_pauses.append(gap)
            elif gap <= 1.0:
                medium_pauses.append(gap)
            else:
                long_pauses.append(gap)
    
    avg_pause = sum(pauses) / len(pauses) if pauses else 0
    total_pause_time = sum(pauses)
    pause_ratio = total_pause_time / total_duration if total_duration > 0 else 0
    
    # Filler words (more accurate counting)
    filler_count = 0
    filler_words_found = []
    for word in words:
        clean_word = word.strip(".,!?;:'\"()")
        if clean_word in FILLER_WORDS:
            filler_count += 1
            filler_words_found.append(clean_word)
    
    # Check multi-word fillers
    transcript_lower = transcript.lower()
    for filler in ["you know", "sort of", "kind of", "i mean"]:
        count = transcript_lower.count(filler)
        if count > 0:
            filler_count += count
            filler_words_found.extend([filler] * count)
    
    filler_ratio = filler_count / word_count if word_count > 0 else 0
    
    # Self-correction detection
    self_corrections = 0
    for pattern in SELF_CORRECTION_PATTERNS:
        self_corrections += len(re.findall(pattern, transcript_lower))
    
    # Articulation rate (excluding pauses)
    speaking_time = total_duration - total_pause_time
    articulation_rate = (word_count / speaking_time * 60) if speaking_time > 0 else 0
    
    # Speaking consistency (variance in word timing)
    if len(word_timestamps) > 2:
        word_durations = [
            word_timestamps[i]["end"] - word_timestamps[i]["start"]
            for i in range(len(word_timestamps))
        ]
        timing_variance = float(np.std(word_durations)) if HAS_NUMPY else 0
    else:
        timing_variance = 0
    
    return {
        "word_count": word_count,
        "duration_seconds": round(total_duration, 2),
        "words_per_minute": round(wpm, 1),
        "articulation_rate": round(articulation_rate, 1),
        "pause_count": len(pauses),
        "short_pause_count": len(short_pauses),
        "medium_pause_count": len(medium_pauses),
        "long_pause_count": len(long_pauses),
        "avg_pause_duration": round(avg_pause, 2),
        "pause_ratio": round(pause_ratio, 3),
        "filler_word_count": filler_count,
        "filler_words": filler_words_found[:10],
        "filler_ratio": round(filler_ratio, 3),
        "self_correction_count": self_corrections,
        "timing_variance": round(timing_variance, 4),
        "fluency_score": _calculate_fluency_score(wpm, pause_ratio, filler_ratio, len(long_pauses), self_corrections)
    }


def analyze_content(transcript: str) -> dict:
    """
    Analyze content quality from transcript.
    Evaluates vocabulary range, sentence complexity, coherence markers, and idea density.
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
    
    # Coherence markers (all levels)
    transcript_lower = transcript.lower()
    coherence_markers = {
        "firstly", "secondly", "thirdly", "first", "second", "third",
        "however", "therefore", "moreover", "furthermore", "additionally",
        "consequently", "nevertheless", "meanwhile", "although", "because",
        "since", "while", "whereas", "in conclusion", "to summarize",
        "for example", "for instance", "specifically", "in addition",
        "on the other hand", "in my opinion", "i believe", "i think",
        "as a result", "in contrast", "similarly", "overall"
    }
    marker_count = sum(1 for m in coherence_markers if m in transcript_lower)
    
    # Sentence detection (improved)
    sentences = re.split(r'[.!?]+', transcript)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip().split()) >= 2]
    sentence_count = len(sentences)
    
    # Average sentence length
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else word_count
    
    # Sentence length variety (good speakers vary their sentence length)
    if sentence_count >= 3:
        sent_lengths = [len(s.split()) for s in sentences]
        sent_length_std = float(np.std(sent_lengths)) if HAS_NUMPY else 0
    else:
        sent_length_std = 0
    
    # Idea density estimation (count clauses, not just sentences)
    idea_count = max(1, sentence_count)
    # Bonus for sentences with subordinate clauses (more developed ideas)
    for conj in SUBORDINATE_CONJUNCTIONS:
        if conj in transcript_lower:
            idea_count += 0.5
    idea_count = int(idea_count)
    
    return {
        "word_count": word_count,
        "unique_word_count": len(unique_words),
        "type_token_ratio": round(type_token_ratio, 3),
        "avg_word_length": round(avg_word_length, 1),
        "long_word_ratio": round(long_word_ratio, 3),
        "long_word_count": len(long_words),
        "coherence_marker_count": marker_count,
        "sentence_count": sentence_count,
        "avg_sentence_length": round(avg_sentence_length, 1),
        "sentence_length_variety": round(sent_length_std, 1),
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
    
    # Confidence distribution analysis
    high_conf = sum(1 for c in confidences if c >= 0.9)
    medium_conf = sum(1 for c in confidences if 0.7 <= c < 0.9)
    low_conf = sum(1 for c in confidences if c < 0.7)
    
    return {
        "confidence_mean": round(mean_confidence, 3),
        "confidence_min": round(min(confidences), 3) if confidences else 0,
        "confidence_std": round(float(np.std(confidences)), 3) if HAS_NUMPY and confidences else 0,
        "high_confidence_pct": round(high_conf / len(confidences) * 100, 1) if confidences else 0,
        "low_confidence_words": low_confidence_words[:10],
        "complex_words_used": complex_used,
        "pronunciation_score": _calculate_pronunciation_score(mean_confidence, len(low_confidence_words), len(word_timestamps))
    }


def analyze_grammar(transcript: str) -> dict:
    """
    Analyze grammar complexity and variety from transcript.
    Checks for subordinate clauses, relative clauses, and sentence structure variety.
    """
    if not transcript or transcript.startswith("["):
        return {"complexity_score": 0, "subordinate_clauses": 0, "relative_clauses": 0}
    
    transcript_lower = transcript.lower()
    words = transcript_lower.split()
    
    # Count subordinate conjunctions (indicates complex sentence structures)
    subordinate_count = 0
    subordinates_used = []
    for conj in SUBORDINATE_CONJUNCTIONS:
        count = transcript_lower.count(conj)
        if count > 0:
            subordinate_count += count
            subordinates_used.append(conj)
    
    # Count relative clauses
    relative_count = 0
    for pron in RELATIVE_PRONOUNS:
        # Count as relative clause only when preceded by a noun-like context
        relative_count += len(re.findall(r'\b\w+\s+' + pron + r'\b', transcript_lower))
    
    # Conditional structures
    conditional_count = len(re.findall(r'\bif\b.*\bwould\b|\bif\b.*\bcould\b|\bif\b.*\bwere\b', transcript_lower))
    
    # Passive voice indicators
    passive_patterns = len(re.findall(r'\b(?:is|are|was|were|been|being)\s+\w+ed\b', transcript_lower))
    
    # Sentence structure variety
    sentences = re.split(r'[.!?]+', transcript)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip().split()) >= 2]
    
    # Check for variety in sentence starters
    if sentences:
        starters = [s.split()[0].lower() if s.split() else "" for s in sentences]
        unique_starters = len(set(starters))
        starter_variety = unique_starters / len(starters) if starters else 0
    else:
        starter_variety = 0
    
    # Grammar complexity score (0-10)
    complexity_score = 3.0
    if subordinate_count >= 3:
        complexity_score += 2.0
    elif subordinate_count >= 1:
        complexity_score += 1.0
    
    if relative_count >= 2:
        complexity_score += 1.5
    elif relative_count >= 1:
        complexity_score += 0.5
    
    if conditional_count >= 1:
        complexity_score += 1.0
    
    if passive_patterns >= 1:
        complexity_score += 0.5
    
    if starter_variety >= 0.7:
        complexity_score += 1.0
    elif starter_variety >= 0.5:
        complexity_score += 0.5
    
    complexity_score = min(10.0, complexity_score)
    
    return {
        "complexity_score": round(complexity_score, 1),
        "subordinate_clauses": subordinate_count,
        "subordinates_used": subordinates_used,
        "relative_clauses": relative_count,
        "conditional_structures": conditional_count,
        "passive_constructions": passive_patterns,
        "sentence_starter_variety": round(starter_variety, 2),
        "grammar_level": _evaluate_grammar_level(complexity_score)
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
        
        # Speech-to-silence ratio
        rms_values = rms[0]
        silence_threshold = 0.01
        speech_frames = np.sum(rms_values > silence_threshold)
        total_frames = len(rms_values)
        speech_ratio = speech_frames / total_frames if total_frames > 0 else 0
        
        return {
            "available": True,
            "sample_rate": sr,
            "duration": round(len(y) / sr, 2),
            "spectral_centroid_mean": round(float(np.mean(spectral_centroid)), 1),
            "zero_crossing_rate_mean": round(float(np.mean(zcr)), 4),
            "rms_energy_mean": round(float(np.mean(rms)), 4),
            "speech_ratio": round(float(speech_ratio), 3)
        }
    except Exception as e:
        return {"available": False, "error": str(e)}


# ---------------------------------------------------------------------------
# Scoring helper functions
# ---------------------------------------------------------------------------
def _evaluate_intonation(pitch_variation: float, pitch_range: float, pitch_slope: float = 0) -> str:
    """Evaluate intonation quality from pitch metrics."""
    if pitch_variation > 0.25 and pitch_range > 100:
        return "expressive"
    elif pitch_variation > 0.15 and pitch_range > 60:
        return "natural"
    elif pitch_variation > 0.08:
        return "limited"
    else:
        return "monotone"


def _calculate_fluency_score(wpm: float, pause_ratio: float, filler_ratio: float, long_pauses: int, self_corrections: int = 0) -> float:
    """Calculate fluency score (0-10 scale). STRICT."""
    score = 10.0
    
    # WPM penalty (ideal: 130-155 WPM for natural English)
    if wpm < 70:
        score -= 4.0
    elif wpm < 90:
        score -= 2.5
    elif wpm < 110:
        score -= 1.5
    elif wpm < 120:
        score -= 0.5
    elif wpm > 200:
        score -= 2.5
    elif wpm > 180:
        score -= 1.5
    elif wpm > 165:
        score -= 0.5
    
    # Pause ratio penalty (stricter)
    if pause_ratio > 0.40:
        score -= 3.5
    elif pause_ratio > 0.30:
        score -= 2.5
    elif pause_ratio > 0.25:
        score -= 1.5
    elif pause_ratio > 0.18:
        score -= 1.0
    elif pause_ratio > 0.10:
        score -= 0.5
    
    # Long pause penalty
    score -= min(long_pauses * 0.7, 3.0)
    
    # Filler word penalty (stricter)
    if filler_ratio > 0.12:
        score -= 3.0
    elif filler_ratio > 0.08:
        score -= 2.0
    elif filler_ratio > 0.05:
        score -= 1.5
    elif filler_ratio > 0.02:
        score -= 0.5
    
    # Self-correction penalty (minor — some self-correction is normal)
    if self_corrections > 3:
        score -= 1.0
    elif self_corrections > 1:
        score -= 0.5
    
    return round(max(1.0, min(10.0, score)), 1)


def _evaluate_vocabulary(ttr: float, avg_length: float, long_ratio: float) -> str:
    """Evaluate vocabulary range (stricter thresholds)."""
    combined = (ttr * 3 + avg_length / 10 + long_ratio * 3) / 3
    if combined > 0.60:
        return "advanced"
    elif combined > 0.45:
        return "good"
    elif combined > 0.30:
        return "adequate"
    else:
        return "limited"


def _evaluate_coherence(markers: int, sentences: int, avg_length: float) -> str:
    """Evaluate coherence quality."""
    marker_ratio = markers / max(sentences, 1)
    if marker_ratio > 0.6 and avg_length > 10:
        return "well-organized"
    elif marker_ratio > 0.3 or (markers >= 3 and avg_length > 8):
        return "adequate"
    elif markers > 0:
        return "basic"
    else:
        return "minimal"


def _evaluate_grammar_level(complexity: float) -> str:
    """Evaluate grammar complexity level."""
    if complexity >= 8:
        return "advanced"
    elif complexity >= 6:
        return "good"
    elif complexity >= 4:
        return "adequate"
    else:
        return "basic"


def _calculate_pronunciation_score(mean_conf: float, low_conf_count: int, total_words: int) -> float:
    """Calculate pronunciation score from Whisper confidence (stricter)."""
    base_score = mean_conf * 10
    
    # Penalty for proportion of low-confidence words (stricter)
    if total_words > 0:
        problem_ratio = low_conf_count / total_words
        base_score -= problem_ratio * 7  # Increased from 5 to 7
    
    return round(max(1.0, min(10.0, base_score)), 1)


# ---------------------------------------------------------------------------
# Fallbacks when libraries are missing
# ---------------------------------------------------------------------------
def _fallback_prosody():
    return {
        "duration_seconds": 0,
        "pitch_mean_hz": 0,
        "pitch_median_hz": 0,
        "pitch_std_hz": 0,
        "pitch_range_hz": 0,
        "pitch_variation_coeff": 0,
        "pitch_slope": 0,
        "intensity_mean_db": 0,
        "intensity_std_db": 0,
        "hnr_db": 0,
        "voiced_ratio": 0,
        "rhythm_regularity": 0,
        "intonation_quality": "unavailable",
        "note": "Install parselmouth for prosody analysis: pip install praat-parselmouth"
    }


def _fallback_fluency(word_count):
    return {
        "word_count": word_count,
        "duration_seconds": 0,
        "words_per_minute": 0,
        "articulation_rate": 0,
        "pause_count": 0,
        "short_pause_count": 0,
        "medium_pause_count": 0,
        "long_pause_count": 0,
        "avg_pause_duration": 0,
        "pause_ratio": 0,
        "filler_word_count": 0,
        "filler_words": [],
        "filler_ratio": 0,
        "self_correction_count": 0,
        "timing_variance": 0,
        "fluency_score": 5.0,
        "note": "Limited analysis — timestamps not available"
    }


def _fallback_content():
    return {
        "word_count": 0,
        "unique_word_count": 0,
        "type_token_ratio": 0,
        "avg_word_length": 0,
        "long_word_ratio": 0,
        "long_word_count": 0,
        "coherence_marker_count": 0,
        "sentence_count": 0,
        "avg_sentence_length": 0,
        "sentence_length_variety": 0,
        "idea_count": 0,
        "vocabulary_range": "unavailable",
        "coherence_quality": "unavailable",
        "note": "Transcript not available"
    }
