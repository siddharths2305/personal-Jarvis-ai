import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import pyttsx3
import random
import subprocess
import re
import cv2  # Import OpenCV for camera functionality

chatStr = ""
engine = pyttsx3.init()


def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"User: {query}\nJarvis: "

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_text = response.choices[0].text.strip()
        chatStr += f"Jarvis: {response_text}\n"
        say(response_text)
        return response_text
    except Exception as e:
        error_message = "Sorry, I couldn't process your request."
        say(error_message)
        print(f"Error: {e}")
        return error_message


def generate_and_save_content(prompt):
    openai.api_key = apikey
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_text = response.choices[0].text.strip()
        filename = "Generated_Content.txt"

        # Create directory if it doesn't exist
        if not os.path.exists("Generated"):
            os.mkdir("Generated")

        file_path = os.path.join("Generated", filename)
        with open(file_path, "w") as f:
            f.write(response_text)

        say(f"Content has been saved to {filename}.")
        print(f"Content written to {file_path}")
    except Exception as e:
        error_message = "Sorry, I couldn't process your request."
        say(error_message)
        print(f"Error: {e}")


def say(text):
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"


def takeTerminalInput():
    query = input("Type your query: ")
    return query


def play_media(media_type):
    folder_path = f"/Users/harry/{media_type.capitalize()}"

    if not os.path.exists(folder_path):
        say(f"Sorry, the {media_type} folder does not exist.")
        return

    media_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp3', '.mp4', '.avi', '.mkv'))]

    if not media_files:
        say(f"No {media_type} files found in the {media_type} folder.")
        return

    media_file = random.choice(media_files)
    media_path = os.path.join(folder_path, media_file)
    os.system(f"open {media_path}")
    say(f"Playing {media_type}: {media_file}")


def search_youtube(query):
    query = query.replace("search youtube for ", "")
    youtube_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    say(f"Searching YouTube for {query}")
    webbrowser.open(youtube_url)


def play_favorite_song():
    favorite_song_url = "https://www.youtube.com/watch?v=hHuG7FIKgtc&list=RDMMhHuG7FIKgtc&start_radio=1"
    say("Playing your favorite song.")
    webbrowser.open(favorite_song_url)


def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I told my wife she was drawing her eyebrows too high. She seemed surprised."
    ]
    joke = random.choice(jokes)
    say(joke)
    print(joke)


def open_app(app_name):
    app_paths = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    }
    if app_name in app_paths:
        try:
            subprocess.Popen(app_paths[app_name])
            say(f"Opening {app_name}")
        except Exception as e:
            say(f"Failed to open {app_name}")
            print(f"Error: {e}")
    else:
        say(f"Application {app_name} is not recognized.")


def open_website(query):
    # Extract website name from the command
    match = re.search(r'open (\w+)', query.lower())
    if match:
        site_name = match.group(1)
        url = f"https://{site_name}.com"

        # Try opening the website
        try:
            say(f"Opening {site_name} sir...")
            webbrowser.open(url)
        except Exception as e:
            say(f"Sorry, I couldn't open {site_name}.")
            print(f"Error: {e}")
    else:
        say("Please specify a valid website name to open.")


def open_camera():
    say("Opening the camera.")
    cap = cv2.VideoCapture(0)  # 0 is usually the default camera index

    if not cap.isOpened():
        say("Sorry, I couldn't access the camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            say("Failed to grab frame.")
            break
        cv2.imshow('Camera', frame)

        # Exit the camera on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    say("Camera closed.")


if __name__ == '__main__':
    print('Welcome to Jarvis AI')
    say("Welcome Sir")

    while True:
        print("Listening...")
        mode = input("Do you want to use voice input or terminal input? (type 'voice' or 'terminal'): ").strip().lower()

        if mode == "voice":
            query = takeCommand()
        elif mode == "terminal":
            query = takeTerminalInput()
        else:
            say("Invalid input mode. Please choose 'voice' or 'terminal'.")
            continue

        # Handle website opening
        if "open" in query.lower() and ".com" not in query.lower():
            open_website(query)

        # Handle camera opening with specific command
        elif "from pc open camera" in query.lower():
            open_camera()

        # Handle other commands
        elif "search youtube for" in query.lower():
            search_youtube(query)

        elif "play my favorite song" in query.lower():
            play_favorite_song()

        elif "open music" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            os.system(f"open {musicPath}")

        elif "play song" in query.lower():
            play_media("music")

        elif "play video" in query.lower():
            play_media("video")

        elif "tell me a joke" in query.lower():
            tell_joke()

        elif "open" in query.lower() and any(app in query.lower() for app in ["notepad", "calculator", "paint", "chrome"]):
            app_name = query.split("open ")[1].strip()
            open_app(app_name)

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {min} minutes")

        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "open pass".lower() in query.lower():
            os.system(f"open /Applications/Passky.app")

        elif "write a mail" in query.lower():
            prompt = "Write a formal email. The subject is 'Holiday Leave Request'. Include a subject line, greeting, body, and closing."
            generate_and_save_content(prompt)

        elif "jarvis quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
