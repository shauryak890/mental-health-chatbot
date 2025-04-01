from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

# Load responses from JSON file
with open('responses.json', 'r') as f:
    responses = json.load(f)

def analyze_message(message):
    message = message.lower()
    
    # Categories and their keywords
    categories = {
        'financial': ['money', 'financial', 'expensive', 'afford', 'cost', 'debt', 'loan'],
        'loneliness': ['alone', 'lonely', 'isolated', 'no friends', 'left out'],
        'academic': ['grades', 'exam', 'study', 'assignment', 'academic', 'course', 'homework'],
        'stress': ['stress', 'pressure', 'overwhelmed', 'anxiety', 'worried'],
        'general': ['help', 'sad', 'depressed', 'confused']
    }
    
    # Find matching category
    for category, keywords in categories.items():
        if any(keyword in message for keyword in keywords):
            return category
    
    return 'general'

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    category = analyze_message(user_message)
    response = random.choice(responses[category])
    
    return jsonify({
        'response': response,
        'category': category
    })

if __name__ == '__main__':
    app.run(debug=True) 