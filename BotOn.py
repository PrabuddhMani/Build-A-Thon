import pyttsx3
import datetime
import speech_recognition as sr
import pyaudio
import wikipedia
import webbrowser
import os
import smtplib
import time
from ecapture import ecapture as ec
import requests
import openai
from config import apikey
import random
# from googlesearch import google
from googlesearch import search

chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Harry: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    os.system(f'say "{text}"')


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning!")
        print("Good Morning!")
    elif hour>=12 and hour<=18:
        speak("Good Afternoon!")
        print("Good Afternoon!")
    else:
        speak("Good Evening!")
        print("Good Evening!")
    speak("Hii sir, please tell How may i help you?")
    print("Hii sir, please tell How may i help you?")

def takeCommand():
    # it takes microphone input from the user and return string output.
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        # r.energy_threshold = 50
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language='en_in')
        print(f"User Said: {query}\n")
    except Exception as e:
        # print(e)

        print("Say that again please...")
        return "None"
    return query

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('realprabuddh@gmail.com','Devil@Dart')
    server.sendmail('realprabuddh@gmail.com',to,content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
    
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('searching wikipedia...')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query,sentences=20)
            speak("According to wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open w3school' in query:
            webbrowser.open("w3school.com")
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
        elif 'play skd 1' in query:
            webbrowser.open("https://www.youtube.com/watch?v=VRArcJZ8zoY&list=RDVRArcJZ8zoY&start_radio=1&rv=VRArcJZ8zoY&t=8")
        elif 'play emraan hashmi mashup' in query:
            webbrowser.open("https://www.youtube.com/watch?v=ko1IN44GLCY&list=RDko1IN44GLCY&start_radio=1&rv=ko1IN44GLCY&t=3")
        elif 'play skd 2' in query:
            webbrowser.open("https://www.youtube.com/watch?v=KZRlmT9uJuI&list=RDKZRlmT9uJuI&start_radio=1&rv=KZRlmT9uJuI&t=2")
        elif 'play music' in query:
            webbrowser.open("https://www.youtube.com/watch?v=lje_S_fpFBE&list=PLV4mMeZbr6jh_clb1wvbjRBA3-ljkZGh_")
        elif 'open harry python playlist' in query:
            webbrowser.open("https://www.youtube.com/playlist?list=PLu0W_9lII9agICnT8t4iYVSZ3eykIAOME")
        elif 'the time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strtime}")
        elif 'open code' in query:
            codePath = "C:\\Users\\prabu\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
        elif 'email to harry' in query:
            try:
                speak("What should i say?")
                content = takeCommand()
                to = "realprabuddh@gmail.com"
                sendEmail(to,content)
                speak("Email has been send!")
            except Exception as e:
                print(e)
                speak("Sorry my friend harry bhai. I am not able to send this email") 
        elif 'open data structure playlist' in query:
            webbrowser.open("https://www.youtube.com/playlist?list=PLxCzCOWd7aiEwaANNt3OqJPVIxwp2ebiT")
        elif 'open web development playlist' in query:
            webbrowser.open("https://www.youtube.com/playlist?list=PLu0W_9lII9agiCUZYRsvtGTXdxkzPyItg")
        elif 'news' in query:
            new = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India, Happy reading')
            time.sleep(6)
        elif "camera" in query or 'take a photo' in query:
            l = len(os.listdir("myClicks"))
            ec.capture(0, "robo camera", f'myClicks\\img{l}.jpg')
        elif 'search' in query:
            query = query.replace("search", "")
            webbrowser.open_new_tab(query)
            time.sleep(5)

        elif "weather" in query:
            response = requests.get('https://api.open-meteo.com/v1/forecast?latitude=31.2560&longitude=75.7051&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m#')

            p = response.json()
            cur_weather = p['current_weather']
            temp =  cur_weather['temperature']
            windspeed = cur_weather['windspeed']
            winddirection = cur_weather['winddirection']
            weathercode = cur_weather['weathercode']
            is_day = cur_weather['is_day']
            cur_time = cur_weather["time"]
            cur_index = p['hourly']['time'].index(cur_time)

            speak(f"Temperature in Celcius unit is {str(temp)} \n  humidity in percentage is {str(p['hourly']['relativehumidity_2m'][cur_index])}\n and the windspeed is {str(cur_weather['windspeed'])}" )
            

        
        
        elif 'quit' in query or 'exit' in  query:
            print('Quiting Sir....')
            speak('Quiting Sir....')
            exit()



    # logic for executing task is based on query.
