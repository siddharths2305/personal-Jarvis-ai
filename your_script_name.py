import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import pyttsx3
import random

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

        # Open websites based on query
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"]]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        # Handle other commands
        if "search youtube for" in query.lower():
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
