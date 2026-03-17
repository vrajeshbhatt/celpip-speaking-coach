"""
CELPIP Scoring Engine — Maps speech analysis to official CELPIP scoring dimensions.
Generates scores on the CELPIP scale (M, 1-12) and actionable feedback.
"""

import json
from pathlib import Path

# ---------------------------------------------------------------------------
# CELPIP Level Descriptors (CLB 10 = CELPIP 10)
# These describe what performance at each level looks like.
# ---------------------------------------------------------------------------
LEVEL_DESCRIPTORS = {
    12: "Expert: Near-native fluency, excellent pronunciation, sophisticated vocabulary, flawless task completion",
    11: "Advanced+: Highly proficient communication, very broad vocabulary, natural intonation throughout",
    10: "Advanced: Highly effective in demanding situations, precise descriptions, broad range of vocabulary, fluent rhythm",
    9: "Effective: Strong communication across contexts, good vocabulary range, clear pronunciation with occasional minor issues", 
    8: "Good: Competent communication, adequate vocabulary, generally clear pronunciation, task mostly fulfilled",
    7: "Adequate: Functional communication, sufficient vocabulary, understandable pronunciation, task addressed",
    6: "Developing: Basic communication with pauses, limited vocabulary, noticeable pronunciation issues",
    5: "Progressing: Simple communication, basic vocabulary, pronunciation often affects understanding",
    4: "Limited: Minimal communication, very basic vocabulary, significant pronunciation difficulties",
    3: "Basic: Very limited communication ability",
}

# ---------------------------------------------------------------------------
# CELPIP Scoring Criteria Descriptions
# ---------------------------------------------------------------------------
CRITERIA = {
    "content_coherence": {
        "name": "Content/Coherence",
        "description": "How relevant, well-organized, and developed your ideas are",
        "weight": 0.25
    },
    "vocabulary": {
        "name": "Vocabulary", 
        "description": "Range and accuracy of word choice",
        "weight": 0.25
    },
    "listenability": {
        "name": "Listenability",
        "description": "Pronunciation, intonation, rhythm, and how easy you are to understand",
        "weight": 0.30
    },
    "task_fulfillment": {
        "name": "Task Fulfillment",
        "description": "How well you addressed all parts of the task",
        "weight": 0.20
    }
}

# Model answers for each task type (abbreviated)
MODEL_ANSWERS = {
    1: "I understand this is a challenging situation, and I'd like to offer some advice. First, I would strongly recommend... The reason for this is... Secondly, it might be helpful to consider... This would be beneficial because... Finally, I think it's important to remember that... These steps should help you navigate this situation successfully.",
    2: "I'd like to share an experience from a few years ago when I... It happened at... and I was with... What made it particularly memorable was... I felt... during the experience, and it taught me an important lesson about... Looking back, I'm grateful for this experience because...",
    3: "Looking at this scene, I can see a... In the foreground, there is... On the left side, I notice... The people in the scene appear to be... Based on their expressions and body language, they seem... The overall atmosphere of the scene is...",
    4: "Based on what I can see in this scene, I predict that... The reason I think this will happen is... Another possibility is that... because... I also expect that... Overall, I believe the situation will evolve in this direction because...",
    5: "While both options have their merits, I would strongly recommend Option... The main reason is... This is particularly important because... Another advantage of this choice is... While the other option might seem attractive because of... , I believe... is the better choice overall because it offers...",
    6: "In this situation, I would first... because it's important to... Then I would say to them: '...' I would also... To make sure this doesn't happen again, I would... I believe this approach would resolve the situation fairly because...",
    7: "I believe that... and I feel quite strongly about this. My main reason is... For example, in my experience... Another important consideration is... While some people might argue that... , I think... In conclusion, I firmly believe that...",
    8: "This is certainly an unusual situation because normally... What makes it particularly strange is... If I were in this situation, I would first... because... Then I would... My best explanation for what might have happened is... To resolve this, I would..."
}


def score_response(analysis: dict, transcript: str, task_number: int, prompt: str) -> tuple:
    """
    Score a CELPIP speaking response on all 4 official dimensions.
    
    Returns:
        (scores_dict, feedback_dict)
    """
    if not transcript or transcript.startswith("["):
        return _empty_scores(), _empty_feedback("No transcript available for scoring.")
    
    # Extract analysis components
    prosody = analysis.get("prosody", {})
    fluency = analysis.get("fluency", {})
    content = analysis.get("content", {})
    pronunciation = analysis.get("pronunciation", {})
    
    # Score each dimension
    scores = {}
    feedback = {}
    
    # 1. Content/Coherence
    cc_score, cc_feedback = _score_content_coherence(content, fluency, task_number, prompt)
    scores["content_coherence"] = cc_score
    feedback["content_coherence"] = cc_feedback
    
    # 2. Vocabulary
    vocab_score, vocab_feedback = _score_vocabulary(content, transcript)
    scores["vocabulary"] = vocab_score
    feedback["vocabulary"] = vocab_feedback
    
    # 3. Listenability
    listen_score, listen_feedback = _score_listenability(prosody, fluency, pronunciation)
    scores["listenability"] = listen_score
    feedback["listenability"] = listen_feedback
    
    # 4. Task Fulfillment
    tf_score, tf_feedback = _score_task_fulfillment(content, fluency, task_number, prompt, transcript)
    scores["task_fulfillment"] = tf_score
    feedback["task_fulfillment"] = tf_feedback
    
    # Calculate overall score (weighted average)
    overall = (
        cc_score * CRITERIA["content_coherence"]["weight"] +
        vocab_score * CRITERIA["vocabulary"]["weight"] +
        listen_score * CRITERIA["listenability"]["weight"] +
        tf_score * CRITERIA["task_fulfillment"]["weight"]
    )
    scores["overall"] = round(overall, 1)
    scores["clb_level"] = _score_to_clb(scores["overall"])
    scores["level_descriptor"] = LEVEL_DESCRIPTORS.get(round(scores["overall"]), "")
    
    # Add CLB 10 benchmark comparison
    feedback["benchmark"] = _generate_benchmark_comparison(scores)
    
    # Add model answer
    feedback["model_answer"] = MODEL_ANSWERS.get(task_number, "")
    
    # Add top improvement priorities
    feedback["priorities"] = _get_improvement_priorities(scores, feedback)
    
    return scores, feedback


def _score_content_coherence(content: dict, fluency: dict, task_number: int, prompt: str) -> tuple:
    """Score content and coherence."""
    score = 5.0  # Base score
    feedback_points = {"strengths": [], "improvements": []}
    
    word_count = content.get("word_count", 0)
    markers = content.get("coherence_marker_count", 0)
    sentences = content.get("sentence_count", 0)
    ideas = content.get("idea_count", 0)
    avg_sent_len = content.get("avg_sentence_length", 0)
    coherence = content.get("coherence_quality", "minimal")
    
    # Word count scoring
    if word_count >= 100:
        score += 2.0
        feedback_points["strengths"].append("Good response length — you developed your ideas well")
    elif word_count >= 60:
        score += 1.0
        feedback_points["strengths"].append("Adequate response length")
    elif word_count >= 30:
        feedback_points["improvements"].append("Try to say more — aim for at least 80-100 words in your response")
    else:
        score -= 2.0
        feedback_points["improvements"].append("Your response was too short. Practice developing your ideas with more detail and examples")
    
    # Coherence markers
    if markers >= 4:
        score += 2.0
        feedback_points["strengths"].append("Excellent use of discourse markers (firstly, however, therefore, etc.)")
    elif markers >= 2:
        score += 1.0
        feedback_points["strengths"].append("Good use of some connecting words")
    else:
        feedback_points["improvements"].append("Use more connecting words like 'firstly', 'however', 'in addition', 'to conclude' to organize your ideas")
    
    # Idea development
    if ideas >= 3:
        score += 1.5
        feedback_points["strengths"].append(f"Good idea development with {ideas} distinct points")
    elif ideas >= 2:
        score += 0.5
    else:
        feedback_points["improvements"].append("Try to include at least 2-3 different ideas or points in your response")
    
    # Sentence variety
    if avg_sent_len > 8 and sentences >= 3:
        score += 0.5
        feedback_points["strengths"].append("Good sentence variety and complexity")
    
    score = round(max(3.0, min(12.0, score)), 1)
    
    return score, {
        "score": score,
        "criterion": "Content/Coherence",
        "strengths": feedback_points["strengths"],
        "improvements": feedback_points["improvements"],
        "detail": f"{word_count} words, {sentences} sentences, {markers} discourse markers, {ideas} ideas developed"
    }


def _score_vocabulary(content: dict, transcript: str) -> tuple:
    """Score vocabulary range and accuracy."""
    score = 5.0
    feedback_points = {"strengths": [], "improvements": []}
    
    ttr = content.get("type_token_ratio", 0)
    avg_word_len = content.get("avg_word_length", 0)
    long_ratio = content.get("long_word_ratio", 0)
    vocab_range = content.get("vocabulary_range", "limited")
    unique_count = content.get("unique_word_count", 0)
    
    # Type-token ratio (vocabulary diversity)
    if ttr > 0.65:
        score += 2.5
        feedback_points["strengths"].append("Excellent vocabulary diversity — you used a wide range of words")
    elif ttr > 0.55:
        score += 1.5
        feedback_points["strengths"].append("Good vocabulary variety")
    elif ttr > 0.45:
        score += 0.5
    else:
        feedback_points["improvements"].append("Try to use more varied vocabulary — avoid repeating the same words")
    
    # Word sophistication 
    if avg_word_len > 5.0:
        score += 1.5
        feedback_points["strengths"].append("Good use of sophisticated vocabulary")
    elif avg_word_len > 4.5:
        score += 0.5
    
    # Long words usage
    if long_ratio > 0.25:
        score += 1.5
        feedback_points["strengths"].append("Strong use of advanced vocabulary (complex words)")
    elif long_ratio > 0.15:
        score += 0.5
    else:
        feedback_points["improvements"].append("Try incorporating more advanced vocabulary — words like 'consequently', 'significant', 'beneficial'")
    
    # Check for strong vocabulary patterns
    advanced_patterns = ["furthermore", "consequently", "nevertheless", "significant", "beneficial", 
                        "perspective", "contribute", "demonstrate", "essential", "establish"]
    used_advanced = sum(1 for w in advanced_patterns if w in transcript.lower())
    if used_advanced >= 3:
        score += 1.0
        feedback_points["strengths"].append(f"Impressive — used {used_advanced} advanced vocabulary words")
    
    score = round(max(3.0, min(12.0, score)), 1)
    
    return score, {
        "score": score,
        "criterion": "Vocabulary",
        "strengths": feedback_points["strengths"],
        "improvements": feedback_points["improvements"],
        "detail": f"{unique_count} unique words, TTR: {ttr:.2f}, avg word length: {avg_word_len:.1f}"
    }


def _score_listenability(prosody: dict, fluency: dict, pronunciation: dict) -> tuple:
    """Score listenability — pronunciation, rhythm, intonation, grammar."""
    score = 5.0
    feedback_points = {"strengths": [], "improvements": []}
    
    # Fluency score component
    fluency_score = fluency.get("fluency_score", 5.0)
    wpm = fluency.get("words_per_minute", 0)
    pause_ratio = fluency.get("pause_ratio", 0)
    filler_count = fluency.get("filler_word_count", 0)
    filler_ratio = fluency.get("filler_ratio", 0)
    
    # Map fluency to listenability
    score += (fluency_score - 5.0) * 0.5
    
    # WPM feedback
    if 120 <= wpm <= 160:
        score += 1.5
        feedback_points["strengths"].append(f"Excellent speaking pace ({wpm:.0f} words/minute) — natural and comfortable")
    elif 100 <= wpm <= 180:
        score += 0.5
        feedback_points["strengths"].append(f"Good speaking pace ({wpm:.0f} words/minute)")
    elif wpm < 80 and wpm > 0:
        score -= 1.0
        feedback_points["improvements"].append(f"You spoke quite slowly ({wpm:.0f} WPM). Try to maintain a pace of 120-150 words/minute")
    elif wpm > 200:
        score -= 0.5
        feedback_points["improvements"].append(f"You spoke quite fast ({wpm:.0f} WPM). Try to slow down slightly for clarity")
    
    # Pause penalty
    if pause_ratio < 0.15 and wpm > 0:
        score += 1.0
        feedback_points["strengths"].append("Smooth delivery with minimal pausing")
    elif pause_ratio > 0.3:
        score -= 1.0
        feedback_points["improvements"].append("Reduce pausing — practice speaking more continuously")
    
    # Filler words
    if filler_count == 0:
        score += 1.0
        feedback_points["strengths"].append("No filler words — clean, professional delivery")
    elif filler_ratio > 0.05:
        score -= 1.0
        feedback_points["improvements"].append(f"Reduce filler words (found {filler_count}). Replace 'um/uh' with a brief pause")
    
    # Intonation quality from prosody
    intonation = prosody.get("intonation_quality", "unavailable")
    pitch_variation = prosody.get("pitch_variation_coeff", 0)
    
    if intonation == "expressive":
        score += 2.0
        feedback_points["strengths"].append("Excellent intonation — your speech has natural, expressive pitch variation")
    elif intonation == "natural":
        score += 1.0
        feedback_points["strengths"].append("Good, natural intonation patterns")
    elif intonation == "limited":
        feedback_points["improvements"].append("Work on varying your pitch more — use rising tones for questions and falling tones for statements")
    elif intonation == "monotone":
        score -= 1.0
        feedback_points["improvements"].append("Your speech sounds flat/monotone. Practice varying your pitch to sound more natural and engaging")
    
    # Pronunciation from Whisper confidence
    pron_score = pronunciation.get("pronunciation_score", 5)
    low_conf_words = pronunciation.get("low_confidence_words", [])
    
    if pron_score >= 8:
        score += 1.5
        feedback_points["strengths"].append("Clear pronunciation — words are well articulated")
    elif pron_score < 5:
        score -= 1.0
        if low_conf_words:
            problem_words = ", ".join(w["word"] for w in low_conf_words[:5])
            feedback_points["improvements"].append(f"Practice pronouncing these words more clearly: {problem_words}")
    
    score = round(max(3.0, min(12.0, score)), 1)
    
    return score, {
        "score": score,
        "criterion": "Listenability",
        "strengths": feedback_points["strengths"],
        "improvements": feedback_points["improvements"],
        "detail": f"{wpm:.0f} WPM, {filler_count} fillers, intonation: {intonation}, pronunciation: {pron_score:.1f}/10"
    }


def _score_task_fulfillment(content: dict, fluency: dict, task_number: int, prompt: str, transcript: str) -> tuple:
    """Score task fulfillment — relevance, completeness, tone."""
    score = 5.0
    feedback_points = {"strengths": [], "improvements": []}
    
    word_count = content.get("word_count", 0)
    ideas = content.get("idea_count", 0)
    
    # Response length relative to task expectations
    task_expectations = {
        1: {"min_words": 70, "expected_ideas": 3, "key": "advice"},
        2: {"min_words": 50, "expected_ideas": 2, "key": "experience"},
        3: {"min_words": 50, "expected_ideas": 3, "key": "description"},
        4: {"min_words": 50, "expected_ideas": 2, "key": "prediction"},
        5: {"min_words": 60, "expected_ideas": 2, "key": "persuasion"},
        6: {"min_words": 60, "expected_ideas": 2, "key": "solution"},
        7: {"min_words": 70, "expected_ideas": 3, "key": "opinion"},
        8: {"min_words": 50, "expected_ideas": 2, "key": "explanation"},
    }
    
    expectation = task_expectations.get(task_number, {"min_words": 50, "expected_ideas": 2, "key": "response"})
    
    # Word count vs. expectation
    if word_count >= expectation["min_words"]:
        score += 2.0
        feedback_points["strengths"].append(f"Good response length for Task {task_number}")
    elif word_count >= expectation["min_words"] * 0.6:
        score += 0.5
        feedback_points["improvements"].append(f"Try to develop your response more — aim for {expectation['min_words']}+ words")
    else:
        score -= 1.5
        feedback_points["improvements"].append(f"Response too short. For Task {task_number}, aim for at least {expectation['min_words']} words")
    
    # Idea count vs. expectation
    if ideas >= expectation["expected_ideas"]:
        score += 2.0
        feedback_points["strengths"].append(f"Good development — you covered {ideas} distinct ideas/points")
    elif ideas >= expectation["expected_ideas"] - 1:
        score += 0.5
    else:
        feedback_points["improvements"].append(f"Include more ideas — Task {task_number} expects at least {expectation['expected_ideas']} distinct points")
    
    # Task-specific keyword checks (basic relevance)
    task_keywords = {
        1: ["recommend", "suggest", "advice", "should", "would", "could", "try"],
        2: ["remember", "experience", "happened", "felt", "learned", "was", "were"],
        3: ["see", "shows", "there", "appears", "looking", "notice", "background", "foreground"],
        4: ["think", "predict", "will", "going to", "likely", "expect", "probably", "might"],
        5: ["prefer", "better", "recommend", "advantage", "because", "should", "choose"],
        6: ["would", "explain", "apologize", "resolve", "understand", "situation"],
        7: ["believe", "opinion", "think", "agree", "disagree", "because", "reason", "example"],
        8: ["unusual", "strange", "normally", "would", "investigate", "explanation"]
    }
    
    keywords = task_keywords.get(task_number, [])
    transcript_lower = transcript.lower()
    matched = sum(1 for k in keywords if k in transcript_lower)
    
    if matched >= len(keywords) * 0.5:
        score += 2.0
        feedback_points["strengths"].append("Your response addresses the task well with appropriate language")
    elif matched >= len(keywords) * 0.25:
        score += 1.0
    else:
        feedback_points["improvements"].append(f"Make sure to address the specific task requirements. Use phrases related to {expectation['key']}")
    
    score = round(max(3.0, min(12.0, score)), 1)
    
    return score, {
        "score": score,
        "criterion": "Task Fulfillment",
        "strengths": feedback_points["strengths"],
        "improvements": feedback_points["improvements"],
        "detail": f"{word_count} words ({expectation['min_words']} expected), {ideas} ideas ({expectation['expected_ideas']} expected)"
    }


def _score_to_clb(score: float) -> int:
    """Convert CELPIP score to CLB level."""
    return max(1, min(12, round(score)))


def _generate_benchmark_comparison(scores: dict) -> dict:
    """Compare scores against CLB 10 benchmark."""
    target = 10
    overall = scores.get("overall", 0)
    gap = target - overall
    
    return {
        "target_level": target,
        "current_level": scores.get("clb_level", 0),
        "gap": round(gap, 1),
        "status": "above_target" if gap <= 0 else ("close" if gap < 1.5 else "needs_work"),
        "message": _benchmark_message(gap, scores)
    }


def _benchmark_message(gap: float, scores: dict) -> str:
    """Generate benchmark comparison message."""
    if gap <= 0:
        return "🎯 You're at or above CLB 10! Keep practicing to maintain this level."
    elif gap < 1:
        return f"📈 You're very close to CLB 10! Focus on your weakest dimension to push through."
    elif gap < 2:
        return f"📊 Good progress toward CLB 10. Focus on consistent improvement in your lower-scoring dimensions."
    else:
        return f"🎯 Your target is CLB 10. Focus on building foundational skills and practice regularly."


def _get_improvement_priorities(scores: dict, feedback: dict) -> list:
    """Get top 3 improvement priorities based on scores."""
    dimensions = [
        ("content_coherence", scores.get("content_coherence", 0)),
        ("vocabulary", scores.get("vocabulary", 0)),
        ("listenability", scores.get("listenability", 0)),
        ("task_fulfillment", scores.get("task_fulfillment", 0))
    ]
    
    # Sort by score (lowest first)
    dimensions.sort(key=lambda x: x[1])
    
    priorities = []
    for dim_key, dim_score in dimensions[:3]:
        dim_feedback = feedback.get(dim_key, {})
        improvements = dim_feedback.get("improvements", [])
        if improvements:
            priorities.append({
                "dimension": CRITERIA[dim_key]["name"],
                "score": dim_score,
                "action": improvements[0]
            })
    
    return priorities


def _empty_scores() -> dict:
    return {
        "content_coherence": 0,
        "vocabulary": 0,
        "listenability": 0,
        "task_fulfillment": 0,
        "overall": 0,
        "clb_level": 0
    }


def _empty_feedback(message: str) -> dict:
    return {
        "content_coherence": {"score": 0, "criterion": "Content/Coherence", "strengths": [], "improvements": [message]},
        "vocabulary": {"score": 0, "criterion": "Vocabulary", "strengths": [], "improvements": [message]},
        "listenability": {"score": 0, "criterion": "Listenability", "strengths": [], "improvements": [message]},
        "task_fulfillment": {"score": 0, "criterion": "Task Fulfillment", "strengths": [], "improvements": [message]},
        "priorities": [],
        "benchmark": {"target_level": 10, "current_level": 0, "gap": 10, "status": "needs_work", "message": message}
    }
