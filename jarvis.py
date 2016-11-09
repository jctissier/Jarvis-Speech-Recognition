#!/usr/bin/env python3
import speech_recognition as sr
import time
import webbrowser
import os
from gtts import gTTS
import subprocess
import pyowm
import json
import datetime
from itertools import islice
import warnings
import pyautogui
import pyaudio
import imaplib
import webbrowser
from termcolor import cprint
import vlc_ctrl

#Globals
warnings.filterwarnings("ignore")

#API Keys
owm = pyowm.OWM('98f7511d86476597089039309a13a7a1') #API Key for weather data

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    subprocess.call(['xdg-open', 'audio.mp3'])
    
def greeting():
    tts = gTTS(text="Hey JC, I'm listening", lang='en')
    tts.save("greeting.mp3")
    subprocess.call(['xdg-open', 'greeting.mp3'])

def login():
    greeting()
    voice()

def voice():
try:
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("I'm listening...")
            audio = r.listen(source)
    speech = r.recognize_google(audio)
    print("You said:   " + r.recognize_google(audio))
    speech_search = ['google', 'directions', 'youtube']
    speech = speech.lower().split(" ")
    print(speech)
    
    #Gets web searches
    if speech[0] in speech_search:
        searching(speech)
        voice()
    #Runs my scripts
    elif "script" and "run" in speech:
        scripts(speech)
        voice()
    #Control messaging apps
    elif "send" in speech:
        messaging_app(speech)
        voice()
    # close applications
    elif 'set' in speech:
        set_calendar(speech)
        voice()
    #cast media to TV
    elif speech[0] == "cast":
        google_cast(speech)
        voice()
    #close applications
    elif 'close' in speech:
        close_apps(speech)
        voice()
        
