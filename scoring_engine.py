"""
CELPIP Scoring Engine — Maps speech analysis to official CELPIP scoring dimensions.
Generates scores on the CELPIP scale (M, 1-12) and actionable feedback.

Scoring is STRICT and aligned to official CELPIP performance standards:
- Level 10+: Near-native fluency, sophisticated vocabulary, complex ideas, full task completion
- Level 7-9: Good communication, adequate vocabulary, mostly clear pronunciation
- Level 4-6: Basic communication with noticeable issues
- Level M-3: Minimal/limited communication

Reference: Official CELPIP Performance Standards (celpip.ca)
"""

import json
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# CELPIP Level Descriptors (Official CLB Alignment)
# ---------------------------------------------------------------------------
LEVEL_DESCRIPTORS = {
    12: {
        "label": "Expert",
        "summary": "Near-native fluency, very broad range of complex vocabulary, sophisticated grammar, flawless task completion",
        "content": "Communicates complex ideas with precise, detailed descriptions. Logical flow with sophisticated transitions.",
        "vocabulary": "Very broad range including abstract language, figures of speech, idioms. Highly specialized and precise.",
        "listenability": "Very good control of complex grammar. Fluent rhythm, native-like pronunciation and intonation.",
        "task": "Adapts language perfectly to situation, purpose, and audience. Precise communication."
    },
    11: {
        "label": "Advanced+",
        "summary": "Highly proficient in demanding situations. Broad vocabulary, natural intonation, extended fluent responses.",
        "content": "Presents and develops ideas with complex, clear descriptions. Good logical organization throughout.",
        "vocabulary": "Broad range with formal language and specialized terms. Descriptive and precise sentences.",
        "listenability": "Good control of broad range of complex grammar. Fluent rhythm with few hesitations.",
        "task": "Addresses all task requirements thoroughly. Appropriate tone and register throughout."
    },
    10: {
        "label": "Advanced",
        "summary": "Highly effective in demanding situations. Precise descriptions, broad vocabulary range, fluent rhythm.",
        "content": "Information presented and developed with clear, precise details. Well-organized with discourse markers.",
        "vocabulary": "Good range of concrete and some abstract language. Mostly accurate and precise word choice.",
        "listenability": "Mostly fluent rhythm and pronunciation. Minor issues that rarely affect understanding. Some complex grammar.",
        "task": "Effectively addresses the task with relevant, complete response. Appropriate tone."
    },
    9: {
        "label": "Effective",
        "summary": "Strong communication across contexts. Good vocabulary, clear pronunciation with occasional minor issues.",
        "content": "Presents information with clear descriptions and reasons. Ideas are organized logically.",
        "vocabulary": "Good range of concrete vocabulary with some abstract language. Generally accurate.",
        "listenability": "Intelligible with mostly fluent rhythm. Some control of complex grammar. Occasional minor pronunciation issues.",
        "task": "Addresses the task well. Response is relevant and mostly complete."
    },
    8: {
        "label": "Good",
        "summary": "Competent communication with adequate vocabulary. Generally clear pronunciation, task mostly fulfilled.",
        "content": "Presents information with clear descriptions or reasons. Some idea development.",
        "vocabulary": "Adequate range for the task. Some word choice issues that don't impede communication.",
        "listenability": "Intelligible speech. Good control of simple structures, some control of complex ones.",
        "task": "Addresses the task. Response is mostly relevant but may miss some aspects."
    },
    7: {
        "label": "Adequate",
        "summary": "Functional communication with sufficient vocabulary. Understandable pronunciation, task addressed.",
        "content": "Presents information and supports ideas with moderately complex reasons.",
        "vocabulary": "Sufficient range for basic communication. Common words used appropriately.",
        "listenability": "Understandable but with noticeable accent. Good control of simple structures.",
        "task": "Task addressed but response may lack completeness or detail."
    },
    6: {
        "label": "Developing",
        "summary": "Basic communication with pauses. Limited vocabulary, noticeable pronunciation issues.",
        "content": "Presents concrete and some abstract information. Limited development of ideas.",
        "vocabulary": "Limited range. Common words with some inaccuracies.",
        "listenability": "Understandable with effort. Noticeable pronunciation and grammar issues.",
        "task": "Partially addresses the task. Some relevant content but incomplete."
    },
    5: {
        "label": "Progressing",
        "summary": "Simple communication, basic vocabulary, pronunciation often affects understanding.",
        "content": "Can communicate basic feelings and describe common situations.",
        "vocabulary": "Basic vocabulary. Frequent repetition and limited range.",
        "listenability": "Pronunciation sometimes affects understanding. Simple sentence structures only.",
        "task": "Attempts the task but response is limited and may be off-topic."
    },
    4: {
        "label": "Limited",
        "summary": "Minimal communication, very basic vocabulary, significant pronunciation difficulties.",
        "content": "Can relate some factual information. Minimal idea development.",
        "vocabulary": "Very basic vocabulary. Very limited range.",
        "listenability": "Pronunciation frequently affects understanding. Very simple structures with errors.",
        "task": "Minimally attempts the task. Largely incomplete."
    },
    3: {
        "label": "Basic",
        "summary": "Very limited communication ability. Can sometimes express basic needs.",
        "content": "Can sometimes express likes, dislikes, and needs.",
        "vocabulary": "Very common words and phrases only.",
        "listenability": "Significant pronunciation issues. Communication is difficult.",
        "task": "Barely attempts the task."
    },
}

# ---------------------------------------------------------------------------
# CELPIP Scoring Criteria (Official Weights)
# ---------------------------------------------------------------------------
CRITERIA = {
    "content_coherence": {
        "name": "Content/Coherence",
        "description": "How relevant, well-organized, and developed your ideas are. Includes number/quality of ideas, logical structure, supporting details and examples.",
        "weight": 0.25
    },
    "vocabulary": {
        "name": "Vocabulary",
        "description": "Range and accuracy of word choice. Suitable use of words and phrases, precision, and whether vocabulary is sufficient for the task.",
        "weight": 0.25
    },
    "listenability": {
        "name": "Listenability",
        "description": "How intelligible and fluent you sound. Includes pronunciation, intonation, rhythm, pauses, self-correction, grammar control, and sentence variety.",
        "weight": 0.30
    },
    "task_fulfillment": {
        "name": "Task Fulfillment",
        "description": "How well you addressed the task requirements. Relevance, completeness, appropriate tone, and adherence to task format.",
        "weight": 0.20
    }
}

# ---------------------------------------------------------------------------
# Academic Word List (AWL) - Common high-level vocabulary
# Presence of these words indicates CLB 9+ vocabulary range
# ---------------------------------------------------------------------------
ACADEMIC_WORDS = {
    "analyze", "approach", "assess", "assume", "benefit", "concept", "consist",
    "constitute", "context", "contribute", "create", "define", "demonstrate",
    "derive", "distribute", "economy", "environment", "establish", "estimate",
    "evaluate", "evidence", "export", "factor", "finance", "formula", "function",
    "identify", "indicate", "individual", "interpret", "involve", "issue",
    "legislate", "major", "method", "occur", "percent", "period", "policy",
    "principle", "proceed", "process", "require", "research", "respond",
    "significant", "similar", "source", "specific", "structure", "theory",
    "vary", "furthermore", "consequently", "nevertheless", "subsequently",
    "perspective", "fundamental", "comprehensive", "substantial", "implement",
    "facilitate", "enhance", "acknowledge", "anticipate", "circumstances",
    "considerable", "demonstrate", "emphasize", "inevitable", "infrastructure",
    "preliminary", "predominantly", "reinforcement", "supplementary",
    "beneficial", "crucial", "essential", "integral", "paramount"
}

# Discourse markers by sophistication level
DISCOURSE_MARKERS = {
    "basic": {"and", "but", "so", "because", "also", "then", "next"},
    "intermediate": {
        "however", "therefore", "moreover", "although", "furthermore",
        "in addition", "on the other hand", "for example", "for instance",
        "as a result", "in my opinion", "i believe", "i think",
        "first", "second", "third", "firstly", "secondly", "finally"
    },
    "advanced": {
        "nevertheless", "consequently", "notwithstanding", "in contrast",
        "on the contrary", "to summarize", "in conclusion", "more importantly",
        "having said that", "that being said", "it is worth noting",
        "from my perspective", "taking into account", "given that",
        "with respect to", "in light of", "by the same token"
    }
}

# Model answers for each task type
MODEL_ANSWERS = {
    1: "I understand this is a challenging situation, and I'd like to offer some specific advice. First, I would strongly recommend that you... The primary reason for this suggestion is... This approach would be beneficial because it addresses the core issue of... Secondly, it might be worth considering... I say this because in my own experience, I've found that... This would help you... Finally, and perhaps most importantly, I'd encourage you to... The key advantage of this approach is... In conclusion, by following these three steps, you should be able to navigate this situation effectively and come out stronger.",
    2: "I'd like to share a meaningful experience from a few years ago that really shaped my perspective. It happened at... and I was with... at the time. What made this situation particularly memorable was... I remember feeling... during the experience — it was a mix of... and... The most significant moment was when... This taught me an important lesson about... specifically that... Looking back, I realize this experience fundamentally changed how I approach... I'm genuinely grateful for it because it helped me develop...",
    3: "Looking at this scene, I can see a vibrant... The setting appears to be... In the foreground, there is... which suggests... On the left side, I notice... while on the right, there are... The people in the scene appear to be... Based on their expressions and body language, they seem... I can also see some interesting details in the background, including... The overall atmosphere of the scene conveys a sense of... What stands out most is...",
    4: "Based on what I can observe in this scene, I would predict several things. First, I think... will likely happen because... The evidence for this is... Another possibility I foresee is that... I believe this because... considering the current circumstances shown, it's reasonable to expect... I also anticipate that... could occur, given that... Overall, I predict the situation will evolve toward... because the combination of... suggests this outcome is most probable.",
    5: "While both options certainly have their merits, I would strongly recommend choosing Option... and I have several compelling reasons for this recommendation. The primary advantage is that... which is particularly important because... Unlike the alternative, this option offers... Another significant benefit is... From a practical standpoint, this makes more sense because... I acknowledge that Option... has the appeal of... however, when you weigh all the factors, including... and... I firmly believe that... is the superior choice. It provides a better balance of... and will serve you well in the long term because...",
    6: "This is certainly a challenging situation, and I would handle it carefully. First and foremost, I would approach... with empathy and say something like: 'I understand that... and I appreciate...' Then, I would calmly explain the situation by saying: '...' Next, I would propose a fair solution: '...' To ensure this doesn't happen again, I would suggest implementing... I believe this approach would work because it acknowledges everyone's concerns while finding a constructive resolution. The most important thing is to maintain a respectful tone throughout.",
    7: "I believe strongly that... and I'd like to explain my reasoning. My primary argument is that... For example, research has shown that... and in my own experience, I've observed... Furthermore, it's important to consider that... which suggests... While I acknowledge that some people might argue... I respectfully disagree because... The evidence clearly indicates... In addition, we should consider the broader implications: ... To conclude, I firmly maintain my position that... because the weight of evidence — both from personal experience and broader observation — supports this view convincingly.",
    8: "This is certainly an unusual and perplexing situation because normally... What makes it particularly strange is that... The first thing I would do is carefully... because it's important to assess the situation before taking action. Then, I would... My initial theory about what might have happened is... possibly because... However, another explanation could be that... To resolve this, I would take the following steps: first... then... and finally... I think the most likely explanation is... and by handling it this way, I can address the situation systematically while keeping myself safe."
}


def score_response(analysis: dict, transcript: str, task_number: int, prompt: str) -> tuple:
    """
    Score a CELPIP speaking response on all 4 official dimensions.
    
    STRICT scoring aligned to official CELPIP performance standards.
    A score of 10+ requires near-native proficiency across all dimensions.
    
    Returns:
        (scores_dict, feedback_dict)
    """
    # Extract analysis components
    prosody = analysis.get("prosody", {})
    fluency = analysis.get("fluency", {})
    content = analysis.get("content", {})
    pronunciation = analysis.get("pronunciation", {})
    audio_features = analysis.get("audio_features", {})

    # Check for empty/invalid transcripts or no speech detected
    speech_ratio = audio_features.get("speech_ratio", 1.0)
    
    if not transcript or transcript.startswith("[") or len(transcript.split()) < 3 or speech_ratio < 0.03:
        err_msg = "This is not eligible to assess. No speech detected or answer invalid."
        return {"error": True, "status": "rejected", "message": err_msg}, {"error": True, "status": "rejected", "message": err_msg}
    
    # Score each dimension (all start from 3.0 base — must EARN higher scores)
    scores = {}
    feedback = {}
    
    # 1. Content/Coherence (25%)
    cc_score, cc_feedback = _score_content_coherence(content, fluency, task_number, prompt, transcript)
    scores["content_coherence"] = cc_score
    feedback["content_coherence"] = cc_feedback
    
    # 2. Vocabulary (25%)
    vocab_score, vocab_feedback = _score_vocabulary(content, transcript)
    scores["vocabulary"] = vocab_score
    feedback["vocabulary"] = vocab_feedback
    
    # 3. Listenability (30%)
    listen_score, listen_feedback = _score_listenability(prosody, fluency, pronunciation)
    scores["listenability"] = listen_score
    feedback["listenability"] = listen_feedback
    
    # 4. Task Fulfillment (20%)
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
    
    level = round(scores["overall"])
    descriptor = LEVEL_DESCRIPTORS.get(max(3, min(12, level)), LEVEL_DESCRIPTORS[3])
    scores["level_label"] = descriptor["label"]
    scores["level_descriptor"] = descriptor["summary"]
    
    # Add CLB 10 benchmark comparison
    feedback["benchmark"] = _generate_benchmark_comparison(scores)
    
    # Add model answer
    feedback["model_answer"] = MODEL_ANSWERS.get(task_number, "")
    
    # Add top improvement priorities
    feedback["priorities"] = _get_improvement_priorities(scores, feedback)
    
    # Add level-specific advice
    feedback["level_advice"] = _get_level_advice(scores["overall"])
    
    # Extract Immediate Actionable Improvements based on the top priorities
    immediate = []
    for p in feedback["priorities"]:
        immediate.append(p["action"])
    feedback["immediate_improvements"] = immediate
    
    return scores, feedback


# ---------------------------------------------------------------------------
# CONTENT/COHERENCE SCORING (Strict)
# ---------------------------------------------------------------------------
def _score_content_coherence(content: dict, fluency: dict, task_number: int, prompt: str, transcript: str) -> tuple:
    """
    Score content and coherence. STRICT rubric.
    
    Level 10 requires: 100+ words, 4+ discourse markers (including intermediate+),
    3+ developed ideas, good sentence variety, logical organization.
    """
    score = 3.0  # Start at minimum — must earn every point
    feedback_points = {"strengths": [], "improvements": []}
    
    word_count = content.get("word_count", 0)
    markers = content.get("coherence_marker_count", 0)
    sentences = content.get("sentence_count", 0)
    ideas = content.get("idea_count", 0)
    avg_sent_len = content.get("avg_sentence_length", 0)
    ttr = content.get("type_token_ratio", 0)
    
    # --- Word count scoring (stricter thresholds) ---
    if word_count >= 120:
        score += 2.5
        feedback_points["strengths"].append(f"Excellent response length ({word_count} words) — well-developed ideas")
    elif word_count >= 90:
        score += 2.0
        feedback_points["strengths"].append(f"Good response length ({word_count} words)")
    elif word_count >= 60:
        score += 1.0
        feedback_points["improvements"].append(f"Response length adequate ({word_count} words) but aim for 90-120+ words for CLB 10")
    elif word_count >= 30:
        score += 0.5
        feedback_points["improvements"].append(f"Response too short ({word_count} words). Target 90+ words to develop your ideas fully")
    else:
        feedback_points["improvements"].append(f"Response very short ({word_count} words). A CLB 10 response needs substantial development — aim for 90-120 words minimum")
    
    # --- Discourse marker sophistication ---
    transcript_lower = transcript.lower()
    
    advanced_markers_used = sum(1 for m in DISCOURSE_MARKERS["advanced"] if m in transcript_lower)
    intermediate_markers_used = sum(1 for m in DISCOURSE_MARKERS["intermediate"] if m in transcript_lower)
    basic_markers_used = sum(1 for m in DISCOURSE_MARKERS["basic"] if m in transcript_lower)
    
    total_markers = advanced_markers_used + intermediate_markers_used + basic_markers_used
    
    if advanced_markers_used >= 2 and total_markers >= 5:
        score += 2.5
        feedback_points["strengths"].append(f"Excellent discourse organization — used {total_markers} connecting phrases including sophisticated markers")
    elif intermediate_markers_used >= 3 and total_markers >= 4:
        score += 2.0
        feedback_points["strengths"].append(f"Good use of discourse markers ({total_markers} total)")
    elif intermediate_markers_used >= 1 and total_markers >= 2:
        score += 1.0
        feedback_points["improvements"].append("Use more varied and sophisticated connectors like 'nevertheless', 'taking into account', 'in light of'")
    elif total_markers >= 1:
        score += 0.5
        feedback_points["improvements"].append("Your ideas lack organization. Use discourse markers: 'firstly', 'however', 'in addition', 'in conclusion'")
    else:
        feedback_points["improvements"].append("No discourse markers detected. Organize your response with connectors: 'First of all...', 'Furthermore...', 'In conclusion...'")
    
    # --- Idea development ---
    if ideas >= 4 and sentences >= 5:
        score += 2.0
        feedback_points["strengths"].append(f"Strong idea development with {ideas} distinct points across {sentences} sentences")
    elif ideas >= 3:
        score += 1.5
        feedback_points["strengths"].append(f"Good idea development ({ideas} points)")
    elif ideas >= 2:
        score += 0.5
        feedback_points["improvements"].append(f"Only {ideas} ideas detected. CLB 10 expects 3+ well-developed points with supporting details")
    else:
        feedback_points["improvements"].append("Insufficient idea development. Present at least 3 distinct ideas, each supported by details or examples")
    
    # --- Sentence variety and complexity ---
    if sentences >= 4 and avg_sent_len >= 10 and avg_sent_len <= 25:
        score += 1.0
        feedback_points["strengths"].append("Good sentence variety with appropriate complexity")
    elif sentences >= 3 and avg_sent_len >= 8:
        score += 0.5
    else:
        if avg_sent_len > 30:
            feedback_points["improvements"].append("Sentences are too long and may be run-on. Break them into shorter, clearer sentences")
        elif avg_sent_len < 6 and sentences > 0:
            feedback_points["improvements"].append("Sentences are too simple and short. Use more complex sentence structures with clauses and details")
    
    score = round(max(3.0, min(12.0, score)), 1)
    
    return score, {
        "score": score,
        "criterion": "Content/Coherence",
        "level_descriptor": LEVEL_DESCRIPTORS.get(max(3, min(12, round(score))), {}).get("content", ""),
        "strengths": feedback_points["strengths"],
        "improvements": feedback_points["improvements"],
        "detail": f"{word_count} words, {sentences} sentences, {total_markers} discourse markers ({advanced_markers_used} advanced), {ideas} ideas developed"
    }


# ---------------------------------------------------------------------------
# VOCABULARY SCORING (Strict)
# ---------------------------------------------------------------------------
def _score_vocabulary(content: dict, transcript: str) -> tuple:
    """
    Score vocabulary range and accuracy. STRICT rubric.
    
    Level 10 requires: TTR > 0.60, avg word length > 5.0, multiple academic
    words, formal/abstract language usage.
    """
    score = 3.0
    feedback_points = {"strengths": [], "improvements": []}
    
    ttr = content.get("type_token_ratio", 0)
    avg_word_len = content.get("avg_word_length", 0)
    long_ratio = content.get("long_word_ratio", 0)
    unique_count = content.get("unique_word_count", 0)
    word_count = content.get("word_count", 0)
    
    # Check for academic/advanced vocabulary
    transcript_lower = transcript.lower()
    words_in_transcript = set(re.findall(r'\b[a-z]+\b', transcript_lower))
    academic_used = words_in_transcript.intersection(ACADEMIC_WORDS)
    academic_count = len(academic_used)
    
    # --- Type-Token Ratio (stricter) ---
    if ttr > 0.70:
        score += 2.5
        feedback_points["strengths"].append(f"Excellent vocabulary diversity (TTR: {ttr:.2f}) — rich variety of word choices")
    elif ttr > 0.60:
        score += 2.0
        feedback_points["strengths"].append(f"Good vocabulary diversity (TTR: {ttr:.2f})")
    elif ttr > 0.50:
        score += 1.0
        feedback_points["improvements"].append(f"Vocabulary diversity is adequate (TTR: {ttr:.2f}) but aim higher. Avoid repeating the same words — use synonyms")
    elif ttr > 0.40:
        score += 0.5
        feedback_points["improvements"].append(f"Limited vocabulary diversity (TTR: {ttr:.2f}). You're repeating too many words. Use synonyms and varied expressions")
    else:
        feedback_points["improvements"].append(f"Very limited vocabulary diversity (TTR: {ttr:.2f}). Practice using a wider range of words")
    
    # --- Word sophistication ---
    if avg_word_len > 5.5:
        score += 1.5
        feedback_points["strengths"].append("Sophisticated vocabulary — good use of complex, precise words")
    elif avg_word_len > 4.8:
        score += 1.0
    elif avg_word_len > 4.0:
        score += 0.5
    else:
        feedback_points["improvements"].append("Vocabulary is mostly basic. Incorporate more precise, multi-syllable words instead of simple ones")
    
    # --- Long words (6+ chars) ---
    if long_ratio > 0.30:
        score += 1.5
        feedback_points["strengths"].append("Strong use of advanced vocabulary (complex words)")
    elif long_ratio > 0.20:
        score += 1.0
    elif long_ratio > 0.12:
        score += 0.5
    else:
        feedback_points["improvements"].append("Use more advanced vocabulary words. Replace simple words with precise alternatives: 'good' → 'beneficial', 'big' → 'significant'")
    
    # --- Academic word usage (key differentiator for 10+) ---
    if academic_count >= 5:
        score += 2.0
        example_words = ", ".join(list(academic_used)[:5])
        feedback_points["strengths"].append(f"Impressive academic vocabulary — used {academic_count} advanced terms ({example_words})")
    elif academic_count >= 3:
        score += 1.0
        feedback_points["strengths"].append(f"Good use of some academic vocabulary ({academic_count} terms)")
    elif academic_count >= 1:
        score += 0.5
        feedback_points["improvements"].append(f"Limited academic vocabulary. Incorporate words like: 'significant', 'beneficial', 'consequently', 'perspective', 'demonstrate'")
    else:
        feedback_points["improvements"].append("No academic vocabulary detected. For CLB 10+, you need words like: 'significant', 'beneficial', 'furthermore', 'perspective', 'consequently'")
    
    # Penalty for very short responses (not enough data)
    if word_count < 40:
        score = max(3.0, score - 3.0)
        feedback_points["improvements"].append(f"Response too short ({word_count} words) to properly evaluate vocabulary range and depth. Speak more.")
    elif word_count < 60:
        score = max(3.0, score - 1.5)
        feedback_points["improvements"].append("Vocabulary range assessment is limited by low word count. Expand your answers.")
    
    score = round(max(3.0, min(12.0, score)), 1)
    
    return score, {
        "score": score,
        "criterion": "Vocabulary",
        "level_descriptor": LEVEL_DESCRIPTORS.get(max(3, min(12, round(score))), {}).get("vocabulary", ""),
        "strengths": feedback_points["strengths"],
        "improvements": feedback_points["improvements"],
        "detail": f"{unique_count} unique words, TTR: {ttr:.2f}, avg length: {avg_word_len:.1f}, {academic_count} academic words, {long_ratio:.0%} complex words"
    }


# ---------------------------------------------------------------------------
# LISTENABILITY SCORING (Strict)
# ---------------------------------------------------------------------------
def _score_listenability(prosody: dict, fluency: dict, pronunciation: dict) -> tuple:
    """
    Score listenability — pronunciation, rhythm, intonation, grammar.
    
    STRICT rubric. Level 10 requires: WPM 120-160, pause ratio < 0.15,
    near-zero fillers, expressive intonation, high pronunciation confidence.
    """
    score = 3.0
    feedback_points = {"strengths": [], "improvements": []}
    
    # Extract metrics
    wpm = fluency.get("words_per_minute", 0)
    pause_ratio = fluency.get("pause_ratio", 0)
    filler_count = fluency.get("filler_word_count", 0)
    filler_ratio = fluency.get("filler_ratio", 0)
    long_pauses = fluency.get("long_pause_count", 0)
    word_count = fluency.get("word_count", 0)
    
    intonation = prosody.get("intonation_quality", "unavailable")
    pitch_variation = prosody.get("pitch_variation_coeff", 0)
    hnr = prosody.get("hnr_db", 0)
    voiced_ratio = prosody.get("voiced_ratio", 0)
    
    pron_score = pronunciation.get("pronunciation_score", 5)
    pron_confidence = pronunciation.get("confidence_mean", 0)
    low_conf_words = pronunciation.get("low_confidence_words", [])
    
    # --- Speaking pace (strict WPM evaluation) ---
    if 130 <= wpm <= 155:
        score += 2.0
        feedback_points["strengths"].append(f"Excellent speaking pace ({wpm:.0f} WPM) — natural and confident")
    elif 120 <= wpm <= 165:
        score += 1.5
        feedback_points["strengths"].append(f"Good speaking pace ({wpm:.0f} WPM)")
    elif 100 <= wpm <= 180:
        score += 0.5
        if wpm < 120:
            feedback_points["improvements"].append(f"Speaking pace is a bit slow ({wpm:.0f} WPM). Native-like flow is 130-155 WPM. Practice speaking more continuously")
        else:
            feedback_points["improvements"].append(f"Speaking pace is slightly fast ({wpm:.0f} WPM). Slow down slightly for clarity — aim for 130-155 WPM")
    elif wpm > 0:
        if wpm < 100:
            score -= 1.0
            feedback_points["improvements"].append(f"Speaking pace is too slow ({wpm:.0f} WPM). This suggests hesitation or difficulty. Target 130-155 WPM")
        else:
            score -= 0.5
            feedback_points["improvements"].append(f"Speaking pace is too fast ({wpm:.0f} WPM). Slow down significantly for clarity")
    
    # --- Pause analysis (strict) ---
    if pause_ratio < 0.10 and wpm > 0:
        score += 1.5
        feedback_points["strengths"].append("Excellent fluency — smooth, continuous delivery with minimal pausing")
    elif pause_ratio < 0.18:
        score += 1.0
        feedback_points["strengths"].append("Good fluency with appropriate pausing")
    elif pause_ratio < 0.25:
        score += 0.5
        feedback_points["improvements"].append(f"Pause ratio of {pause_ratio:.0%} is noticeable. Practice speaking more continuously with natural breath pauses")
    elif pause_ratio < 0.35:
        feedback_points["improvements"].append(f"Too much pausing ({pause_ratio:.0%} of response). This disrupts the flow. Practice to reduce hesitation pauses")
    else:
        score -= 1.0
        feedback_points["improvements"].append(f"Excessive pausing ({pause_ratio:.0%}). This significantly impacts listenability. Consider thinking during prep time and practicing speaking without long gaps")
    
    # Long pause penalty
    if long_pauses >= 3:
        score -= 1.5
        feedback_points["improvements"].append(f"Found {long_pauses} long pauses (>1 second). These break your narrative flow — practice thinking ahead while speaking")
    elif long_pauses >= 1:
        score -= 0.5
        feedback_points["improvements"].append(f"Found {long_pauses} long pause(s). Try to maintain continuous speech")
    
    # --- Filler words (strict) ---
    if filler_count == 0 and word_count > 20:
        score += 1.5
        feedback_points["strengths"].append("No filler words — clean, professional delivery")
    elif filler_ratio <= 0.02:
        score += 0.5
        feedback_points["strengths"].append("Very few filler words")
    elif filler_ratio <= 0.05:
        feedback_points["improvements"].append(f"Found {filler_count} filler words ({filler_ratio:.0%}). Replace 'um/uh/like' with brief natural pauses")
    elif filler_ratio <= 0.10:
        score -= 1.0
        feedback_points["improvements"].append(f"Too many filler words ({filler_count} total, {filler_ratio:.0%}). This significantly impacts perceived fluency. Practice pausing silently instead")
    else:
        score -= 2.0
        feedback_points["improvements"].append(f"Excessive filler words ({filler_count} total, {filler_ratio:.0%}). This is a major fluency issue. Record yourself and practice eliminating fillers")
    
    # --- Intonation quality ---
    if intonation == "expressive":
        score += 2.0
        feedback_points["strengths"].append("Excellent intonation — natural, expressive pitch variation that enhances communication")
    elif intonation == "natural":
        score += 1.0
        feedback_points["strengths"].append("Good, natural intonation patterns")
    elif intonation == "limited":
        score -= 0.5
        feedback_points["improvements"].append("Intonation is limited. Vary your pitch: rise for questions, fall for statements, emphasize key words")
    elif intonation == "monotone":
        score -= 1.5
        feedback_points["improvements"].append("Speech sounds monotone/flat. Practice varying your pitch to sound more engaging — mark stress words in your notes during prep time")
    
    # --- Pronunciation confidence ---
    if pron_confidence > 0.90:
        score += 1.5
        feedback_points["strengths"].append("Clear, confident pronunciation — words are well articulated")
    elif pron_confidence > 0.80:
        score += 0.5
        feedback_points["strengths"].append("Generally clear pronunciation")
    elif pron_confidence > 0.65:
        feedback_points["improvements"].append("Some pronunciation clarity issues detected. Focus on enunciating clearly")
    elif pron_confidence > 0:
        score -= 1.0
        if low_conf_words:
            problem_words = ", ".join(w["word"] for w in low_conf_words[:5])
            feedback_points["improvements"].append(f"Pronunciation issues detected on: {problem_words}. Practice these words slowly and clearly")
        else:
            feedback_points["improvements"].append("Pronunciation needs improvement. Practice speaking clearly and at a moderate pace")
    
    # --- Voice quality (HNR) ---
    if hnr > 15:
        score += 0.5
        feedback_points["strengths"].append("Good voice quality — clear and resonant")
    elif hnr > 0 and hnr < 5:
        feedback_points["improvements"].append("Voice quality could improve. Speak clearly into the microphone and project your voice")
    
    score = round(max(3.0, min(12.0, score)), 1)
    
    return score, {
        "score": score,
        "criterion": "Listenability",
        "level_descriptor": LEVEL_DESCRIPTORS.get(max(3, min(12, round(score))), {}).get("listenability", ""),
        "strengths": feedback_points["strengths"],
        "improvements": feedback_points["improvements"],
        "detail": f"{wpm:.0f} WPM, {filler_count} fillers ({filler_ratio:.0%}), pause ratio: {pause_ratio:.0%}, {long_pauses} long pauses, intonation: {intonation}, pronunciation: {pron_confidence:.0%} confidence"
    }


# ---------------------------------------------------------------------------
# TASK FULFILLMENT SCORING (Strict)
# ---------------------------------------------------------------------------
def _score_task_fulfillment(content: dict, fluency: dict, task_number: int, prompt: str, transcript: str) -> tuple:
    """
    Score task fulfillment — relevance, completeness, tone, format.
    
    STRICT rubric. Level 10 requires: hitting ALL key elements of the task,
    appropriate tone, adequate response length, and relevant content.
    """
    score = 3.0
    feedback_points = {"strengths": [], "improvements": []}
    
    word_count = content.get("word_count", 0)
    ideas = content.get("idea_count", 0)
    duration_seconds = fluency.get("duration_seconds", 0)
    
    expected_duration = 90 if task_number in [1, 7] else 60
    duration_ratio = duration_seconds / expected_duration if expected_duration > 0 else 0
    
    # Task-specific expectations (stricter)
    task_expectations = {
        1: {"name": "Giving Advice", "min_words": 80, "ideal_words": 120, "expected_ideas": 3, "key": "advice",
            "required_elements": ["acknowledge situation", "give 2-3 specific suggestions", "explain why each helps"]},
        2: {"name": "Personal Experience", "min_words": 60, "ideal_words": 90, "expected_ideas": 2, "key": "experience",
            "required_elements": ["describe the experience", "include when/where/who", "express feelings", "share what you learned"]},
        3: {"name": "Describing a Scene", "min_words": 60, "ideal_words": 90, "expected_ideas": 3, "key": "description",
            "required_elements": ["describe the setting", "describe people/actions", "use spatial language", "mention details"]},
        4: {"name": "Making Predictions", "min_words": 60, "ideal_words": 90, "expected_ideas": 2, "key": "prediction",
            "required_elements": ["make specific predictions", "explain reasoning", "connect to scene details"]},
        5: {"name": "Comparing and Persuading", "min_words": 70, "ideal_words": 100, "expected_ideas": 3, "key": "persuasion",
            "required_elements": ["acknowledge both options", "clearly state recommendation", "give reasons", "address concerns"]},
        6: {"name": "Dealing with Difficult Situation", "min_words": 70, "ideal_words": 100, "expected_ideas": 2, "key": "solution",
            "required_elements": ["show empathy", "describe actions to take", "include what you would say", "propose resolution"]},
        7: {"name": "Expressing Opinions", "min_words": 80, "ideal_words": 120, "expected_ideas": 3, "key": "opinion",
            "required_elements": ["state opinion clearly", "support with reasons", "give examples", "acknowledge opposing view"]},
        8: {"name": "Unusual Situation", "min_words": 60, "ideal_words": 90, "expected_ideas": 2, "key": "explanation",
            "required_elements": ["identify what's unusual", "describe the situation", "explain what you'd do", "consider explanations"]},
    }
    
    expectation = task_expectations.get(task_number, {
        "name": "Speaking Task", "min_words": 60, "ideal_words": 90, "expected_ideas": 2, "key": "response",
        "required_elements": ["address the topic", "develop ideas"]
    })
    
    # --- Response length vs. task expectation ---
    if word_count >= expectation["ideal_words"]:
        score += 2.0
        feedback_points["strengths"].append(f"Good response length for {expectation['name']} ({word_count} words)")
    elif word_count >= expectation["min_words"]:
        score += 1.0
        feedback_points["improvements"].append(f"Response length adequate but could be more developed. Aim for {expectation['ideal_words']}+ words for this task type")
    elif word_count >= expectation["min_words"] * 0.5:
        score += 0.5
        feedback_points["improvements"].append(f"Response too short for {expectation['name']} ({word_count} words). Aim for at least {expectation['min_words']} words")
    else:
        feedback_points["improvements"].append(f"Response far too short ({word_count} words). {expectation['name']} requires at least {expectation['min_words']} words with developed ideas")
        
    # --- Duration ratio evaluation ---
    if duration_ratio < 0.3:
        score -= 3.0
        feedback_points["improvements"].append(f"Response duration ({duration_seconds:.0f}s) is significantly shorter than the expected {expected_duration}s. This severely impacts your score.")
    elif duration_ratio < 0.5:
        score -= 2.0
        feedback_points["improvements"].append(f"You only spoke for {duration_seconds:.0f}s out of {expected_duration}s. Use the full time to develop your ideas.")
    elif duration_ratio < 0.8:
        score -= 1.0
        feedback_points["improvements"].append(f"You stopped early ({duration_seconds:.0f}s out of {expected_duration}s). Elaborate more to maximize your score.")
    
    # --- Idea count vs. expectation ---
    if ideas >= expectation["expected_ideas"] + 1:
        score += 2.0
        feedback_points["strengths"].append(f"Excellent coverage — {ideas} distinct ideas, exceeding the {expectation['expected_ideas']} expected")
    elif ideas >= expectation["expected_ideas"]:
        score += 1.5
        feedback_points["strengths"].append(f"Good — covered the expected {expectation['expected_ideas']} ideas")
    elif ideas >= expectation["expected_ideas"] - 1 and ideas > 0:
        score += 0.5
        feedback_points["improvements"].append(f"Only {ideas} idea(s) developed. {expectation['name']} expects at least {expectation['expected_ideas']} distinct, supported points")
    else:
        feedback_points["improvements"].append(f"Insufficient idea development for {expectation['name']}. Present {expectation['expected_ideas']}+ ideas, each with supporting details")
    
    # --- Task-specific keyword/relevance checks ---
    task_keywords = {
        1: {"must_have": ["recommend", "suggest", "advice", "should", "would", "could", "try", "consider"],
            "bonus": ["because", "reason", "benefit", "advantage", "important", "help"]},
        2: {"must_have": ["remember", "experience", "happened", "felt", "learned", "was", "were", "time", "when"],
            "bonus": ["felt", "realized", "grateful", "taught", "lesson", "changed"]},
        3: {"must_have": ["see", "shows", "there", "appears", "looking", "notice"],
            "bonus": ["background", "foreground", "left", "right", "center", "behind", "atmosphere"]},
        4: {"must_have": ["think", "predict", "will", "going to", "likely", "expect", "probably"],
            "bonus": ["because", "based on", "evidence", "suggest", "reason"]},
        5: {"must_have": ["prefer", "better", "recommend", "advantage", "because", "should", "choose"],
            "bonus": ["compared", "while", "although", "superior", "benefit", "drawback"]},
        6: {"must_have": ["would", "explain", "apologize", "resolve", "understand", "situation", "say"],
            "bonus": ["empathy", "solution", "compromise", "fair", "respectful"]},
        7: {"must_have": ["believe", "opinion", "think", "agree", "disagree", "because", "reason"],
            "bonus": ["example", "experience", "evidence", "however", "conclude", "strongly"]},
        8: {"must_have": ["unusual", "strange", "normally", "would", "first", "explanation"],
            "bonus": ["investigate", "theory", "possible", "because", "resolve", "step"]}
    }
    
    keywords = task_keywords.get(task_number, {"must_have": [], "bonus": []})
    transcript_lower = transcript.lower()
    
    must_have_matched = sum(1 for k in keywords["must_have"] if k in transcript_lower)
    bonus_matched = sum(1 for k in keywords["bonus"] if k in transcript_lower)
    
    must_have_ratio = must_have_matched / len(keywords["must_have"]) if keywords["must_have"] else 0
    
    if must_have_ratio >= 0.6 and bonus_matched >= 3:
        score += 2.5
        feedback_points["strengths"].append(f"Excellent task relevance — your response directly addresses {expectation['name']} with appropriate language and structure")
    elif must_have_ratio >= 0.4 and bonus_matched >= 1:
        score += 1.5
        feedback_points["strengths"].append("Good task relevance — response addresses the main requirements")
    elif must_have_ratio >= 0.25:
        score += 0.5
        feedback_points["improvements"].append(f"Response partially addresses the task. For {expectation['name']}, make sure to: {', '.join(expectation['required_elements'])}")
    else:
        feedback_points["improvements"].append(f"Response may be off-topic or doesn't address the task well. Key elements for {expectation['name']}: {', '.join(expectation['required_elements'])}")
    
    # --- Tone appropriateness check (basic) ---
    # For Task 6 (difficult situation): should show empathy
    if task_number == 6:
        empathy_words = ["understand", "sorry", "apologize", "appreciate", "empathy", "feel", "perspective"]
        empathy_count = sum(1 for w in empathy_words if w in transcript_lower)
        if empathy_count >= 2:
            score += 0.5
            feedback_points["strengths"].append("Appropriate empathetic tone for handling a difficult situation")
        else:
            feedback_points["improvements"].append("Show more empathy when dealing with difficult situations — use phrases like 'I understand...', 'I appreciate your perspective...'")
    
    # For Task 5 (persuading): should be persuasive
    if task_number == 5:
        persuasion_words = ["strongly", "clearly", "definitely", "certainly", "undoubtedly", "convinced"]
        persuasion_count = sum(1 for w in persuasion_words if w in transcript_lower)
        if persuasion_count >= 1:
            score += 0.5
            feedback_points["strengths"].append("Good persuasive language")
        else:
            feedback_points["improvements"].append("Use more persuasive language — 'I strongly recommend...', 'I'm convinced that...'")
    
    score = round(max(3.0, min(12.0, score)), 1)
    
    return score, {
        "score": score,
        "criterion": "Task Fulfillment",
        "level_descriptor": LEVEL_DESCRIPTORS.get(max(3, min(12, round(score))), {}).get("task", ""),
        "strengths": feedback_points["strengths"],
        "improvements": feedback_points["improvements"],
        "detail": f"{duration_seconds:.0f}s/{expected_duration}s time, {word_count}/{expectation['ideal_words']} words, {ideas}/{expectation['expected_ideas']} ideas, {must_have_matched}/{len(keywords['must_have'])} task keywords matched, {bonus_matched} bonus keywords"
    }


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def _score_to_clb(score: float) -> int:
    """Convert CELPIP score to CLB level."""
    return max(1, min(12, round(score)))


def _generate_benchmark_comparison(scores: dict) -> dict:
    """Compare scores against CLB 10 benchmark."""
    target = 10
    overall = scores.get("overall", 0)
    gap = target - overall
    
    # Find weakest dimension
    dimensions = {
        "content_coherence": scores.get("content_coherence", 0),
        "vocabulary": scores.get("vocabulary", 0),
        "listenability": scores.get("listenability", 0),
        "task_fulfillment": scores.get("task_fulfillment", 0),
    }
    weakest = min(dimensions, key=dimensions.get)
    weakest_score = dimensions[weakest]
    
    return {
        "target_level": target,
        "current_level": scores.get("clb_level", 0),
        "gap": round(gap, 1),
        "weakest_dimension": CRITERIA[weakest]["name"],
        "weakest_score": weakest_score,
        "status": "above_target" if gap <= 0 else ("close" if gap < 1.5 else ("on_track" if gap < 3 else "needs_work")),
        "message": _benchmark_message(gap, scores, weakest)
    }


def _benchmark_message(gap: float, scores: dict, weakest: str) -> str:
    """Generate benchmark comparison message."""
    weakest_name = CRITERIA[weakest]["name"]
    
    if gap <= 0:
        return f"🎯 You're at CLB {scores['clb_level']} — at or above your target! Keep practicing to maintain consistency."
    elif gap < 1:
        return f"📈 Almost there! You're CLB {scores['clb_level']}, just {gap:.1f} points from CLB 10. Focus on {weakest_name} to push through."
    elif gap < 2:
        return f"📊 Good progress at CLB {scores['clb_level']}. Close the {gap:.1f}-point gap by strengthening {weakest_name} — your current weakest area."
    elif gap < 3:
        return f"🔄 You're at CLB {scores['clb_level']} — {gap:.1f} points from your target. Prioritize {weakest_name} and practice speaking daily."
    else:
        return f"🎯 Currently at CLB {scores['clb_level']}, working toward CLB 10. Build foundational skills in {weakest_name} first, then expand."


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
                "gap_to_10": round(10 - dim_score, 1),
                "action": improvements[0]
            })
    
    return priorities


def _get_level_advice(overall: float) -> str:
    """Get level-specific coaching advice."""
    level = round(overall)
    
    if level >= 10:
        return "You're performing at CLB 10+ level. To maintain and push to 11-12: focus on sophisticated vocabulary, complex grammar without errors, native-like intonation, and nuanced arguments."
    elif level >= 8:
        return "You're close to CLB 10. Key areas to push through: (1) Use more discourse markers and organize responses clearly, (2) Expand vocabulary with academic words, (3) Reduce fillers and pauses, (4) Practice natural intonation."
    elif level >= 6:
        return "Focus on building a stronger foundation: (1) Practice speaking continuously for 60-90 seconds, (2) Learn and use discourse markers like 'however', 'furthermore', 'in conclusion', (3) Build vocabulary beyond common words, (4) Record yourself and listen back."
    elif level >= 4:
        return "Work on core speaking skills: (1) Practice speaking in full sentences, (2) Learn basic discourse markers, (3) Focus on pronunciation of common words, (4) Build confidence by speaking daily — even 5 minutes helps."
    else:
        return "Start with fundamentals: (1) Practice forming complete sentences in English, (2) Listen to English media daily, (3) Repeat phrases out loud, (4) Focus on clarity over speed."


def _empty_scores() -> dict:
    return {
        "content_coherence": 0,
        "vocabulary": 0,
        "listenability": 0,
        "task_fulfillment": 0,
        "overall": 0,
        "clb_level": 0,
        "level_label": "—",
        "level_descriptor": "No response recorded"
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
