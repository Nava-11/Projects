import os
import pytesseract
import pyttsx3
from PIL import Image
import mss
import keyboard
import tkinter as tk
from groq import Groq
from dotenv import load_dotenv

# ---------------------------
# Setup
# ---------------------------

# Load environment variables from .env
load_dotenv()

# Configure Tesseract (⚠️ adjust path if different)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("❌ Missing GROQ_API_KEY in .env file")
client = Groq(api_key=GROQ_API_KEY)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 175)  # speed
engine.setProperty("volume", 1.0)  # max volume


def speak(text: str):
    """Read out text via system voice"""
    engine.say(text)
    engine.runAndWait()


def capture_screen():
    """Capture the primary screen and return extracted text via OCR"""
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Monitor[1] = primary screen
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        text = pytesseract.image_to_string(img, lang="eng")
    return text.strip()


def analyze_with_groq(text: str) -> str:
    """Send extracted text to Groq LLM for context-aware analysis"""
    if not text:
        return "⚠️ No text detected on screen."

    prompt = f"""
    You are ScreenSense AI.
    Analyze the following screen content:

    {text}

    Your tasks:
    - If it's CODE → explain what it does and suggest improvements.
    - If it's an ERROR → explain the cause and suggest fixes.
    - If it's an ARTICLE/WEB CONTENT → summarize in 3 bullet points.
    - If it's something else → provide a short useful description.
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",  # Groq’s fast & lightweight model
            temperature=0.3,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ Error calling Groq API: {e}"


def show_output(text: str):
    """Popup window with extracted AI analysis"""
    root = tk.Tk()
    root.title("ScreenSense AI")
    root.geometry("600x400")

    output_box = tk.Text(root, wrap="word", font=("Consolas", 11))
    output_box.insert("1.0", text)
    output_box.pack(expand=True, fill="both")

    scrollbar = tk.Scrollbar(output_box)
    scrollbar.pack(side="right", fill="y")
    output_box.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=output_box.yview)

    root.mainloop()


def run_screensense():
    """Capture → OCR → Analyze → Show popup → Speak"""
    print("📸 Capturing screen...")
    screen_text = capture_screen()
    print("\n📝 Extracted Screen Text:\n", screen_text or "⚠️ [Empty OCR Output]")

    print("\n🤖 Analyzing with Groq...\n")
    analysis = analyze_with_groq(screen_text)
    print(analysis)

    # Show popup window
    show_output(analysis)

    # Speak output
    speak(analysis)


# ---------------------------
# Main Program
# ---------------------------
if __name__ == "__main__":
    print("✅ ScreenSense AI is running...")
    print("👉 Press Ctrl+Shift+A anytime to capture & analyze screen")
    print("👉 Press ESC to quit")

    keyboard.add_hotkey("ctrl+shift+a", run_screensense)
    keyboard.wait("esc")
