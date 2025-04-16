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

# Load responses from JSON file as fallback
try:
    with open('responses.json', 'r') as f:
        responses = json.load(f)
except:
    responses = {}

# User session storage - in a production environment, this would be a database
conversation_history = {}
user_profiles = {}

# ShuttleAI API for better, more human-like responses
# You would need to sign up at https://shuttleai.app/ for a free API key
SHUTTLE_API_URL = "https://api.shuttleai.app/v1/chat/completions"
SHUTTLE_API_KEY = "shuttle-l8ph7k_RfY3hT1jhzdk_pcw2qvl-K6CQK_d3aXD008iq_kLsJ0_U2h1dHRsZUFJQ6Nzj3dWSIaWt-sVZRBiuxHmiN-m35ew-g5VSsZbQKpOa_2EhUTY"  # Add your free API key here

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
        name_greeting = f" {user_name}" if random.random() < 0.5 else ""
    else:
        name_greeting = ""
    
    # Map patterns to friendly, casual responses
    if pattern == 'greeting':
        greetings = [
            f"Hey{name_greeting}! How are you doing today?",
            f"Hi there{name_greeting}! What's up?",
            f"Hello{name_greeting}! How's it going?",
            f"Hey, good to see you{name_greeting}! How's your day been?",
            f"Hi{name_greeting}! What's happening?",
            f"Hey{name_greeting}! 👋 How's everything going?",
            f"Hi there! Nice to chat with you{name_greeting}!",
            f"Hey{name_greeting}! What's new with you?",
            f"Hello{name_greeting}! How's life treating you?",
            f"Hey{name_greeting}! Good to hear from you! How have you been?",
        ]
        return random.choice(greetings), 'greetings'
    
    elif pattern == 'farewell':
        farewells = [
            f"Talk to you later{name_greeting}! I'm here whenever you need me.",
            f"Take care{name_greeting}! Come back anytime.",
            f"Bye for now! Hope the rest of your day goes well{name_greeting}.",
            f"See you soon{name_greeting}! I'll be here when you want to talk again.",
            f"Later{name_greeting}! Have a good one!",
            f"Catch you later{name_greeting}! 👋",
            f"Goodbye{name_greeting}! It was nice chatting with you.",
            f"Until next time{name_greeting}! Take care of yourself.",
            f"See ya{name_greeting}! Drop by anytime you want to chat.",
            f"Bye{name_greeting}! Hope to talk again soon!"
        ]
        return random.choice(farewells), 'farewells'
    
    elif pattern == 'thanks':
        thanks_responses = [
            f"No problem at all{name_greeting}! That's what I'm here for.",
            f"Happy to help{name_greeting}! Anything else on your mind?",
            f"Anytime{name_greeting}! I'm always here to listen.",
            f"You're welcome{name_greeting}! Is there something else you'd like to chat about?",
            f"Of course{name_greeting}! How are you feeling now?",
            f"Glad I could help{name_greeting}! 😊",
            f"No worries{name_greeting}! That's why I'm here.",
            f"My pleasure{name_greeting}! Anything else I can help with?",
            f"You got it{name_greeting}! Always here when you need to talk.",
            f"Sure thing{name_greeting}! How's everything else going?"
        ]
        return random.choice(thanks_responses), 'general'
    
    elif pattern == 'confusion':
        clarifications = [
            f"Sorry if I wasn't clear{name_greeting}! What confused you?",
            f"Let me try again{name_greeting}. What didn't make sense?",
            f"My bad{name_greeting}! Let me explain differently.",
            f"Sorry about that{name_greeting}. What can I clarify?",
            f"I might have been a bit unclear. What part lost you{name_greeting}?",
            f"Oops, let me be clearer{name_greeting}! What part was confusing?",
            f"Sorry for the confusion{name_greeting}. Let's try a different approach.",
            f"My mistake{name_greeting}! Let me try to be more clear.",
            f"I didn't explain that well. What specifically confused you{name_greeting}?",
            f"Sorry about that{name_greeting}! Let's back up and try again."
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
        if conversation_pattern == 'greeting':
            return 'greetings', "conversation_pattern" 
        elif conversation_pattern == 'farewell':
            return 'farewells', "conversation_pattern"
        else:
            return conversation_pattern, "conversation_pattern"
    
    # Simple text matches for greetings that might be missed by the pattern detector
    text_lower = message.lower().strip()
    basic_greetings = ['hi', 'hello', 'hey', 'greetings', 'sup', 'yo', 'hiya', 'whats up', "what's up"]
    if text_lower in basic_greetings or text_lower.startswith('hi ') or text_lower.startswith('hello ') or text_lower.startswith('hey '):
        return 'greetings', "conversation_pattern"
    
    # Handle "how are you" variants directly
    how_are_you_patterns = ['how are you', 'how r u', 'how u doing', 'how are u', 'how you doing', 'hows it going', "how's it going"]
    if any(pattern in text_lower for pattern in how_are_you_patterns) or text_lower in how_are_you_patterns:
        return 'greetings', "conversation_pattern"
    
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

def call_shuttle_api(input_text, category, user_id=None):
    """Call ShuttleAI API to get a more natural response"""
    if not SHUTTLE_API_KEY:
        return None

    # Get user name for personalization if available
    user_name = ""
    if user_id in user_profiles and "name" in user_profiles[user_id]:
        user_name = user_profiles[user_id]["name"]
    
    # Get conversation history for context
    context = []
    if user_id in conversation_history:
        # Get last 5 messages for context
        for msg in conversation_history[user_id][-5:]:
            role = "user" if msg.get('role') == 'user' else "assistant"
            context.append({"role": role, "content": msg.get('text', '')})
    
    # Create a system prompt based on the category
    system_prompt = f"You are a friendly mental health support chatbot for college students. Be conversational, empathetic, and supportive. Use casual language with some slang and emojis occasionally to sound more natural and relatable. Your responses should be helpful but not clinical."
    
    if category == 'financial':
        system_prompt += " The student is asking about financial stress or money problems. Be understanding and offer practical advice."
    elif category == 'academic':
        system_prompt += " The student is asking about academic pressure or study-related stress. Provide supportive and practical guidance."
    elif category == 'loneliness':
        system_prompt += " The student is feeling lonely or socially isolated. Be especially empathetic and suggest ways to connect with others."
    elif category == 'stress':
        system_prompt += " The student is experiencing stress or anxiety. Offer calming techniques and supportive language."
    
    if user_name:
        system_prompt += f" The student's name is {user_name}, occasionally use their name naturally in your response."

    # Prepare the API request
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history for context
    if context:
        messages.extend(context)
    
    # Add the current user message
    messages.append({"role": "user", "content": input_text})
    
    # Log the request we're about to make
    print(f"ShuttleAI Request - Input: '{input_text}', Category: {category}")
    
    try:
        # Try using a smaller model first if the main one is out of credits
        models_to_try = ["shuttle-2", "shuttle-1", "shuttle-3"]
        
        for model in models_to_try:
            try:
                print(f"Trying model: {model}")
                response = requests.post(
                    SHUTTLE_API_URL,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {SHUTTLE_API_KEY}"
                    },
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 350
                    },
                    timeout=10  # Timeout after 10 seconds
                )
                
                # Log the response status
                print(f"ShuttleAI Response Status for {model}: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        result = response.json()
                        if 'choices' in result and len(result['choices']) > 0:
                            response_content = result['choices'][0]['message']['content']
                            print(f"ShuttleAI Response Content: '{response_content[:50]}...'")
                            return response_content
                        else:
                            print(f"ShuttleAI Response Missing Choices: {result}")
                    except Exception as parse_error:
                        print(f"ShuttleAI Response Parse Error: {parse_error}")
                elif response.status_code == 402:
                    # Out of credits for this model, try the next one
                    print(f"Out of credits for {model}, trying next model...")
                    continue
                else:
                    print(f"ShuttleAI Error with {model}: {response.text}")
                    # Try the next model if this one didn't work
                    continue
            except Exception as model_error:
                print(f"Error with model {model}: {model_error}")
                # Try the next model
                continue
    except Exception as e:
        print(f"Error calling ShuttleAI API: {e}")
    
    print("ShuttleAI Fallback: Using local responses")
    return None

def generate_custom_fallback_response(input_text, category, user_id=None):
    """Generate a custom fallback response when API fails"""
    
    # Get user name for personalization if available
    user_name = ""
    if user_id in user_profiles and "name" in user_profiles[user_id]:
        user_name = user_profiles[user_id]["name"]
        name_greeting = f" {user_name}" if random.random() < 0.3 else ""
    else:
        name_greeting = ""
    
    # Add some randomness to make responses feel more natural
    emojis = ["", "", "", "😊", "👋", "💭", "🎓", "💬", "🙂", "👍"]
    emoji = random.choice(emojis)
    
    # Common phrase starters based on category
    financial_starters = [
        f"Talking about money can be tough{name_greeting}! ",
        f"Financial stress is super common in college. ",
        f"Money issues are definitely challenging{name_greeting}. ",
        f"Campus life is expensive, right? ",
        f"Being broke as a student is practically a universal experience! "
    ]
    
    academic_starters = [
        f"School pressure can feel overwhelming{name_greeting}. ",
        f"Academic stress is something most students deal with. ",
        f"College work can pile up so quickly! ",
        f"Balancing all your classes can be a lot{name_greeting}. ",
        f"Those deadlines and exams can really get to you, huh? "
    ]
    
    loneliness_starters = [
        f"Feeling disconnected is really hard{name_greeting}. ",
        f"Social stuff in college can be complicated. ",
        f"Making connections takes time. ",
        f"College can sometimes feel isolating despite being surrounded by people. ",
        f"It's totally normal to feel a bit lost socially sometimes. "
    ]
    
    stress_starters = [
        f"That sounds really overwhelming{name_greeting}. ",
        f"Stress can really build up in college. ",
        f"It's a lot to handle sometimes, isn't it? ",
        f"Taking care of your mental health is super important. ",
        f"College can really test your stress limits. "
    ]
    
    general_starters = [
        f"Hey{name_greeting}! ",
        f"I hear you. ",
        f"Thanks for sharing that{name_greeting}. ",
        f"I appreciate you opening up. ",
        f"That's really interesting. "
    ]
    
    casual_starters = [
        f"Cool{name_greeting}! ",
        f"Awesome! ",
        f"Nice to chat about this! ",
        f"That's fun to talk about. ",
        f"Great question! "
    ]
    
    # Select appropriate starter based on category
    if category == 'financial':
        starter = random.choice(financial_starters)
    elif category == 'academic':
        starter = random.choice(academic_starters)
    elif category == 'loneliness':
        starter = random.choice(loneliness_starters)
    elif category == 'stress':
        starter = random.choice(stress_starters)
    elif category in ['hobbies', 'entertainment', 'campus_life', 'food', 'future_plans', 'technology', 'weather', 'positive_chat', 'casual_chat']:
        starter = random.choice(casual_starters)
    else:
        starter = random.choice(general_starters)
    
    # Common follow-up questions to encourage conversation
    follow_ups = [
        "What's been your experience with that?",
        "How has that been affecting you?",
        "What's helped you deal with this in the past?",
        "What do you think would help most right now?",
        "How long have you been feeling this way?",
        "Is there a specific part of this that's most challenging for you?",
        "Have you talked to anyone else about this?",
        "What would make this situation better for you?",
        "Is there something specific you're looking for advice on?",
        "Would it help to talk more about this?"
    ]
    
    # Construct the response
    # For questions, try to provide some insight before asking a follow-up
    if input_text.strip().endswith('?'):
        question_insights = {
            'financial': [
                "Managing money as a student involves finding that balance between necessities and enjoyment.",
                "Student budgets are always tight, but small changes can make a big difference.",
                "Financial stress is one of the most common issues students face, so you're definitely not alone.",
                "College financial systems can be confusing, but there are often resources to help navigate them.",
                "Many students don't realize how many financial support options are actually available."
            ],
            'academic': [
                "Finding your own study rhythm is often more important than following generic advice.",
                "Academic pressure affects everyone differently, but breaks are essential for everyone.",
                "What works for one student might not work for another when it comes to studying.",
                "Balance between courses is something even the best students struggle with sometimes.",
                "Most professors understand student stress more than they let on."
            ],
            'loneliness': [
                "Meaningful connections often happen in unexpected places on campus.",
                "Quality friendships usually take time to develop, especially in new environments.",
                "Many students feel lonely even when surrounded by others on campus.",
                "Finding your community often happens through shared interests rather than forced interactions.",
                "Social media can sometimes make campus loneliness feel worse by comparison."
            ],
            'stress': [
                "Small daily self-care habits often help more than big stress-relief attempts.",
                "Stress in college often comes from multiple sources piling up at once.",
                "Your body gives physical signals about stress that are important to recognize.",
                "Taking breaks isn't lazy - it's actually essential for productivity.",
                "Different stress relief techniques work for different people."
            ]
        }
        
        if category in question_insights:
            insight = random.choice(question_insights[category])
            return f"{starter}{emoji} {insight} {random.choice(follow_ups)}"
        else:
            return f"{starter}{emoji} That's a good question. {random.choice(follow_ups)}"
    else:
        # For statements, add empathy and a follow-up
        return f"{starter}{emoji} {random.choice(follow_ups)}"

def get_response_with_context(category, user_id, conversation_pattern=None):
    """Get a response based on category and conversation context"""
    # First try to use custom fallback responses since ShuttleAI requires credits
    # If it's a common conversation pattern, handle it differently
    if conversation_pattern:
        response, response_category = get_conversational_response(conversation_pattern, user_id)
        if response:
            return response, response_category
    
    # Generate a custom fallback response
    if user_id in conversation_history and len(conversation_history[user_id]) > 0:
        last_message = conversation_history[user_id][-1].get('text', '') if conversation_history[user_id][-1].get('role') == 'user' else ''
        custom_response = generate_custom_fallback_response(last_message, category, user_id)
        if custom_response:
            return custom_response, category
    
    # Only try ShuttleAI if explicitly enabled
    if SHUTTLE_API_KEY and False:  # Disabled for now to avoid credit usage
        if user_id in conversation_history and len(conversation_history[user_id]) > 0:
            last_message = conversation_history[user_id][-1].get('text', '') if conversation_history[user_id][-1].get('role') == 'user' else ''
            
            # Try to get response from ShuttleAI
            shuttle_response = call_shuttle_api(last_message, category, user_id)
            if shuttle_response:
                return shuttle_response, category
    
    # If all else fails, fall back to the existing responses.json
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

def get_session_id():
    """Generate or retrieve a session ID for the current user"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']

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
        
        # Add bot response to history
        conversation_history[user_id].append({
            'text': response_text,
            'role': 'bot',
            'category': response_category,
            'timestamp': ''
        })
        
        # Return response with userId for session tracking
        return jsonify({
            'response': response_text,
            'category': response_category,
            'userId': user_id
        })
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'response': "I'm having trouble processing your message right now. Could you try again?",
            'category': 'general'
        }), 200  # Still return 200 to avoid client-side errors

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