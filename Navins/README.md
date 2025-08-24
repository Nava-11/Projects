# Navins – AI Voice Assistant

Navins is a Jarvis-like AI voice assistant that can interact with users conversationally, perform tasks, fetch information, and control your computer. It combines voice recognition, text-to-speech, AI-powered conversation, and screen scanning for a seamless experience.



## Features

1. **Voice Interaction**

   * Listens to your commands and responds using natural speech.
   * Supports casual conversation (chatting, jokes, greetings, etc.).

2. **AI Conversational Brain**

   * Uses OpenAI API (`gpt-4o-mini`) to hold contextual conversations.
   * Remembers the conversation history for more natural interactions.

3. **Screen & HUD Scanning**

   * Can scan your screen (OCR functionality) and provide contextual insights.

4. **Utility Functions**

   * Wikipedia search
   * Google search
   * Weather updates
   * Alarms and reminders
   * Notes management
   * Play YouTube videos or music
   * Send emails
   * WolframAlpha queries
   * Tell jokes

5. **Customizable Preferences**

   * Remembers your name and other user preferences for personalized interactions.



## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/YourUsername/Navins.git
cd Navins
```

2. **Create a virtual environment (optional but recommended):**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** in the root directory with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```



## Usage

Run the main assistant:

```bash
python screen/navins.py
```

### How it works:

* The assistant greets you based on the time of day.
* Listen for commands like:

  * `"open youtube"`
  * `"the time"`
  * `"wikipedia <query>"`
  * `"play video <name>"`
  * `"set alarm <HH:MM:SS>"`
  * `"gpt"` or `"ask gpt"` → engages AI conversational brain
* For casual conversation, just speak normally. Navins responds naturally.

**To exit:** Say `"exit"` or `"bye"`.


## File Structure

```
Navins/
│
├─ screen/
│   ├─ navins.py         # Main assistant script
│   └─ conversation.py   # AI chat functionality
│
├─ index.py              # Screen scanning functions
├─ requirements.txt      # Python dependencies
├─ .env                  # Environment variables (API keys)
└─ README.md
```



## Dependencies

* Python 3.10+
* pyttsx3 – Text-to-speech
* speech\_recognition – Speech-to-text
* wikipedia – Wikipedia search
* webbrowser – Open URLs
* smtplib – Email sending
* requests – HTTP requests
* pywhatkit – YouTube & Google searches
* wolframalpha – Query computations
* pyjokes – Telling jokes
* openai – AI conversational brain
* python-dotenv – Load environment variables



## Notes

* Make sure your microphone works and you have an active internet connection.
* Replace placeholder paths for music, VS Code, and email credentials as needed.
* Set your own API keys for OpenAI and WolframAlpha in `.env`.



Do you want me to do that?
