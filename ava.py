import json
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import subprocess
import requests
from datetime import datetime, timedelta
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 140)  # Adjust speech rate

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for voice commands."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?")
        except sr.RequestError:
            speak("Sorry, there was a problem with the speech recognition service.")
        return None

def open_application(app_name):
    """Open applications based on the name."""
    apps = {
        "youtube": "https://www.youtube.com",
        "twitter": "https://twitter.com",
        "facebook": "https://www.facebook.com",
        "whatsapp": "https://web.whatsapp.com",
        "instagram": "https://www.instagram.com",
        "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe %s",
        "files": "explorer.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "cmd": "cmd.exe",
        "control panel": "control"
    }

    app_path = apps.get(app_name)
    if app_path:
        if app_path.endswith(".exe"):
            subprocess.Popen(app_path)
        else:
            webbrowser.open(app_path)
        speak(f"Opening {app_name}.")
    else:
        speak(f"Sorry, I don't know how to open {app_name}.")

def search_google(query):
    """Open web browser and search on Google."""
    if query:
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching Google for {query}.")
    else:
        speak("Sorry, I couldn't understand the search query.")

def get_weather(location="YOUR_LOCATION"):
    """Fetch current weather information and forecasts."""
    api_key = "YOUR_API_KEY"  # Replace with your actual API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            speak(f"The current weather in {location} is {weather} with a temperature of {temp}°C.")
        else:
            speak("Sorry, I couldn't fetch the weather information.")
    except requests.exceptions.RequestException:
        speak("Sorry, I am having trouble accessing the weather service right now.")

def set_alarm(time_str):
    """Set an alarm for a specific time."""
    try:
        alarm_time = datetime.strptime(time_str, '%H:%M')
        now = datetime.now()
        alarm_time = alarm_time.replace(year=now.year, month=now.month, day=now.day)
        if alarm_time < now:
            alarm_time += timedelta(days=1)
        delay = (alarm_time - now).total_seconds()
        threading.Timer(delay, lambda: speak("Alarm time!")).start()
        speak(f"Alarm set for {time_str}.")
    except ValueError:
        speak("Sorry, I couldn't understand the time format. Please use HH:MM format.")

def set_timer(duration_str):
    """Set a timer for a specific duration."""
    try:
        duration = int(duration_str.split()[0])
        unit = duration_str.split()[1]
        if unit == "minutes":
            delay = duration * 60
        elif unit == "hours":
            delay = duration * 3600
        else:
            speak("Invalid timer unit.")
            return
        threading.Timer(delay, lambda: speak("Timer finished!")).start()
        speak(f"Timer set for {duration} {unit}.")
    except (ValueError, IndexError):
        speak("Sorry, I couldn't understand the duration.")

def set_reminder(reminder_text, time_str):
    """Set a reminder for a specific time."""
    try:
        reminder_time = datetime.strptime(time_str, '%H:%M')
        now = datetime.now()
        reminder_time = reminder_time.replace(year=now.year, month=now.month, day=now.day)
        if reminder_time < now:
            reminder_time += timedelta(days=1)
        delay = (reminder_time - now).total_seconds()
        threading.Timer(delay, lambda: speak(f"Reminder: {reminder_text}")).start()
        speak(f"Reminder set for {time_str}.")
    except ValueError:
        speak("Sorry, I couldn't understand the time format. Please use HH:MM format.")

def tell_joke():
    """Tell a joke."""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why was the math book sad? It had too many problems.",
        "What do you call fake spaghetti? An impasta!"
    ]
    speak(jokes[0])

def open_youtube_play_songs():
    """Open YouTube and play Telugu songs."""
    webbrowser.open("https://www.youtube.com/results?search_query=telugu+songs")
    speak("Playing Telugu songs on YouTube.")

def handle_command(command):
    """Process and respond to the command."""
    if "tell me about" in command:
        topic = command.replace("tell me about", "").strip()
        speak(f"Here is some information about {topic}: [insert info here].")  # You can enhance this with actual APIs
    elif "open" in command:
        app_name = command.replace("open", "").strip()
        open_application(app_name)
    elif "search google for" in command:
        query = command.replace("search google for", "").strip()
        search_google(query)
    elif "what's the weather" in command:
        location = command.replace("what's the weather in", "").strip() if "in" in command else "YOUR_LOCATION"
        get_weather(location)
    elif "set an alarm for" in command:
        time_str = command.replace("set an alarm for", "").strip()
        set_alarm(time_str)
    elif "set a timer for" in command:
        duration_str = command.replace("set a timer for", "").strip()
        set_timer(duration_str)
    elif "remind me to" in command:
        parts = command.replace("remind me to", "").split(" at ")
        reminder_text = parts[0].strip()
        time_str = parts[1].strip()
        set_reminder(reminder_text, time_str)
    elif "tell me a joke" in command:
        tell_joke()
    elif "play telugu songs" in command:
        open_youtube_play_songs()
    else:
        speak("Sorry, I didn't understand the command.")

# Main loop
if __name__ == "__main__":
    while True:
        command = listen()
        if command:
            handle_command(command)
