from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json
import random
import re
import requests
import uuid
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import string

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = 'mindfulchat_secret_key'  # For session management

# Download NLTK resources if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('wordnet')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load responses from JSON file
with open('responses.json', 'r') as f:
    responses = json.load(f)

# User session storage - in a production environment, this would be a database
conversation_history = {}
user_profiles = {}

# HuggingFace API for complex queries (free tier)
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HUGGINGFACE_API_KEY = ""  # Add your free API key here

# Common conversation patterns for more natural response selection
conversation_patterns = {
    'greeting': [
        'hi', 'hello', 'hey', 'sup', 'whats up', "what's up", 'yo', 'hiya', 
        'morning', 'afternoon', 'evening', 'howdy'
    ],
    'farewell': [
        'bye', 'goodbye', 'see ya', 'see you', 'talk later', 'cya', 'gtg', 
        'got to go', 'have to go', 'catch you later', 'peace'
    ],
    'thanks': [
        'thanks', 'thank you', 'thx', 'ty', 'appreciate', 'grateful', 'thks'
    ],
    'agreement': [
        'yes', 'yeah', 'yep', 'sure', 'ok', 'okay', 'alright', 'i agree', 
        'that sounds good', 'sounds good', 'that works', 'works for me'
    ],
    'disagreement': [
        'no', 'nope', 'nah', 'i disagree', 'not really', 'don\'t think so',
        'i don\'t think so', 'not sure', 'disagree'
    ],
    'confusion': [
        'confused', 'don\'t understand', 'what do you mean', 'unclear', 
        'i\'m lost', 'what?', 'huh?', 'not following'
    ],
    'positive_emotion': [
        'happy', 'glad', 'excited', 'great', 'awesome', 'excellent', 'amazing',
        'wonderful', 'fantastic', 'good', 'nice', 'cool', 'love', 'joy'
    ],
    'negative_emotion': [
        'sad', 'upset', 'depressed', 'unhappy', 'angry', 'frustrated', 'anxious',
        'stressed', 'worried', 'annoyed', 'terrible', 'awful', 'bad', 'sucks'
    ],
    'help_request': [
        'help', 'assist', 'support', 'advice', 'guidance', 'solution', 'tip',
        'suggestion', 'recommend', 'what should i do', 'how can i'
    ]
}

# Categories and their extended keywords
categories = {
    'financial': [
        'money', 'financial', 'expensive', 'afford', 'cost', 'debt', 'loan', 'budget', 'tuition', 
        'rent', 'bills', 'payment', 'broke', 'poor', 'income', 'scholarship', 'grant', 'funding',
        'pay', 'finance', 'economic', 'dollar', 'cash', 'salary', 'wage', 'bank', 'spending',
        'savings', 'borrow', 'credit card', 'funds', 'expensive', 'cheap', 'price', 'paid'
    ],
    'loneliness': [
        'alone', 'lonely', 'isolated', 'no friends', 'left out', 'excluded', 'outcast', 'rejection',
        'disconnected', 'friendless', 'abandoned', 'solitary', 'social', 'connect', 'belong', 'inclusion',
        'relationship', 'interact', 'companionship', 'alienated', 'outsider', 'withdrawn', 'detached',
        'no one', 'by myself', 'miss', 'missing', 'homesick', 'hard to make friends', 'quiet',
        'shy', 'awkward', 'uncomfortable', 'don\'t fit in', 'don\'t belong', 'no group'
    ],
    'academic': [
        'grades', 'exam', 'study', 'assignment', 'academic', 'course', 'homework', 'class', 'lecture',
        'professor', 'test', 'essay', 'deadline', 'research', 'paper', 'quiz', 'gpa', 'fail', 'pass',
        'degree', 'major', 'minor', 'credit', 'semester', 'thesis', 'graduation', 'procrastination',
        'finals', 'midterm', 'assignment', 'project', 'lab', 'reading', 'textbook', 'notes',
        'studying', 'college', 'university', 'school', 'learned', 'learning', 'education', 'student',
        'teacher', 'instructor', 'course load', 'subjects', 'semester'
    ],
    'stress': [
        'stress', 'pressure', 'overwhelmed', 'anxiety', 'worried', 'tension', 'burnout', 'exhausted',
        'panic', 'nervous', 'fear', 'dread', 'distress', 'frazzled', 'apprehensive', 'strain', 'burden',
        'troubled', 'upset', 'restless', 'tense', 'anxious', 'agitated', 'frustrated', 'can\'t sleep',
        'insomnia', 'too much', 'can\'t handle', 'can\'t cope', 'freaking out', 'breaking down', 
        'losing it', 'mental health', 'therapy', 'counseling', 'depressed', 'depression',
        'psychiatrist', 'psychologist', 'medication', 'treatment', 'self-care'
    ],
    'general': [
        'help', 'sad', 'depressed', 'confused', 'uncertain', 'lost', 'stuck', 'unsure', 'advice',
        'guidance', 'support', 'direction', 'question', 'recommend', 'suggest', 'opinion', 'perspective',
        'thought', 'feeling', 'emotion', 'mental', 'health', 'wellbeing', 'therapy', 'counseling',
        'how are you', 'what\'s up', 'hey', 'hello', 'hi', 'life', 'situation', 'problem', 
        'issue', 'difficulty', 'challenge', 'struggle', 'concerned', 'worried', 'wondering'
    ],
    'hobbies': [
        'hobby', 'hobbies', 'fun', 'interest', 'interests', 'pastime', 'activity', 'activities',
        'sport', 'sports', 'game', 'games', 'play', 'playing', 'art', 'music', 'reading', 'books',
        'collect', 'collection', 'craft', 'crafts', 'baking', 'cooking', 'hiking', 'biking',
        'running', 'swimming', 'exercise', 'workout', 'gym', 'dance', 'dancing', 'sing', 'singing',
        'instrument', 'draw', 'drawing', 'paint', 'painting', 'photography', 'video games', 'gaming'
    ],
    'entertainment': [
        'movie', 'movies', 'show', 'shows', 'tv', 'television', 'series', 'film', 'watch', 'watching',
        'stream', 'streaming', 'netflix', 'hulu', 'disney', 'amazon', 'youtube', 'music', 'song', 'songs',
        'album', 'concert', 'band', 'artist', 'podcast', 'podcasts', 'book', 'books', 'novel', 'read',
        'reading', 'game', 'games', 'gaming', 'video game', 'play', 'playing', 'theater', 'performance'
    ],
    'campus_life': [
        'campus', 'dorm', 'roommate', 'roommates', 'housing', 'dining hall', 'cafeteria', 'library',
        'club', 'clubs', 'organization', 'organizations', 'event', 'events', 'party', 'parties',
        'greek life', 'fraternity', 'sorority', 'student center', 'rec center', 'gym', 'quad',
        'campus tour', 'orientation', 'freshman', 'sophomore', 'junior', 'senior', 'undergrad',
        'tradition', 'football', 'basketball', 'sports', 'game', 'games', 'tailgate'
    ],
    'food': [
        'food', 'eat', 'eating', 'meal', 'meals', 'dining', 'dining hall', 'cafeteria', 'restaurant',
        'restaurants', 'cook', 'cooking', 'recipe', 'recipes', 'snack', 'snacks', 'dinner', 'lunch',
        'breakfast', 'brunch', 'coffee', 'drinks', 'drink', 'cuisine', 'delicious', 'tasty', 'yummy',
        'favorite food', 'hungry', 'starving', 'order in', 'takeout', 'delivery', 'kitchen'
    ],
    'future_plans': [
        'future', 'plan', 'plans', 'planning', 'goal', 'goals', 'dream', 'dreams', 'aspiration',
        'aspirations', 'career', 'job', 'jobs', 'internship', 'internships', 'graduation', 'graduate',
        'after college', 'post-grad', 'grad school', 'masters', 'phd', 'doctorate', 'professional',
        'resume', 'interview', 'company', 'industry', 'field', 'five year plan', 'long term'
    ],
    'technology': [
        'tech', 'technology', 'computer', 'laptop', 'phone', 'smartphone', 'app', 'apps', 'software',
        'hardware', 'device', 'devices', 'gadget', 'gadgets', 'internet', 'online', 'digital', 'social media',
        'instagram', 'twitter', 'facebook', 'tiktok', 'snapchat', 'website', 'ai', 'artificial intelligence',
        'vr', 'virtual reality', 'ar', 'augmented reality', 'coding', 'programming'
    ],
    'weather': [
        'weather', 'sunny', 'sun', 'rain', 'rainy', 'snow', 'snowy', 'cold', 'hot', 'warm', 'cool',
        'temperature', 'climate', 'forecast', 'storm', 'cloudy', 'clouds', 'wind', 'windy', 'humid',
        'humidity', 'season', 'seasonal', 'spring', 'summer', 'fall', 'autumn', 'winter'
    ],
    'positive_chat': [
        'happy', 'happiness', 'joy', 'grateful', 'thankful', 'appreciate', 'appreciation', 'proud',
        'accomplishment', 'success', 'win', 'winning', 'achievement', 'celebrate', 'celebration',
        'exciting', 'excited', 'looking forward', 'optimistic', 'positive', 'good news', 'smile',
        'laughed', 'laugh', 'fun', 'enjoyed', 'enjoy', 'pleasure', 'pleased', 'satisfying'
    ],
    'casual_chat': [
        'chat', 'talk', 'talking', 'conversation', 'catch up', 'what\'s new', 'been up to',
        'these days', 'lately', 'weekend', 'day', 'week', 'today', 'yesterday', 'tomorrow',
        'plans', 'happening', 'going on', 'what are you', 'how are you', 'how\'s it going',
        'how\'s life', 'how have you been', 'what have you been', 'tell me about'
    ]
}

def preprocess_text(text):
    """Preprocess text by tokenizing, converting to lowercase, and lemmatizing"""
    # Remove punctuation
    text = text.lower()
    text = ''.join([char for char in text if char not in string.punctuation])
    
    # Tokenize and lemmatize
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatized_tokens

def detect_conversation_pattern(text):
    """Detect if message matches common conversation patterns"""
    text_lower = text.lower()
    
    # Check for patterns
    for pattern, phrases in conversation_patterns.items():
        for phrase in phrases:
            if phrase in text_lower or text_lower.startswith(phrase + ' ') or text_lower == phrase:
                return pattern
    
    return None

def get_conversational_response(pattern, user_id=None):
    """Generate a natural conversational response for common patterns"""
    # Personalize with name if we have it
    user_name = ""
    if user_id in user_profiles and "name" in user_profiles[user_id]:
        user_name = user_profiles[user_id]["name"]
    
    # Map patterns to friendly, casual responses
    if pattern == 'greeting':
        if 'greetings' in responses:
            return random.choice(responses['greetings']), 'greetings'
        else:
            greetings = [
                f"Hey there! How's it going today?",
                f"Hi! What's been on your mind lately?",
                f"Hello! How's your day shaping up?",
                f"Hey! Good to hear from you. How are things?",
                f"Hi there! What's happening in your world today?"
            ]
            return random.choice(greetings), 'general'
    
    elif pattern == 'farewell':
        if 'farewells' in responses:
            return random.choice(responses['farewells']), 'farewells'
        else:
            farewells = [
                f"Talk to you later! Remember I'm here whenever you need me.",
                f"Take care! Come back anytime you want to chat.",
                f"Bye for now! Hope the rest of your day goes well.",
                f"See you soon! I'll be here when you want to talk again.",
                f"Later! Remember to be kind to yourself today."
            ]
            return random.choice(farewells), 'general'
    
    elif pattern == 'thanks':
        thanks_responses = [
            f"No problem at all! That's what friends are for.",
            f"Happy to help! What else is on your mind?",
            f"Anytime! I'm always here to listen and chat.",
            f"You're welcome! Is there anything else you'd like to talk about?",
            f"That's what I'm here for! How are you feeling now?"
        ]
        return random.choice(thanks_responses), 'general'
    
    elif pattern == 'confusion':
        clarifications = [
            f"Sorry if I wasn't clear! What part confused you?",
            f"Let me try to explain that better. What didn't make sense?",
            f"My bad if that was confusing. Let's try a different approach.",
            f"Sometimes I don't express things well. What would help make it clearer?",
            f"Sorry about that! Let me try again in a simpler way."
        ]
        return random.choice(clarifications), 'general'
    
    # For more complex patterns, get a more specific response
    return None, None

def extract_potential_name(message):
    """Try to extract a user's name if they introduce themselves"""
    name_patterns = [
        r"(?:i'm|i am|call me|name is|this is)\s+([A-Z][a-z]+)",
        r"(?:my name's|my name is)\s+([A-Z][a-z]+)"
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, message)
        if match:
            return match.group(1)
    
    return None

def detect_casual_conversation_topic(message):
    """Detect which casual conversation topic the message is most related to"""
    text_lower = message.lower()
    topic_scores = {}
    
    # Check for keywords in casual conversation categories
    casual_categories = ['hobbies', 'entertainment', 'campus_life', 'food', 
                         'future_plans', 'technology', 'weather', 'positive_chat', 'casual_chat']
    
    for category in casual_categories:
        if category in categories:
            score = 0
            for keyword in categories[category]:
                if keyword in text_lower:
                    score += 1
                # Check for questions about the topic
                question_patterns = [
                    f"do you {keyword}", f"what {keyword}", f"how about {keyword}",
                    f"like {keyword}", f"enjoy {keyword}", f"favorite {keyword}"
                ]
                for pattern in question_patterns:
                    if pattern in text_lower:
                        score += 2  # Questions about topics get higher weight
            
            topic_scores[category] = score
    
    # Get the most relevant casual topic
    if topic_scores:
        max_score = max(topic_scores.values())
        if max_score > 0:
            best_topics = [t for t, s in topic_scores.items() if s == max_score]
            return random.choice(best_topics)
    
    # If no specific casual topic is detected
    return 'casual_chat'

def analyze_message_advanced(message, user_id=None):
    """Analyze message with more sophisticated natural language processing"""
    # Try to extract user name for personalization
    potential_name = extract_potential_name(message)
    if potential_name and user_id:
        if user_id not in user_profiles:
            user_profiles[user_id] = {}
        user_profiles[user_id]["name"] = potential_name
    
    # Check for common conversation patterns first
    conversation_pattern = detect_conversation_pattern(message)
    if conversation_pattern:
        # Map 'greeting' to 'greetings' to match the responses.json format
        if conversation_pattern == 'greeting':
            return 'greetings', "conversation_pattern"
        elif conversation_pattern == 'farewell':
            return 'farewells', "conversation_pattern"
        else:
            return conversation_pattern, "conversation_pattern"
    
    # Preprocess the message
    processed_tokens = preprocess_text(message)
    
    # Check for casual conversation topics
    if len(message.split()) < 15 and not any(word in message.lower() for word in ['help', 'problem', 'issue', 'worried', 'anxious', 'stress']):
        # This might be casual conversation rather than seeking help
        casual_topic = detect_casual_conversation_topic(message)
        if casual_topic and casual_topic in responses:
            return casual_topic, None
    
    # Count occurrences of keywords for each category
    category_scores = {category: 0 for category in categories}
    
    # Look for multi-word phrases first (more specific)
    for category, keywords in categories.items():
        for keyword in keywords:
            if ' ' in keyword and keyword.lower() in message.lower():
                category_scores[category] += 3  # Higher weight for multi-word matches
    
    # Then check individual tokens
    for token in processed_tokens:
        for category, keywords in categories.items():
            for keyword in keywords:
                if ' ' not in keyword and token == keyword:
                    category_scores[category] += 1
                # Partial matching for longer keywords
                elif len(token) > 3 and len(keyword) > 3 and token in keyword:
                    category_scores[category] += 0.5
    
    # Check user history for context if available
    if user_id and user_id in conversation_history:
        history = conversation_history[user_id]
        if len(history) >= 2:
            # If previous interactions were about a certain category, boost that category's score
            prev_categories = [msg.get('category', 'general') for msg in history[-3:]]
            for prev_cat in prev_categories:
                if prev_cat in category_scores:
                    category_scores[prev_cat] += 0.5
            
            # Check for topic continuity
            if history[-1].get('role') == 'bot':
                last_bot_msg = history[-1].get('text', '').lower()
                if '?' in last_bot_msg:
                    # If bot asked a question and user replied, boost the category of the question
                    category_scores[history[-1].get('category', 'general')] += 1
    
    # Get the category with the highest score
    max_score = max(category_scores.values())
    if max_score > 0:
        # If there's a clear match, use that category
        strongest_categories = [cat for cat, score in category_scores.items() if score == max_score]
        return random.choice(strongest_categories), None
    
    # If no category matches well or it's very general, use 'general'
    return 'general', None

def find_relevant_messages(history, current_message, max_count=3):
    """Find the most contextually relevant previous messages"""
    if not history or len(history) <= 1:
        return []
    
    # Get the most recent messages, excluding the current message
    recent_messages = [msg for msg in history[-7:-1] if msg.get('role') == 'user']
    
    # If too few messages, just return what we have
    if len(recent_messages) <= max_count:
        return recent_messages
    
    # Tokenize the current message
    current_tokens = set(preprocess_text(current_message))
    
    # Score previous messages based on token overlap
    scored_messages = []
    for msg in recent_messages:
        msg_tokens = set(preprocess_text(msg.get('text', '')))
        overlap = len(current_tokens.intersection(msg_tokens))
        scored_messages.append((overlap, msg))
    
    # Sort by relevance score (highest first)
    scored_messages.sort(reverse=True)
    
    # Return the most relevant messages
    return [msg for _, msg in scored_messages[:max_count]]

def get_response_with_context(category, user_id, conversation_pattern=None):
    """Get a response based on category and conversation context"""
    # If it's a common conversation pattern, handle it differently
    if conversation_pattern:
        response, response_category = get_conversational_response(conversation_pattern, user_id)
        if response:
            return response, response_category
    
    # Safety check - make sure the category exists in responses
    if category not in responses:
        print(f"Warning: Category '{category}' not found in responses, using 'general' instead")
        category = 'general'
    
    # Get a basic response from the category
    basic_response = random.choice(responses[category])
    
    # If we don't have context, return a basic response
    if user_id not in conversation_history or len(conversation_history[user_id]) < 2:
        return basic_response, category
    
    # Check conversation history for patterns
    history = conversation_history[user_id]
    last_messages = [msg.get('text', '') for msg in history[-3:] if msg.get('role') == 'user']
    last_message = history[-1].get('text', '') if history[-1].get('role') == 'user' else ''
    
    # Add personalization if we know the user's name
    user_name = ""
    if user_id in user_profiles and "name" in user_profiles[user_id]:
        user_name = user_profiles[user_id]["name"]
        # Occasionally use the name in responses (not every time)
        if random.random() < 0.3 and len(user_name) > 0:
            basic_response = f"{basic_response}"
            if "?" not in basic_response:
                basic_response += f" {user_name}."
            else:
                basic_response = basic_response.replace("?", f", {user_name}?")
    
    # Pattern: User has mentioned the same category multiple times - they may need deeper support
    if category != 'general' and any(category == msg.get('category') for msg in history[-3:] if msg.get('role') == 'bot'):
        # Add empathy or validation sometimes
        if random.random() < 0.5 and 'empathy' in responses:
            empathy = random.choice(responses.get('empathy', []))
            return f"{empathy} {basic_response}", category
        
        # Add validation sometimes
        if random.random() < 0.4 and 'validation' in responses:
            validation = random.choice(responses.get('validation', []))
            return f"{validation} {basic_response}", category
    
    # Pattern: User is making progress - offer positive reinforcement
    positive_indicators = ['better', 'improved', 'trying', 'progress', 'helped', 'good', 'working on', 'thanks', 'thank you']
    if any(indicator in " ".join(last_messages).lower() for indicator in positive_indicators):
        if random.random() < 0.7 and 'positive_reinforcement' in responses:
            reinforcement = random.choice(responses['positive_reinforcement'])
            return f"{reinforcement} {basic_response}", 'positive_reinforcement'
    
    # Pattern: User mentions coping or strategies - offer specific coping mechanisms
    coping_indicators = ['cope', 'deal with', 'manage', 'strategy', 'technique', 'help me', 'suggestion', 'advice', 'how do I', 'what can I']
    if any(indicator in " ".join(last_messages).lower() for indicator in coping_indicators):
        if random.random() < 0.7 and 'coping_strategies' in responses:
            coping_strategy = random.choice(responses['coping_strategies'])
            return coping_strategy, 'coping_strategies'
    
    # For emotional messages, add an empathetic response
    emotional_words = ['sad', 'depressed', 'anxious', 'worried', 'scared', 'lonely', 'overwhelmed', 'stressed', 'upset']
    if any(word in last_message.lower() for word in emotional_words):
        if random.random() < 0.6 and 'empathy' in responses:
            empathy = random.choice(responses.get('empathy', []))
            return f"{empathy} {basic_response}", 'empathy'
    
    # If the user asks a question, make sure we give an answer, not just ask another question
    if last_message.endswith('?') and basic_response.endswith('?'):
        # If our basic response is also a question, try to get a non-question response
        non_question_responses = [r for r in responses[category] if not r.endswith('?')]
        if non_question_responses:
            return random.choice(non_question_responses), category
    
    # Provide a more varied response structure - sometimes combine multiple response types
    if random.random() < 0.3:
        category_options = list(responses.keys())
        random_category = random.choice(category_options)
        if random_category != category and random_category not in ['empathy', 'validation', 'positive_reinforcement', 'coping_strategies']:
            if random_category in responses:
                additional_response = random.choice(responses[random_category])
                # Don't make the combined response too long
                if len(basic_response) + len(additional_response) < 200:
                    return f"{basic_response} {additional_response}", category
    
    return basic_response, category

def call_huggingface_api(input_text, history=None):
    """Call HuggingFace API for complex or undefined queries"""
    if not HUGGINGFACE_API_KEY:
        return None
    
    # Include conversation history for better context
    conversation_context = ""
    if history and len(history) > 0:
        # Get last few exchanges
        recent_exchanges = history[-6:]  # Last 3 exchanges (6 messages)
        for msg in recent_exchanges:
            role = "User: " if msg.get('role') == 'user' else "Assistant: "
            conversation_context += f"{role}{msg.get('text', '')}\n"
    
    # Combine context with current input
    full_input = conversation_context + f"User: {input_text}\nAssistant:"
    
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": full_input}
    
    try:
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()[0].get('generated_text')
        else:
            print(f"HuggingFace API error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Error calling HuggingFace API: {e}")
        return None

def get_session_id():
    """Generate or retrieve a session ID for the current user"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']

def create_fallback_response(message, user_id=None):
    """Create a more intelligent fallback response when external API fails"""
    # Try to extract the core question or concern
    question_pattern = re.search(r'(?:can|could|would|how|why|what|when|where|is|are|do|does|did|should|has|have).*\?', message, re.IGNORECASE)
    
    # Get user name if available
    user_name = ""
    if user_id in user_profiles and "name" in user_profiles[user_id]:
        user_name = user_profiles[user_id]["name"]
        name_prefix = f"{user_name}, " if random.random() < 0.3 else ""
    else:
        name_prefix = ""
    
    # For questions, acknowledge we need to think more
    if question_pattern:
        questioning_responses = [
            f"{name_prefix}That's a great question. I need to think about that more, but my initial thought is that it depends on your specific situation. Could you tell me more about what you're experiencing?",
            f"I'm still learning about that topic. What aspect of it matters most to you right now?",
            f"That's something I'd like to explore with you. Before I share my thoughts, could you tell me why you're asking about this?",
            f"That's an interesting question. I don't have a simple answer, but I'd be happy to discuss it more with you. What are your thoughts on it?",
            f"{name_prefix}I appreciate you bringing that up. It's a complex topic, and I'd like to understand your perspective better before responding. What led you to ask about this?"
        ]
        return random.choice(questioning_responses), 'general'
    
    # For statements or general conversation
    general_responses = [
        f"{name_prefix}I appreciate you sharing that with me. Would you like to tell me more about what's been on your mind lately?",
        f"Thanks for opening up. I'm here to listen whenever you want to talk more about it.",
        f"I value your perspective on this. Is there a specific aspect you'd like to explore further?",
        f"{name_prefix}That's really insightful. How long have you been thinking about this?",
        f"I hear you. Sometimes it helps to talk these things through. What else has been going on?"
    ]
    return random.choice(general_responses), 'general'

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests with context tracking and advanced NLP"""
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get or create user session ID
        user_id = data.get('userId') or get_session_id()
        
        # Initialize user history if not exists
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        # Add user message to history
        conversation_history[user_id].append({
            'text': user_message,
            'role': 'user',
            'timestamp': data.get('timestamp', '')
        })
        
        # Analyze message to determine category and conversation pattern
        category, conversation_pattern = analyze_message_advanced(user_message, user_id)
        
        # Get contextual response
        response_text, response_category = get_response_with_context(category, user_id, conversation_pattern)
        
        # For general category with longer messages, try to use external API first
        should_use_api = (category == 'general' and len(user_message.split()) > 10) or data.get('forceApi', False)
        
        if should_use_api:
            api_response = call_huggingface_api(user_message, conversation_history[user_id])
            if api_response:
                response_text = api_response
                response_category = 'general'
            else:
                # If API fails, create a more intelligent fallback
                fallback_response, fallback_category = create_fallback_response(user_message, user_id)
                response_text = fallback_response
                response_category = fallback_category
        
        # Add bot response to history
        conversation_history[user_id].append({
            'text': response_text,
            'role': 'bot',
            'category': response_category,
            'timestamp': data.get('timestamp', '')
        })
        
        # Limit history size to prevent memory issues (last 20 messages)
        if len(conversation_history[user_id]) > 20:
            conversation_history[user_id] = conversation_history[user_id][-20:]
        
        return jsonify({
            'response': response_text,
            'category': response_category,
            'userId': user_id
        })
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'response': "I'm having trouble processing that right now. Could you try again?",
            'category': 'general',
            'error': str(e)
        }), 200  # Return 200 instead of 500 to prevent CORS issues

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history for a user"""
    user_id = request.args.get('userId') or get_session_id()
    
    if user_id not in conversation_history:
        return jsonify({'history': []})
    
    return jsonify({
        'history': conversation_history[user_id],
        'userId': user_id
    })

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation history for a user"""
    user_id = request.json.get('userId') or get_session_id()
    
    if user_id in conversation_history:
        conversation_history[user_id] = []
    
    return jsonify({
        'success': True,
        'userId': user_id
    })

if __name__ == '__main__':
    app.run(debug=True) 