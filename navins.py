import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import requests
import json
import time
import pywhatkit
import wolframalpha
# from deep_translator import GoogleTranslator

# translator = GoogleTranslator(source='en', target='fr')
# translated_text = translator.translate("Hello, world!")
# print(translated_text)



# Initialize Text-to-Speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Greet the user
def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Hi, I am Navins. How can I help you today?")
def get_answer(query):
    api_key = "W29XAE-Q7L39ULAY5"  # Replace with your Wolfram Alpha API key
    client = wolframalpha.Client(api_key)
    try:
        res = client.query(query)
        answer = next(res.results).text
        speak(answer)
    except Exception as e:
        speak("I couldn't find an answer to that. Please try asking something else.")
def tell_time():
    from datetime import datetime
    now = datetime.now()
    time = now.strftime("%H:%M")
    speak(f"The current time is {time}.")

# Function to search something on Google
def search_google(query):
    search_query = query.replace("search", "").strip()
    speak(f"Searching for {search_query} on Google.")
    webbrowser.open(f"https://www.google.com/search?q={search_query}")
def search_google(query):
    search_query = query.replace("search", "").strip()
    speak(f"Searching for {search_query} on Google.")
    webbrowser.open(f"https://www.google.com/search?q={search_query}")
# Listen to user commands
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again, please...")
        return "None"
    return query.lower()

# Send Email
def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')  # Replace with your email and password
        server.sendmail('your_email@gmail.com', to, content)
        server.close()
        speak("Email has been sent.")
    except Exception as e:
        speak("Sorry, I couldn't send the email.")

# Weather Updates
def get_weather(city):
    api_key = "423490b55962d89d457c35e3e301fd67"  # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    weather_data = response.json()
    if weather_data["cod"] != "404":
        main = weather_data["main"]
        weather_desc = weather_data["weather"][0]["description"]
        temp = main["temp"]
        speak(f"The current temperature in {city} is {temp} degrees Celsius with {weather_desc}.")
    else:
        speak("City not found. Please try again.")

# Notes
def take_note():
    speak("What would you like me to write down?")
    note = takecommand()
    with open("notes.txt", "a") as file:
        file.write(f"{datetime.datetime.now()} - {note}\n")
    speak("I've saved the note.")

# Alarms
def set_alarm(alarm_time):
    speak(f"Alarm set for {alarm_time}.")
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if current_time == alarm_time:
            speak("Wake up! It's time!")
            break
        time.sleep(1)

# Jokes
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

# Translation
# def translate_text(text, target_language='es'):  # Default to Spanish
#     translator = Translator()
#     translated = translator.translate(text, dest=target_language)
#     speak(f"Translation: {translated.text}")

# Preferences
def save_preferences(preferences):
    with open("preferences.json", "w") as file:
        json.dump(preferences, file)

def load_preferences():
    try:
        with open("preferences.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Main program
if __name__ == "__main__":
    preferences = load_preferences()
    if 'name' not in preferences:
        speak("What should I call you?")
        name = takecommand()
        preferences['name'] = name
        save_preferences(preferences)
        speak(f"Nice to meet you, {name}!")
    else:
        speak(f"Welcome back, {preferences['name']}!")

    wishme()

    while True:
        query = takecommand()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia:")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'play music' in query:
            music_dir = r'C:\Users\YourUsername\Music'  # Replace with your music directory
            songs = [song for song in os.listdir(music_dir) if song.endswith(('.mp3', '.wav'))]
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("No songs found in the specified directory.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'open code' in query:
            codePath = r"C:\Users\YourUsername\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk"  # Replace with your VS Code path
            os.startfile(codePath)

        elif 'email to' in query:
            try:
                speak("What should I say?")
                content = takecommand()
                to = "recipient_email@gmail.com"  # Replace with recipient's email
                sendEmail(to, content)
            except Exception as e:
                speak("Sorry, I couldn't send the email.")

        elif 'weather' in query:
            speak("Which city?")
            city = takecommand()
            get_weather(city)

        elif 'add note' in query:
            take_note()

        elif 'set alarm' in query:
            speak("What time should I set the alarm for? (e.g., 07:30:00)")
            alarm_time = takecommand()
            set_alarm(alarm_time)

        elif 'translate' in query:
            speak("What would you like me to translate?")
            text_to_translate = takecommand()
            translate_text(text_to_translate)

        elif 'exit' in query or 'bye' in query:
            speak("Goodbye! Have a nice day.")
            break
        elif "search" in query:
            search_google(query)

