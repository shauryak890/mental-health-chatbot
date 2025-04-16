# MindfulChat - Mental Health Chatbot for University Students

A responsive mental health chatbot application designed specifically for university students, featuring a Python backend with Flask and a React frontend.

## Features

- **Contextual conversations** - The chatbot tracks conversation history to provide more relevant responses
- **Category-specific support** - Specialized responses for financial stress, academic pressure, loneliness, and general stress
- **Mental health resources** - Curated resources page with helpful links and information
- **Modern, responsive UI** - Clean design that works on desktop and mobile devices
- **Accessibility features** - Skip links, keyboard navigation, and screen reader support
- **Natural, human-like responses** - Integration with ShuttleAI for more conversational and less robotic responses

## Project Structure

```
mindfulchat/
├── backend/             # Python Flask backend
│   ├── app.py           # Main Flask application with endpoints
│   ├── requirements.txt # Python dependencies
│   └── responses.json   # Fallback response templates
│
└── frontend/            # React frontend
    ├── public/          # Static files
    ├── src/             # Source files
    │   ├── components/  # React components
    │   ├── App.js       # Main App component
    │   └── App.css      # Styles
    └── package.json     # Frontend dependencies and scripts
```

## Setup Instructions

### Prerequisites

- Node.js (v14 or later)
- Python 3.7 or later
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up ShuttleAI for more natural responses (optional but recommended):
   - Sign up for a free account at [ShuttleAI](https://shuttleai.app/)
   - Create an API key from your dashboard
   - Open `app.py` and add your API key to the `SHUTTLE_API_KEY` variable

5. Run the Flask server:
   ```
   python app.py
   ```
   The backend will be available at http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the required dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```
   The application will be available at http://localhost:3000

## API Endpoints

- `POST /api/chat` - Send a message to the chatbot
  - Request body: `{ "message": "Your message here", "userId": "optional-user-id" }`
  - Response: `{ "response": "Bot response", "category": "message-category", "userId": "user-id" }`

- `GET /api/history` - Get conversation history for a user
  - Query parameters: `userId` (optional)
  - Response: `{ "history": [...messages], "userId": "user-id" }`

- `POST /api/reset` - Reset conversation history for a user
  - Request body: `{ "userId": "user-id" }`
  - Response: `{ "success": true, "userId": "user-id" }`

## Customization

### Improving Response Quality

The chatbot now uses ShuttleAI to generate more natural, human-like responses that don't sound robotic. If ShuttleAI is unavailable or you prefer not to use it, the system will fall back to the predefined responses in `responses.json`.

To modify the AI's personality or tone:
1. Open `app.py`
2. Find the `call_shuttle_api` function
3. Edit the `system_prompt` to change how the AI responds

### Adding More Response Templates

If you want to enhance the fallback responses, edit the `responses.json` file in the backend directory. You can add new categories or expand existing ones.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- FontAwesome for the icons
- Framer Motion for animations
- NLTK for natural language processing
- ShuttleAI for enhanced conversational AI capabilities 