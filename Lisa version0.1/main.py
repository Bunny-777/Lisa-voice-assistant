import speech_recognition as sr
import pyttsx3
import requests
import webbrowser
import musicLibrary
from playsound import playsound
import datetime

# Initialize the speech engine once
engine = pyttsx3.init()

def speak(text):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)  # Fallback to voices[0] if [1] doesn't exist
    engine.say(text)
    engine.runAndWait()

def news():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=49ee266250fb4efe9d06edec49bbae3b"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        titles = [article['title'] for article in data['articles']]
        top_three_titles = titles[:3]
        formatted_titles = "\n".join([f"{i + 1}. {title}" for i, title in enumerate(top_three_titles)])
        speak("Sure, here are the top 3 news headlines.")
        speak(formatted_titles)
    else:
        print("No news right now.")

def greet_based_on_time():
    current_time = datetime.datetime.now().time()
    if current_time < datetime.time(12, 0):
        greeting = "Good Morning Sir"
    elif datetime.time(12, 0) <= current_time < datetime.time(18, 0):
        greeting = "Good Afternoon Sir"
    else:
        greeting = "Good Evening Sir"
    
    speak(greeting)

def operation(command):
    song = command.split(" ")[1]
    link = musicLibrary.music[song]
    webbrowser.open(link)

def search(command):
    to_remove = "search "
    if command.startswith(to_remove):
        command = command[len(to_remove):]
        app = command
    else:
        app = command.split(" ")[1]
    link = "https://www.google.co.in/search?q=" + app
    playsound("D:\\project\\query.mp3")
    webbrowser.open(link)

def site(command):   
    app = command.split(" ")[1]
    links = {
        "youtube": "https://www.youtube.com/",
        "facebook": "https://www.facebook.com/",
        "spotify": "https://open.spotify.com/",
        "instagram": "https://www.instagram.com/",
        "twitter": "https://www.x.com/"
    }
    link = links.get(app, f"https://www.{app}")
    playsound("D:\\project\\query.mp3")
    webbrowser.open(link)

def mainf(r):
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=5, phrase_time_limit=4)
        word = r.recognize_google(audio).lower()
        
        if "wake up" in word:
            playsound("D:\\project\\query.mp3")
            speak("Hey there! I am Lisa, your virtual assistant. How can I help you?")
           # greet_based_on_time()
            while True:
                print("Listening...")
                try:
                    audio = r.listen(source, timeout=5, phrase_time_limit=3)
                    command = r.recognize_google(audio).lower()
                    if "exit" in command:
                        speak("Thank you")
                        playsound("D:\\project\\end.mp3")
                        exit()
                    elif "news" in command:
                        playsound("D:\\project\\query.mp3")
                        news()
                    elif "play music" in command:
                        operation(command)
                    elif "search" in command:
                        search(command)
                    elif "open" in command:
                        site(command)
                except sr.UnknownValueError:
                    print("Couldn't understand the audio. Please try again.")
                except sr.RequestError as e:
                    print(f"Error with the Google service: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")

if __name__ == "__main__":
    playsound("D:\\project\\start.mp3")
    r = sr.Recognizer()
    while True:
        mainf(r)
