import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice',voices[0].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wishme():
    hour=int(datetime.datetime.now().hour)
    if(hour>=0 and hour<12):
        speak("Good Morning !!")
    elif(hour>=12 and hour<18):
        speak("Good Afternoon!!")
    else:
        speak("Good Evening!!")
    speak("Hi I am Navins.. How may I help you..")
def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        audio=r.listen(source)
    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-in')
        print(f"User said:  {query}\n")
    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query
def sendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com','password')
    server.sendmail('youremail@gmail.com',to,content)
    server.close()
if __name__=="__main__":
    wishme()
    while True:
        query=takecommand().lower()
        #logic for executing tasks
        if 'wikipedia' in query:
            speak("Searching in Wikipedia ..")
            query=query.replace("wikipedia","")
            results=wikipedia.summary(query,sentences=2)
            speak("According to wikipedia..")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'play music' in query:
            try:
                music_dir = r'C:\Users\navan\Music'
                songs = [song for song in os.listdir(music_dir) if song.endswith(('.mp3', '.wav'))]
                if songs:
                    os.startfile(os.path.join(music_dir, songs[0]))
                else:
                    print("No songs found in the specified directory.")
            except Exception as e:
                print(f"An error occurred: {e}")
        elif 'the time' in query:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f" the time is {strTime}")
        elif 'open code' in query:
            codePath="C:\\Users\\navan\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Visual Studio Code.lnk"
            os.startfile(codePath)
        elif 'email to navaneeth' in query:
            try:
                speak('what shoul I say')
                content=takecommand()
                to="navaneethh49@gmail.com"
                sendEmail(to,content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("Sorry, Email has not been sent")
        elif 'exit' in query or 'bye' in query:
            speak("Goodbye! Have a nice day.")
            break




