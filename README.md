# MindfulChat - Mental Health Chatbot for University Students

A responsive mental health chatbot application designed specifically for university students, featuring a Python backend with Flask and a React frontend.

## Features

- **Contextual conversations** - The chatbot tracks conversation history to provide more relevant responses
- **Category-specific support** - Specialized responses for financial stress, academic pressure, loneliness, and general stress
- **Mental health resources** - Curated resources page with helpful links and information
- **Modern, responsive UI** - Clean design that works on desktop and mobile devices
- **Accessibility features** - Skip links, keyboard navigation, and screen reader support

## Project Structure

```
mindfulchat/
├── backend/             # Python Flask backend
│   ├── app.py           # Main Flask application with endpoints
│   ├── requirements.txt # Python dependencies
│   └── responses.json   # Response templates for different categories
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

4. Run the Flask server:
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

### Adding More Response Templates

To add more responses, edit the `responses.json` file in the backend directory. You can add new categories or expand existing ones.

### External API Integration

For more advanced chatbot capabilities, you can add your HuggingFace API key in the `app.py` file:

```python
HUGGINGFACE_API_KEY = "your-api-key-here"
```

## License

This project is open source and available under the MIT License.

## Acknowledgments

- FontAwesome for the icons
- Framer Motion for animations
- NLTK for natural language processing 