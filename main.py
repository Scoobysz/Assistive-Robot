import speech_recognition as sr
import os
import webbrowser
import datetime
import openai
from config import apikey
import pyttsx3


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for prompt: {prompt} \n*******************\n\n"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=100,
        n=1,
        stop=None,
    )

    generated_text = response.choices[0].text.strip()
    print(generated_text)
    text += generated_text

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('AI')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def chat(query, chatStr):
    openai.api_key = apikey
    chatStr += f"Abhay: {query}\n Scooby:"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=100,
        n=1,
        stop=None,
    )

    generated_text = response.choices[0].text.strip()
    say(generated_text)

    chatStr += f"{generated_text}\n"

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(query.split('AI')[1:]).strip()}.txt", "w") as f:
        f.write(chatStr)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing.......")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some error occurred. Sorry."


def openYouTubeVideo(title):
    search_query = title + " YouTube"
    url = f"https://www.youtube.com/results?search_query={search_query}"
    webbrowser.open(url)


def searchInternet(query):
    search_query = query.replace("search the internet for", "").strip()
    if search_query:
        say(f"Searching the internet for {search_query}...")
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
    else:
        say("Sorry, I couldn't recognize the search query.")


say("Hello, I am your personal AI assistant Scooby")
chatStr = ""

while True:
    print("Listening......")
    query = takeCommand()
    say(query)
    sites = [
        #["YouTube", "https://www.youtube.com"],
        ["Wikipedia", "https://www.wikipedia.com"],
        ["Google", "https://www.google.com"],
        ["Instagram", "https://www.instagram.com"],
        ["Twitter", "https://www.twitter.com"],
        ["Gmail", "https://mail.google.com/mail/u/0/#inbox"],
    ]

    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            say(f"Opening {site[0]}....")
            webbrowser.open(site[1])

    if "The time" in query:
        strfTime = datetime.datetime.now().strftime("%H:%M:%S")
        say(f"The time is {strfTime}")

    if "Using AI".lower() in query.lower():
        ai(prompt=query)
    elif "open YouTube" in query:
        # Check if the query contains a video title
        if len(query.split("open YouTube ")) > 1:
            video_title = query.split("open YouTube ")[1]
            openYouTubeVideo(video_title)
        else:
            say("Sure, opening YouTube...")
            webbrowser.open("https://www.youtube.com")
    elif "search internet for" in query.lower():
        searchInternet(query.lower())
    else:
        chat(query, chatStr)
