import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import threading
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os

# Initialize backend components
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# === Backend Logic ===
def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        update_text("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            update_text(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            update_text("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            update_text("Could not request results.")
            return ""

def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Here are the search results for {query}")

def youtube_search(query):
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    speak(f"Here are the YouTube results for {query}")

def get_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    speak(f"The current time is {current_time}")
    update_text(f"Time: {current_time}")
def open_app(command):
    if 'notepad' in command:
        os.system("notepad.exe")
    elif 'calculator' in command:
        os.system("calc.exe")
    else:
        speak("App not configured yet.")
def system_control(command):
    if 'shutdown' in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")
    elif 'restart' in command:
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")
    elif 'lock' in command:
        speak("Locking the system.")
        os.system("rundll32.exe user32.dll,LockWorkStation")
    


# === GUI Logic ===
def update_text(message):
    output_label.config(text=message)

def start_assistant():
    speak("Hello, I am J.A.R.V.I.S. How can I assist you today?")
    while True:
        command = listen()
        if 'google' in command:
            query = command.replace('google', '')
            google_search(query)
        elif 'youtube' in command:
            query = command.replace('youtube', '')
            youtube_search(query)
        elif 'time' in command:
            get_time()
        elif 'open' in command:
            open_app(command)
        elif 'shutdown' in command or 'restart' in command or 'lock' in command:
            system_control(command)
        elif 'exit' in command:
            speak("Goodbye!")
            break
        else:
            speak("I can help you with Google search, YouTube search, or tell you the time.")

def threaded_assistant():
    thread = threading.Thread(target=start_assistant)
    thread.daemon = True
    thread.start()


# === GUI Setup ===
app = tk.Tk()
app.title("J.A.R.V.I.S - AI Desktop Assistant")
app.geometry("800x600")
app.config(bg="#0f0f0f")

# Background Image
bg_img = Image.open("a-0025.JPG")  # Replace with your GIF/image path
bg_img = bg_img.resize((800, 600), Image.ANTIALIAS)
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(app, image=bg_photo)
bg_label.place(x=0, y=0)

# Output Display
output_label = tk.Label(app, text="Welcome, J.A.R.V.I.S online.", font=("Helvetica", 16), bg="#000000", fg="white")
output_label.pack(pady=20)

# Control Buttons
start_btn = tk.Button(app, text="Start Listening", font=("Arial", 14), command=threaded_assistant, bg="green", fg="white")
start_btn.pack(pady=10)

exit_btn = tk.Button(app, text="Exit", font=("Arial", 14), command=app.quit, bg="red", fg="white")
exit_btn.pack(pady=10)

app.mainloop()
