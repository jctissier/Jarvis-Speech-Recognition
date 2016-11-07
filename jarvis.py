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
