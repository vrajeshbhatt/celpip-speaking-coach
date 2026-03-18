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
        "number": 0,
        "name": "Practice Task (Unscored)",
        "description": "This is a warm-up task to help you get comfortable with the microphone and recording. It is NOT scored.",
        "instructions": "This practice task will help you get used to speaking into the microphone. Talk about the topic below. Remember, this task is NOT scored — it's just for practice. You will have 30 seconds to prepare and 60 seconds to speak.",
        "prep_time": 30,
        "response_time": 60,
        "is_practice": True,
        "tips": [
            "Use this time to test your microphone",
            "Get comfortable with the recording interface",
            "Practice speaking at a natural pace",
            "This task is NOT scored — relax and warm up"
        ],
        "prompts": [
            {
                "id": "T0-P1",
                "scenario": "Tell me about your favorite hobby or activity that you enjoy doing in your free time. Why do you enjoy it?",
                "topic": "Favorite hobby"
            },
            {
                "id": "T0-P2",
                "scenario": "Describe the city or town where you currently live. What do you like about it?",
                "topic": "Where you live"
            },
            {
                "id": "T0-P3",
                "scenario": "Talk about a meal or food that you really enjoy. What makes it special to you?",
                "topic": "Favorite food"
            }
        ]
    },
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
            },
            {"id": "T1-P6", "scenario": "Your friend wants to quit their stable job to become a full-time artist, but they have no financial safety net.", "situation": "Friend wants to quit job for art without savings.", "target": "your friend"},
            {"id": "T1-P7", "scenario": "Your colleague is extremely nervous about giving a major presentation to the CEO tomorrow morning.", "situation": "Colleague is nervous about CEO presentation.", "target": "your colleague"},
            {"id": "T1-P8", "scenario": "Your friend is considering quitting their secure job to travel the world for a year without much savings. Give them advice.", "situation": "Quitting job to travel without savings", "target": "your friend"},
            {"id": "T1-P9", "scenario": "Your cousin is about to go for their first major job interview and is extremely nervous. Give them advice on how to prepare and stay calm.", "situation": "Nervous about first job interview", "target": "your cousin"},
            {"id": "T1-P10", "scenario": "Your neighbor wants to start a large vegetable garden but has never planted anything before and has a very small backyard. Give them advice.", "situation": "Starting a garden with no experience", "target": "your neighbor"}
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
            },
            {"id": "T2-P6", "scenario": "Talk about a time you received a piece of advice that changed your perspective. What was it, and why was it important?", "topic": "Life-changing advice"},
            {"id": "T2-P7", "scenario": "Describe a time you had to work with someone who had a very different personality from yours. How did you manage to work together?", "topic": "Working with different personalities"},
            {"id": "T2-P8", "scenario": "Talk about a time when you had to make a difficult decision that affected your family or friends. What happened?", "topic": "A difficult decision"},
            {"id": "T2-P9", "scenario": "Describe a time when you received a gift that was very meaningful to you. Who gave it to you and why was it special?", "topic": "A meaningful gift"},
            {"id": "T2-P10", "scenario": "Talk about a project or achievement you are particularly proud of. What was it, and what did it take to accomplish?", "topic": "A proud achievement"}
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
                "topic": "Community park",
                "image_url": "https://images.unsplash.com/photo-1544365558-35aa4afcf11f?w=800&q=80"
            },
            {
                "id": "T3-P2",
                "scenario": "Imagine a bustling farmers' market on a weekend morning. There are vendors selling fresh fruits, vegetables, and baked goods. Musicians are performing near the entrance. Families are shopping and children are eating ice cream.",
                "scene_description": "A weekend farmers' market",
                "topic": "Farmers market",
                "image_url": "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?w=800&q=80"
            },
            {
                "id": "T3-P3",
                "scenario": "Imagine a modern office workspace during a busy workday. Some employees are working at their desks, others are having a meeting in a glass conference room. A person is making coffee in the kitchen area. The whiteboard has project plans written on it.",
                "scene_description": "A modern office workspace",
                "topic": "Office scene",
                "image_url": "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=800&q=80"
            },
            {
                "id": "T3-P4",
                "scenario": "Imagine a neighborhood street after a snowfall. Children are building a snowman in the front yard. A person is shoveling their driveway. A mail carrier is delivering packages. Holiday decorations are visible on some houses.",
                "scene_description": "A winter neighborhood scene",
                "topic": "Winter neighborhood",
                "image_url": "https://images.unsplash.com/photo-1517260739337-6799d239ce83?w=800&q=80"
            },
            {"id": "T3-P5", "scenario": "Imagine a bustling airport terminal. People are rushing to gates, some are sleeping on chairs, others are checking the large flight information screens. A child is waving at a plane through the window.", "scene_description": "A busy airport terminal", "topic": "Airport scene", "image_url": "https://images.unsplash.com/photo-1530521954074-e64f6810b32d?w=800&q=80"},
            {"id": "T3-P6", "scenario": "Imagine a quiet, grand library with high ceilings. Students are sitting at long wooden tables with laptops and stacks of books. A librarian is shelving books on a rolling ladder. Large windows show a rainy day outside.", "scene_description": "A quiet grand library", "topic": "Library scene", "image_url": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800&q=80"},
            {"id": "T3-P7", "scenario": "Imagine a busy rainy day at a city bus stop. People are holding umbrellas, some are splashing in puddles, a bus is approaching, and a street performer is playing music nearby.", "scene_description": "A rainy city bus stop", "topic": "Rainy bus stop", "image_url": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=800&q=80"},
            {"id": "T3-P8", "scenario": "Imagine a sunny rooftop terrace in a city. People are sitting at small tables, some are drinking coffee, others are looking at the skyline. There are plants in large pots and a small fountain.", "scene_description": "A sunny rooftop terrace", "topic": "Rooftop terrace", "image_url": "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=800&q=80"},
            {"id": "T3-P9", "scenario": "Imagine a crowded sports stadium during a game. Fans are cheering, waving flags, some are eating snacks. The players are in the middle of a play, and large screens show the score.", "scene_description": "A crowded sports stadium", "topic": "Sports stadium", "image_url": "https://images.unsplash.com/photo-1504450758481-7338eba7524a?w=800&q=80"}
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
                "scenario": "Based on the park scene: The weather is starting to change — dark clouds are forming in the distance. The families having picnics are starting to pack up.",
                "context": "Park scene with approaching weather change",
                "topic": "Park predictions",
                "image_url": "https://images.unsplash.com/photo-1544365558-35aa4afcf11f?w=800&q=80"
            },
            {
                "id": "T4-P2",
                "scenario": "Based on the busy farmers' market scene: Predict what the vendors and the shoppers might do in the next few minutes.",
                "context": "Busy outdoor farmers' market",
                "topic": "Market predictions",
                "image_url": "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?w=800&q=80"
            },
            {
                "id": "T4-P3",
                "scenario": "Based on the office scene: It's 4:30 PM on a Friday. The meeting in the conference room seems to be getting intense. One person's phone keeps buzzing.",
                "context": "Office scene near end of work week",
                "topic": "Office predictions",
                "image_url": "https://images.unsplash.com/photo-1497215728101-856f4ea42174?w=800&q=80"
            },
            {
                "id": "T4-P4",
                "scenario": "Based on the winter neighborhood scene: The mail carrier is arriving but the driveway is very icy and entirely unshoveled. Predict what might happen.",
                "context": "Winter neighborhood with mail carrier",
                "topic": "Winter neighborhood predictions",
                "image_url": "https://images.unsplash.com/photo-1517260739337-6799d239ce83?w=800&q=80"
            },
            {"id": "T4-P5", "scenario": "Based on the airport scene: A major announcement is made that several international flights have been canceled due to a storm. Predict the reactions and actions of the passengers.", "context": "Airport with canceled flights", "topic": "Airport predictions", "image_url": "https://images.unsplash.com/photo-1530521954074-e64f6810b32d?w=800&q=80"},
            {"id": "T4-P6", "scenario": "Based on the library scene: The power suddenly goes out in the entire library, leaving it in near darkness. Predict what the students and the librarian will do.", "context": "Library power outage", "topic": "Library predictions", "image_url": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800&q=80"},
            {"id": "T4-P7", "scenario": "Based on the rainy bus stop scene: A large car is driving through a puddle right next to the people waiting. Predict what will happen to the people and their reaction.", "context": "Rainy bus stop puddle splash", "topic": "Bus stop predictions", "image_url": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?w=800&q=80"},
            {"id": "T4-P8", "scenario": "Based on the rooftop terrace: A sudden strong gust of wind blows through the city. Predict what will happen to the items on the tables and the people.", "context": "Windy rooftop terrace", "topic": "Rooftop predictions", "image_url": "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=800&q=80"},
            {"id": "T4-P9", "scenario": "Based on the sports stadium: The home team scores a last-minute winning goal. Predict the reaction of the fans and the players.", "context": "Stadium winning goal", "topic": "Stadium predictions", "image_url": "https://images.unsplash.com/photo-1504450758481-7338eba7524a?w=800&q=80"}
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
            },
            {"id": "T5-P5", "scenario": "Your friend is deciding on transportation:\nOption A: Buying a new car \u2014 convenience, long-term asset, but expensive and high maintenance\nOption B: Using public transit and car-sharing \u2014 cost-effective, eco-friendly, but less flexible\nPersuade your friend to choose one.", "option_a": "Buying a new car", "option_b": "Public transit & car-sharing", "topic": "Transportation choice"},
            {"id": "T5-P6", "scenario": "Your friend is deciding where to live:\nOption A: A house with a big garden \u2014 privacy, space, nature, but more maintenance\nOption B: A modern condo with amenities \u2014 gym, pool, security, low maintenance, but less space\nPersuade your friend to choose one.", "option_a": "House with garden", "option_b": "Modern condo", "topic": "Home type choice"},
            {"id": "T5-P7", "scenario": "Your friend is deciding on a pet:\nOption A: A high-energy dog \u2014 needs long walks, training, but very loyal and fun\nOption B: A low-maintenance cat \u2014 independent, quiet, good for small spaces, but less active\nPersuade your friend to choose one.", "option_a": "High-energy dog", "option_b": "Low-maintenance cat", "topic": "Pet choice"},
            {"id": "T5-P8", "scenario": "Your friend is choosing a place to study:\nOption A: A quiet, traditional library \u2014 no distractions, very formal, but far away\nOption B: A lively, modern cafe \u2014 comfortable, near home, but can be noisy and crowded\nPersuade your friend to choose one.", "option_a": "Traditional library", "option_b": "Modern cafe", "topic": "Study spot choice"},
            {"id": "T5-P9", "scenario": "Your friend is deciding on a new skill to learn:\nOption A: A coding bootcamp \u2014 intensive, career-focused, but expensive and time-consuming\nOption B: A local language class \u2014 social, culturally enriching, but slower career progression\nPersuade your friend to choose one.", "option_a": "Coding bootcamp", "option_b": "Language class", "topic": "New skill choice"}
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
            },
            {"id": "T6-P5", "scenario": "You promised to help a close friend move to their new apartment today, but a major last-minute emergency has come up at work and you must stay late. Your friend is expecting you in an hour. What do you say and do?", "situation": "Canceling help for a move due to work emergency", "topic": "Social commitment conflict"},
            {"id": "T6-P6", "scenario": "You arrive at your hotel after a long flight and find that your room is dirty and smells like smoke, even though you booked a non-smoking room. The front desk tells you the hotel is fully booked and there are no other rooms. What do you say and do?", "situation": "Dirty hotel room when fully booked", "topic": "Hotel complaint"},
            {"id": "T6-P7", "scenario": "You are at a movie theater and the person behind you is talking loudly on their phone and kicking your seat. You have asked them to stop once, but they ignored you. What do you say and do?", "situation": "Rude person at movie theater", "topic": "Theater conflict"},
            {"id": "T6-P8", "scenario": "Your flight has been overbooked and the airline is asking for volunteers to take a later flight in exchange for a travel voucher. You have an important meeting tomorrow morning. What do you say and do?", "situation": "Overbooked flight with important meeting", "topic": "Airline dispute"},
            {"id": "T6-P9", "scenario": "You are at a library and notice someone is marking and tearing pages out of a rare, expensive reference book. The person seems unaware that they are being watched. What do you say and do?", "situation": "Vandalism at the library", "topic": "Library incident"}
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
            },
            {"id": "T7-P6", "scenario": "Some people argue that public transportation should be free for all citizens to encourage its use and reduce traffic. Others believe it should be funded by the people who use it. What is your opinion?", "topic": "Free public transit"},
            {"id": "T7-P7", "scenario": "Is it better for children to grow up in a small town with a tight-knit community or in a large city with more diverse opportunities? What is your opinion?", "topic": "Small town vs. large city childhood"},
            {"id": "T7-P8", "scenario": "Some people believe that every citizen should be required to perform one year of community service after high school. Others believe this should be entirely voluntary. What is your opinion?", "topic": "Mandatory community service"},
            {"id": "T7-P9", "scenario": "Do you think that the government should strictly regulate the amount of sugar in soft drinks to improve public health? Why or why not?", "topic": "Regulating sugar in drinks"},
            {"id": "T7-P10", "scenario": "In your opinion, is it more important for a city to invest in building more parks and green spaces or in improving public transportation infrastructure?", "topic": "Parks vs. Public Transit investment"}
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
            },
            {"id": "T8-P5", "scenario": "While walking through the city center, you see a person walking a full-grown peacock on a leash as if it were a dog. People are staring, but the peacock owner is acting perfectly normal.", "situation": "Person walking a peacock on a leash", "topic": "Unusual pet in public"},
            {"id": "T8-P6", "scenario": "You enter a local cafe and realize that all the staff and customers are dressed in elaborate 18th-century historical costumes. They are using old-fashioned language, but they are ordering modern lattes and using iPads. What do you say and do?", "situation": "Historical costume cafe with modern tech", "topic": "Time-traveler cafe mystery"},
            {"id": "T8-P7", "scenario": "You are at a park and see a tree where the leaves are perfectly square and glowing with a soft blue light. A small crowd has gathered, but no one seems to know what is happening.", "situation": "Glowing square-leaved tree", "topic": "Nature anomaly"},
            {"id": "T8-P8", "scenario": "You are walking down a street and notice a house that is built entirely upside down. The roof is on the ground, and the front door is at the very top, accessible only by a long ladder. People are coming and going as if it were normal.", "situation": "Upside-down house with ladder door", "topic": "Architectural anomaly"},
            {"id": "T8-P9", "scenario": "You go to a local lake and see a group of people having a picnic on a large, flat rock that is floating three feet above the surface of the water. The rock is not tethered to anything.", "situation": "Floating picnic rock anomaly", "topic": "Physics anomaly"}
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
    """Get all 8 scored tasks with random prompts for a full test simulation.
    Excludes Practice Task 0 (unscored warm-up).
    """
    test = []
    for task in CELPIP_TASKS:
        if task.get("is_practice", False):
            continue  # Skip unscored practice task
        prompt = random.choice(task["prompts"])
        test.append({
            **{k: v for k, v in task.items() if k != "prompts"},
            "prompt": prompt
        })
    return test


