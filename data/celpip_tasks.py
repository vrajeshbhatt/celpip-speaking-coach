"""
CELPIP Speaking Tasks Database
All 8 scored tasks with official format, timing, instructions, and multiple prompts.
"""

import random

# ---------------------------------------------------------------------------
# CELPIP Speaking Task Definitions
# ---------------------------------------------------------------------------

CELPIP_TASKS = [
    {
        "number": 1,
        "name": "Giving Advice",
        "description": "Give advice to someone about a specific situation.",
        "instructions": "You will hear about a situation. Then you will give advice to someone about what to do in that situation. You will have 30 seconds to prepare and 90 seconds to speak.",
        "prep_time": 30,
        "response_time": 90,
        "tips": [
            "Start by acknowledging the situation",
            "Give 2-3 specific pieces of advice",
            "Explain WHY each suggestion would help",
            "Use phrases like 'I would recommend...', 'You should consider...', 'In my opinion...'",
            "End with encouragement or a summary"
        ],
        "prompts": [
            {
                "id": "T1-P1",
                "scenario": "Your friend has just moved to a new city for work. They don't know anyone there and are feeling lonely and homesick.",
                "situation": "Your friend moved to a new city and feels lonely.",
                "target": "your friend"
            },
            {
                "id": "T1-P2",
                "scenario": "Your colleague is struggling to balance their work responsibilities with studying for a professional certification exam.",
                "situation": "Your colleague needs to balance work and studying.",
                "target": "your colleague"
            },
            {
                "id": "T1-P3",
                "scenario": "Your neighbor is thinking about adopting a pet but is unsure whether they have enough time and resources to take care of one.",
                "situation": "Your neighbor wants to adopt a pet but is unsure.",
                "target": "your neighbor"
            },
            {
                "id": "T1-P4",
                "scenario": "A family member wants to start their own small business but has no prior business experience and limited savings.",
                "situation": "A family member wants to start a business with limited experience.",
                "target": "your family member"
            },
            {
                "id": "T1-P5",
                "scenario": "Your friend's teenage child is spending too much time on social media and their grades are dropping. Your friend doesn't know how to handle the situation.",
                "situation": "Your friend's child is addicted to social media.",
                "target": "your friend"
            }
        ]
    },
    {
        "number": 2,
        "name": "Talking about a Personal Experience",
        "description": "Talk about a personal experience related to a given topic.",
        "instructions": "You will be asked to talk about a personal experience. Think about a situation from your own life that relates to the topic. You will have 30 seconds to prepare and 60 seconds to speak.",
        "prep_time": 30,
        "response_time": 60,
        "tips": [
            "Use past tense to describe the experience",
            "Include specific details: when, where, who was involved",
            "Describe how you FELT during the experience",
            "Explain what you LEARNED from it",
            "Make it personal and genuine"
        ],
        "prompts": [
            {
                "id": "T2-P1",
                "scenario": "Talk about a time when you had to learn something completely new. What was it, and how did you feel about the experience?",
                "topic": "Learning something new"
            },
            {
                "id": "T2-P2",
                "scenario": "Describe a memorable journey or trip you have taken. What made it special?",
                "topic": "A memorable trip"
            },
            {
                "id": "T2-P3",
                "scenario": "Talk about a time when you helped someone and it made a difference. What happened?",
                "topic": "Helping someone"
            },
            {
                "id": "T2-P4",
                "scenario": "Describe a challenging situation you faced at work or school. How did you handle it?",
                "topic": "Overcoming a challenge"
            },
            {
                "id": "T2-P5",
                "scenario": "Talk about a cultural event or celebration that is important to you. Why is it meaningful?",
                "topic": "A cultural celebration"
            }
        ]
    },
    {
        "number": 3,
        "name": "Describing a Scene",
        "description": "Describe what you see in a picture or scene in as much detail as possible.",
        "instructions": "Look at the scene below. Describe what is happening in as much detail as possible. You will have 30 seconds to prepare and 60 seconds to speak.",
        "prep_time": 30,
        "response_time": 60,
        "tips": [
            "Start with an overview: 'This scene shows...'",
            "Describe the setting and background",
            "Talk about the people: what they're doing, wearing, their expressions",
            "Mention objects and their positions",
            "Use spatial language: 'in the foreground', 'on the left', 'behind'"
        ],
        "prompts": [
            {
                "id": "T3-P1",
                "scenario": "Imagine a busy community park on a sunny Saturday afternoon. There are families having picnics, children playing on the playground, joggers on the trail, and a group of people doing yoga on the grass. A food truck is parked near the entrance.",
                "scene_description": "A busy community park on a sunny Saturday",
                "topic": "Community park"
            },
            {
                "id": "T3-P2",
                "scenario": "Imagine a bustling farmers' market on a weekend morning. There are vendors selling fresh fruits, vegetables, and baked goods. Musicians are performing near the entrance. Families are shopping and children are eating ice cream.",
                "scene_description": "A weekend farmers' market",
                "topic": "Farmers market"
            },
            {
                "id": "T3-P3",
                "scenario": "Imagine a modern office workspace during a busy workday. Some employees are working at their desks, others are having a meeting in a glass conference room. A person is making coffee in the kitchen area. The whiteboard has project plans written on it.",
                "scene_description": "A modern office workspace",
                "topic": "Office scene"
            },
            {
                "id": "T3-P4",
                "scenario": "Imagine a neighborhood street after a snowfall. Children are building a snowman in the front yard. A person is shoveling their driveway. A mail carrier is delivering packages. Holiday decorations are visible on some houses.",
                "scene_description": "A winter neighborhood scene",
                "topic": "Winter neighborhood"
            }
        ]
    },
    {
        "number": 4,
        "name": "Making Predictions",
        "description": "Look at a scene and make predictions about what will happen next.",
        "instructions": "Look at the scene you described. Now predict what you think will happen next. Use your imagination and explain your reasoning. You will have 30 seconds to prepare and 60 seconds to speak.",
        "prep_time": 30,
        "response_time": 60,
        "tips": [
            "Use future tense and predictive language",
            "Make 2-3 specific predictions",
            "Explain your reasoning for each prediction",
            "Use phrases like 'I think...', 'It's likely that...', 'Based on what I see...'",
            "Connect predictions to details in the scene"
        ],
        "prompts": [
            {
                "id": "T4-P1",
                "scenario": "Based on the park scene: The weather is starting to change — dark clouds are forming in the distance. Some vendors are looking up at the sky with concern.",
                "context": "Park scene with approaching weather change",
                "topic": "Park predictions"
            },
            {
                "id": "T4-P2",
                "scenario": "Based on the office scene: It's 4:30 PM on a Friday. The meeting in the conference room seems to be getting intense. One person's phone keeps buzzing.",
                "context": "Office scene near end of work week",
                "topic": "Office predictions"
            },
            {
                "id": "T4-P3",
                "scenario": "Based on a restaurant scene: A couple is having dinner at a fancy restaurant. The man looks nervous and keeps touching his jacket pocket. A waiter is bringing a special dessert with a candle.",
                "context": "Restaurant scene with nervous man",
                "topic": "Restaurant predictions"
            },
            {
                "id": "T4-P4",
                "scenario": "Based on a school scene: Students are gathering in the gymnasium. Some students are setting up decorations. A DJ is testing the sound equipment. Teachers are putting out refreshments.",
                "context": "School gymnasium being prepared for an event",
                "topic": "School event predictions"
            }
        ]
    },
    {
        "number": 5,
        "name": "Comparing and Persuading",
        "description": "Compare two options and persuade someone to choose one.",
        "instructions": "You will see two options. Compare them and persuade your friend to choose the one you prefer. Give clear reasons for your recommendation. You will have 60 seconds to prepare and 60 seconds to speak.",
        "prep_time": 60,
        "response_time": 60,
        "tips": [
            "Briefly acknowledge both options",
            "Clearly state which one you recommend",
            "Give 2-3 strong reasons for your choice",
            "Address potential concerns about your recommendation",
            "Use persuasive language: 'I strongly believe...', 'The main advantage is...'"
        ],
        "prompts": [
            {
                "id": "T5-P1",
                "scenario": "Your friend is deciding between two vacation options:\nOption A: A beach resort in Mexico — all-inclusive, relaxing, warm weather\nOption B: A hiking trip in the Canadian Rockies — adventurous, scenic, active\nPersuade your friend to choose one.",
                "option_a": "Beach resort in Mexico",
                "option_b": "Hiking trip in the Canadian Rockies",
                "topic": "Vacation choice"
            },
            {
                "id": "T5-P2",
                "scenario": "Your friend is choosing between two job offers:\nOption A: A large corporation — higher salary, good benefits, structured environment\nOption B: A startup company — lower salary, stock options, flexible and creative culture\nPersuade your friend to choose one.",
                "option_a": "Large corporation job",
                "option_b": "Startup company job",
                "topic": "Job choice"
            },
            {
                "id": "T5-P3",
                "scenario": "Your friend wants to learn a new skill and is deciding between:\nOption A: Taking an online course — flexible schedule, self-paced, cheaper\nOption B: Attending in-person classes — structured learning, networking, hands-on practice\nPersuade your friend to choose one.",
                "option_a": "Online course",
                "option_b": "In-person classes",
                "topic": "Learning method"
            },
            {
                "id": "T5-P4",
                "scenario": "Your friend is deciding where to live:\nOption A: Downtown apartment — convenient, close to work, nightlife, but small and expensive\nOption B: Suburban house — spacious, quiet, affordable, but longer commute\nPersuade your friend to choose one.",
                "option_a": "Downtown apartment",
                "option_b": "Suburban house",
                "topic": "Living situation"
            }
        ]
    },
    {
        "number": 6,
        "name": "Dealing with a Difficult Situation",
        "description": "Handle a challenging situation by explaining what you would say and do.",
        "instructions": "You will hear about a difficult situation. Explain how you would deal with it. Think about what you would SAY to the people involved and what ACTIONS you would take. You will have 60 seconds to prepare and 60 seconds to speak.",
        "prep_time": 60,
        "response_time": 60,
        "tips": [
            "Show empathy and understanding first",
            "Describe specific actions you would take",
            "Include what you would SAY to others",
            "Propose a fair solution or compromise",
            "Maintain a professional and calm tone"
        ],
        "prompts": [
            {
                "id": "T6-P1",
                "scenario": "You ordered furniture online three weeks ago. The delivery was supposed to arrive last week, but it still hasn't come. When you call customer service, they say there's no record of your order, even though you have the confirmation email. What do you say and do?",
                "situation": "Missing furniture delivery with no record",
                "topic": "Customer service dispute"
            },
            {
                "id": "T6-P2",
                "scenario": "You are working on a group project at work. One team member has not been contributing their share of the work, and the deadline is in two days. The rest of the team is frustrated. As the team lead, what do you say and do?",
                "situation": "Uncooperative team member near deadline",
                "topic": "Workplace conflict"
            },
            {
                "id": "T6-P3",
                "scenario": "You live in an apartment building. Your upstairs neighbor plays loud music late at night, and it has been affecting your sleep and work performance. You have already spoken to them once, but the noise continues. What do you say and do?",
                "situation": "Persistent noisy neighbor",
                "topic": "Neighbor conflict"
            },
            {
                "id": "T6-P4",
                "scenario": "You are at a restaurant celebrating a friend's birthday. The service is extremely slow, the food arrives cold, and one person in your group received the wrong order. The bill also includes items you didn't order. What do you say and do?",
                "situation": "Bad restaurant experience during celebration",
                "topic": "Restaurant complaint"
            }
        ]
    },
    {
        "number": 7,
        "name": "Expressing Opinions",
        "description": "Express and support your opinion on a given topic.",
        "instructions": "You will be asked about your opinion on a topic. State your opinion clearly and support it with reasons and examples. You will have 30 seconds to prepare and 90 seconds to speak.",
        "prep_time": 30,
        "response_time": 90,
        "tips": [
            "State your opinion clearly at the beginning",
            "Support with 2-3 strong reasons",
            "Use specific examples from your experience or knowledge",
            "Acknowledge the opposing view briefly",
            "Conclude by restating your position"
        ],
        "prompts": [
            {
                "id": "T7-P1",
                "scenario": "Some people believe that working from home is more productive than working in an office. Others think that being in the office is essential for collaboration and focus. What is your opinion?",
                "topic": "Remote work vs. office work"
            },
            {
                "id": "T7-P2",
                "scenario": "Some people think that social media has made people more connected, while others believe it has actually made people more isolated. What is your opinion?",
                "topic": "Social media and connection"
            },
            {
                "id": "T7-P3",
                "scenario": "There is a debate about whether children should be required to learn a musical instrument or participate in sports. Some say it builds discipline, others say children should choose their own activities. What do you think?",
                "topic": "Structured activities for children"
            },
            {
                "id": "T7-P4",
                "scenario": "Many cities are considering banning single-use plastics like bags and straws to help the environment. Some people support this, while others think it is inconvenient and won't make a real difference. What is your opinion?",
                "topic": "Banning single-use plastics"
            },
            {
                "id": "T7-P5",
                "scenario": "Some people believe that university education is essential for career success, while others argue that practical experience and self-learning are more valuable. What is your opinion?",
                "topic": "University education vs. practical experience"
            }
        ]
    },
    {
        "number": 8,
        "name": "Describing an Unusual Situation",
        "description": "Describe an unusual situation and explain what you would do about it.",
        "instructions": "You will hear about an unusual situation. Describe what is unusual about it and explain what you would do. You will have 30 seconds to prepare and 60 seconds to speak.",
        "prep_time": 30,
        "response_time": 60,
        "tips": [
            "Clearly identify what is unusual about the situation",
            "Describe the situation in detail",
            "Explain what you would do step by step",
            "Consider different possible explanations",
            "Show logical thinking and problem-solving"
        ],
        "prompts": [
            {
                "id": "T8-P1",
                "scenario": "You come home from work and find that your front door is wide open. The lights inside are on, but you are sure you turned them off and locked the door before leaving this morning.",
                "situation": "Open front door when you left it locked",
                "topic": "Unexpected open door"
            },
            {
                "id": "T8-P2",
                "scenario": "You arrive at your workplace on Monday morning and find that all the furniture in your office has been rearranged. Your desk is now facing the wall, and someone else's belongings are on your desk. No one told you about any changes.",
                "situation": "Office rearranged without notice",
                "topic": "Office rearrangement"
            },
            {
                "id": "T8-P3",
                "scenario": "You are at a grocery store and notice that every item on one particular shelf has a price tag of $0.01. The items are expensive organic products that normally cost $10-$15 each. No store employee seems to be aware of this.",
                "situation": "Mispriced items at the grocery store",
                "topic": "Mispriced groceries"
            },
            {
                "id": "T8-P4",
                "scenario": "You go to pick up your car from the parking lot after work and find a different car parked in your spot — the same color and model as yours. Your car is nowhere to be seen, but the keys to this other car are sitting on the dashboard.",
                "situation": "Your car replaced by an identical one",
                "topic": "Missing car mystery"
            }
        ]
    }
]


def get_task_with_prompt(task_number: int) -> dict | None:
    """Get a specific task with a randomly selected prompt."""
    for task in CELPIP_TASKS:
        if task["number"] == task_number:
            prompt = random.choice(task["prompts"])
            return {
                **{k: v for k, v in task.items() if k != "prompts"},
                "prompt": prompt,
                "total_prompts": len(task["prompts"])
            }
    return None


def get_full_test_sequence() -> list:
    """Get all 8 tasks with random prompts for a full test simulation."""
    test = []
    for task in CELPIP_TASKS:
        prompt = random.choice(task["prompts"])
        test.append({
            **{k: v for k, v in task.items() if k != "prompts"},
            "prompt": prompt
        })
    return test
