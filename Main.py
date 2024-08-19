import speech_recognition as sr
import win32com.client
import webbrowser
import os
import time
import json
import requests
import spacy
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
import pygame


def speaks(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def ai(query):
            ans =f"Openai response for {query}\n*************************\n\n"
            headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTkyNTcyYzktNGRjMy00ZjU5LWFjN2UtMjFmYWMxODlmN2Q1IiwidHlwZSI6ImFwaV90b2tlbiJ9.c1lVwLrdMRliGCl7xyZxrNGWyK2ZVxtNgYP1ZhIpkR8"}

            url = "https://api.edenai.run/v2/text/code_generation"
            payload = {
                "providers": "openai",
                "prompt": "",
                "instruction": query,
                "temperature": 0.1,
                "max_tokens": 500,
            }
            response = requests.post(url, json=payload, headers=headers)

            result = json.loads(response.text)
        # print(result['openai']['generated_text'])
            ans += result['openai']['generated_text']
            if not os.path.exists("Openai"):
                os.mkdir("Openai")
            with open(f"Openai/{query[30:]}.txt","w") as f:
                f.write(ans)
chatstr=""
def chat(question):
        global chatstr
        # print(chatstr)
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOTkyNTcyYzktNGRjMy00ZjU5LWFjN2UtMjFmYWMxODlmN2Q1IiwidHlwZSI6ImFwaV90b2tlbiJ9.c1lVwLrdMRliGCl7xyZxrNGWyK2ZVxtNgYP1ZhIpkR8"}
        chatstr +=f"{name}: {question}\n Aura: "

        url = "https://api.edenai.run/v2/text/code_generation"
        payload = {
            "providers": "openai",
            "prompt": "",
            "instruction": chatstr,
            "temperature": 0.1,
            "max_tokens": 500,
        }
        response = requests.post(url, json=payload, headers=headers)

        result = json.loads(response.text)
        speaks(result['openai']['generated_text'])
        chatstr += f"{result['openai']['generated_text']}\n"
        return result['openai']['generated_text']

def weather(city):
        api_URL=f"https://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&appid=7966d8afb532b511573f1f59b4fc3137"
        response=requests.get(api_URL)
        result=json.loads(response.text)
        return(result['main']['temp'])
def news(data):
    apikey=f"https://newsdata.io/api/1/news?apikey=pub_4769371bafa864a49e5f8db5f5783a4bc3a66&q={data}&language=en"
    r=requests.get(apikey)
    result=json.loads(r.text)
    return result['results'][0]['title']
     
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Please say something:")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            return query
        except sr.RequestError:
            # API was unreachable or unresponsive
            speaks("Sorry, I couldn't reach the recognition service.")
            
        except sr.UnknownValueError:
            # Speech was unintelligible
            speaks("Sorry, I could not understand the audio.")

def sep(text):
    nltk.download('punkt')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    nltk.download('averaged_perceptron_tagger')
    sentence = text                                      #Returns the city name using NLP
    words = word_tokenize(sentence)
    pos_tags = pos_tag(words)
    named_entities = ne_chunk(pos_tags)
    for subtree in named_entities:
        if hasattr(subtree, 'label') and subtree.label() == 'GPE':
            entity = ' '.join([leaf[0] for leaf in subtree.leaves()])
            # print(f"Geopolitical entity found: {entity}")
            return entity
    return None

def keyword(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    if keywords:                                                                    #Returns any noun or pronoun name using NLP
        return keywords[0]  # Return the first keyword found
    return None
pygame.mixer.init()

def play_music(file_path):
    
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

def wish():
    curr_time = time.strftime("%H:%M:%S")
    # print(curr_time)
    curr_time = int(time.strftime("%H"))
    # print(curr_time)
    if(4<=curr_time<12):
        return("Good Morning")
    if(12<=curr_time<17):
        return("Good Afternoon")
    if(17<=curr_time<20 or 20<=curr_time<24 or 0<=curr_time<4):
        return("Good Evening")
    else:
        print("none")
            

if __name__ == "__main__":
    name=input("Enter your name -> ")
    greet=wish()
    speaks(f"Hey {name} , {greet} i am your personal assistant , How can i help you ")
    while True:
        print("Listening...")
        text = takecommand()
        print("Recognizing...")
        print(f"user said: {text}")
        sites=[["youtube","https://www.youtube.com"], ["wikipedia" , "https://www.wikipedia.com"] ,["Google" , "https://www.google.com"] , ["Linkedin" ,"https://www.linkedin.com"] ,["Instagram" , "https://www.instagram.com"] ]
        for site in sites:
            if f"open {site[0]}".lower() in text.lower():
                speaks(f"Opening {site[0]} sir .....")
                webbrowser.open(site[1])
        if "play".lower() in text.lower():
            music=text[5:]
            print(music)
            musicPath = f"D:\\{music}.mp3"
            if os.path.exists(musicPath):
                play_music(musicPath)
                speaks("Playing music...")
                time.sleep(150)
            else:
                speaks("Sorry, I couldn't find the music file.")
        elif "the time".lower() in text.lower():
            curr_time = time.strftime("%H:%M:%S")
            speaks(f" the time is {curr_time}") 

        elif "open my pictures".lower() in text.lower():
            path="C:\\Users\\hp\\OneDrive\\Pictures\\Saved Pictures"
            os.startfile(path)

        elif "using Artificial intelligence".lower() in text.lower():
            ai(query=text)
        elif "weather".lower() in text.lower():
            city=sep(text)
            report=weather(city)
            speaks(f"the Weather of{city} is {report} degree celsius") 
        elif "news".lower() in text.lower():
            key=keyword(text)
            data=news(key)
            print(data)
            speaks(data) 
        
        elif "quit".lower() in text.lower():
             speaks(f"Good Bye {name} , Have a nice Day")
             exit()
        elif "reset chat".lower() in text.lower():
             chatstr=""
        else:
            chat(text)
