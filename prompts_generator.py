"""
Prompts Generator — Robust task generation for CELPIP Speaking.
Supports template-based generation and LLM-based generation (if API key provided).
"""

import random
import json
import os
from datetime import datetime

class PromptsGenerator:
    def __init__(self):
        # A pool of higher-quality scenario templates
        self.templates = {
            1: [
                "Your {target} is {situation}. Give them advice on how to handle it.",
                "Imagine {target} who {situation}. What advice would you give them?"
            ],
            7: [
                "Some people think that {topic_a} is better, while others prefer {topic_b}. What is your opinion?",
                "There is a debate about whether {topic_a} should be {action}. What do you think?"
            ]
        }
        
        self.new_topics = [
            "starting a YouTube channel", "learning to cook professionally", "moving to a rural area",
            "volunteering at a local animal shelter", "taking a sabbatical year", "learning a third language",
            "investing in cryptocurrency", "becoming a minimalist", "starting an urban garden",
            "pursuing a PhD", "becoming a digital nomad", "learning a musical instrument at 40"
        ]

    def generate_prompt(self, task_number=None, topic=None):
        """Generate a new prompt for a specific task."""
        task_number = task_number or random.randint(1, 8)
        topic = topic or random.choice(self.new_topics)
        
        if task_number == 1:
            return {
                "id": f"GEN-1-{random.randint(1000, 9999)}",
                "scenario": f"Your friend is thinking about {topic}, but they are unsure if it's the right move. They are looking for your advice on the pros and cons and what they should consider. What would you say to them?",
                "situation": f"Friend considering {topic}",
                "target": "your friend"
            }
        elif task_number == 7:
            return {
                "id": f"GEN-7-{random.randint(1000, 9999)}",
                "scenario": f"There is a lot of discussion lately about {topic}. Some people argue it is a great idea, while others believe it has significant drawbacks. What is your opinion on this matter?",
                "topic": topic
            }
        elif task_number == 2:
            return {
                "id": f"GEN-2-{random.randint(1000, 9999)}",
                "scenario": f"Talk about a personal experience you have had related to {topic}. How did it happen, and what did you learn?",
                "topic": topic
            }
        
        # Generic fallback
        timestamp = datetime.now().strftime("%H:%M:%S")
        return {
            "id": f"NEW-{random.randint(1000, 9999)}",
            "scenario": f"New Challenge Generated at {timestamp}: {topic.capitalize()} - Talk about your perspective and experience on this.",
            "topic": topic
        }

generator = PromptsGenerator()
