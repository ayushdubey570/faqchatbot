Smart FAQ Chatbot API
A complete REST API backend using FastAPI, LangChain, and Google Gemini that acts as a smart FAQ chatbot system with conversation memory and training capabilities.

🚀 Features
FastAPI Backend: Modern, fast web framework for building APIs
Google Gemini Integration: Powered by Google's Gemini Pro model via LangChain
Conversation Memory: Maintains context across conversations using ConversationBufferMemory
SQLite Database: Stores conversation logs and training data
Training System: Add custom Q&A pairs to improve chatbot responses
Session Management: Optional session-based conversations
Comprehensive Logging: All interactions are logged for analysis
📋 Requirements
Python 3.8+
Google API Key (for Gemini Pro)
All dependencies listed in requirements.txt
🛠️ Installation & Setup
1. Clone and Setup Environment
bash
# Create project directory
mkdir faq-chatbot-api
cd faq-chatbot-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
2. Install Dependencies
bash
pip install -r requirements.txt
3. Configure Environment Variables
Get your Google API Key:
Go to Google AI Studio
Create a new API key
Copy the API key
Update the .env file:
bash
GOOGLE_API_KEY=your_actual_google_api_key_here
4. Run the Application
bash
# Using uvicorn directly
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# Or run the main.py file
python main.py
The API will be available at: http://127.0.0.1:8000 or http://localhost:8000

📚 API Endpoints
1. Health Check
GET /
Description: Check if the API is running
Response: Health status and timestamp
2. Ask Question
POST /ask
Description: Submit a question and get an AI-generated answer
Request Body:
json
{
  "question": "What is artificial intelligence?",
  "session_id": "optional-session-id"
}
Response:
json
{
  "answer": "AI response here...",
  "question": "What is artificial intelligence?",
  "timestamp": "2025-06-09T10:30:00",
  "session_id": "optional-session-id"
}
3. Get Conversation Logs
GET /logs
Description: Retrieve all conversation logs
Response: Array of conversation logs with timestamps
4. Add Training Data
POST /train
Description: Add custom Q&A pairs for training
Request Body:
json
{
  "question": "What are your business hours?",
  "answer": "We are open Monday to Friday, 9 AM to 6 PM."
}
Response:
json
{
  "id": 1,
  "message": "Training data added successfully",
  "question": "What are your business hours?",
  "answer": "We are open Monday to Friday, 9 AM to 6 PM."
}
5. Additional Endpoints
GET /training - Get all training data
POST /reset - Reset conversation memory
GET /status - Get chatbot status and memory info
🧪 Testing the API
Using curl:
bash
# Health check
curl http://localhost:8000/

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?"}'

# Add training data
curl -X POST http://localhost:8000/train \
  -H "Content-Type: application/json" \
  -d '{"question": "What is your return policy?", "answer": "We offer 30-day returns on all items."}'

# Get logs
curl http://localhost:8000/logs
Using Python requests:
python
import requests

# Ask a question
response = requests.post("http://localhost:8000/ask", 
    json={"question": "Tell me about Python programming"})
print(response.json())

# Add training data
response = requests.post("http://localhost:8000/train",
    json={
        "question": "What payment methods do you accept?",
        "answer": "We accept credit cards, PayPal, and bank transfers."
    })
print(response.json())
📖 API Documentation
Once the server is running, you can access:

Interactive API Docs: http://localhost:8000/docs (Swagger UI)
Alternative API Docs: http://localhost:8000/redoc (ReDoc)
🗃️ Database Schema
The SQLite database (logs.db) contains two tables:

conversation_logs
id: Primary key
question: User question
answer: AI response
timestamp: When the conversation occurred
session_id: Optional session identifier
training_data
id: Primary key
question: Training question
answer: Expected answer
created_at: When the training data was added
🔧 Configuration
The system uses environment variables for configuration:

GOOGLE_API_KEY: Your Google API key for Gemini Pro
🚨 Error Handling
The API includes comprehensive error handling:

Input validation for all endpoints
Proper HTTP status codes
Detailed error messages
Database connection error handling
LLM API error handling
🔍 Troubleshooting
Common Issues:
"GOOGLE_API_KEY not found"
Make sure your .env file is in the project root
Verify the API key is correctly set
"Module not found" errors
Ensure all dependencies are installed: pip install -r requirements.txt
Check that your virtual environment is activated
Database errors
The SQLite database is created automatically
Check file permissions in the project directory
Port already in use
Change the port in main.py or kill existing processes on port 8000
📈 Scaling Considerations
For production use, consider:

Using PostgreSQL instead of SQLite
Implementing proper authentication and authorization
Adding rate limiting
Using Redis for session management
Implementing proper logging and monitoring
Adding input sanitization and validation
🤝 Contributing
Feel free to submit issues, feature requests, or pull requests to improve this FAQ chatbot system!

