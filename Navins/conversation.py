# conversation.py
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env variables
load_dotenv()

# Get the API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in .env")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)


def chat_with_jarvis(user_input, conversation_history=[]):
    """
    Handles natural conversation with memory.
    conversation_history: keeps track of context.
    """
    conversation_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # lightweight but smart enough
        messages=conversation_history
    )

    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})
    return reply, conversation_history
