import os
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
from db import get_training_data, get_recent_conversations

# Load environment variables
load_dotenv()

class FAQChatbot:
    def __init__(self):
        """Initialize the FAQ chatbot with Google Gemini and conversation memory."""
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Initialize Google Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=self.api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key="question",
            output_key="answer"
        )
        
        # Create the conversation chain
        self._create_chain()
    
    def _create_chain(self):
        """Create the LangChain conversation chain."""
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt()),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])
        
        # Create the chain
        self.chain = (
            RunnablePassthrough.assign(
                chat_history=lambda x: self.memory.chat_memory.messages
            )
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt with training data context."""
        base_prompt = """You are a helpful FAQ chatbot assistant. You provide accurate, concise, and helpful answers to user questions.

Key guidelines:
1. Be helpful, friendly, and professional
2. Provide clear and accurate information
3. If you're unsure about something, acknowledge it
4. Keep responses concise but comprehensive
5. Use the conversation history to provide contextual responses
"""
        
        # Add training data context if available
        training_data = get_training_data()
        if training_data:
            training_context = "\n\nHere are some example Q&A pairs for reference:\n"
            for data in training_data[:10]:  # Limit to recent 10 for context
                training_context += f"Q: {data['question']}\nA: {data['answer']}\n\n"
            base_prompt += training_context
        
        return base_prompt
    
    def ask(self, question: str, session_id: Optional[str] = None) -> str:
        """Ask a question and get an AI response."""
        try:
            # Get response from the chain
            response = self.chain.invoke({"question": question})
            
            # Save to memory
            self.memory.save_context(
                {"question": question},
                {"answer": response}
            )
            
            return response
        except Exception as e:
            return f"I apologize, but I encountered an error while processing your question: {str(e)}"
    
    def clear_memory(self):
        """Clear the conversation memory."""
        self.memory.clear()
    
    def get_memory_summary(self) -> dict:
        """Get a summary of the current conversation memory."""
        messages = self.memory.chat_memory.messages
        return {
            "total_messages": len(messages),
            "conversation_pairs": len(messages) // 2,
            "memory_buffer": self.memory.buffer
        }

# Global chatbot instance
chatbot = None

def get_chatbot() -> FAQChatbot:
    """Get or create the global chatbot instance."""
    global chatbot
    if chatbot is None:
        chatbot = FAQChatbot()
    return chatbot

def reset_chatbot():
    """Reset the global chatbot instance."""
    global chatbot
    if chatbot:
        chatbot.clear_memory()
    chatbot = None
    