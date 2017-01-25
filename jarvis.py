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

# Use at the beginning
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
    #open applications
    elif 'open' in speech:
        open_apps(speech)
        voice()
    #Mac controls
    elif 'mac' in speech:
        control_mac(speech)
        voice()
    #Current time
    elif 'time' in speech:
        speak(datetime.datetime.now().strftime("%I:%M %p"))
        voice()
    #provides date information
    elif 'date' in speech:
        date(speech)
        voice()
    #Gets weather data
    elif 'weather' in speech:
        choose_weather(speech)
        voice()
    #Gets temperature data
    elif 'temperature' in speech:
        choose_weather(speech)
        voice()
    #Sunrise time
    elif 'sunrise' in speech:
        choose_weather(speech)
        voice()
    #Sunset time
    elif 'sunset' in speech:
        choose_weather(speech)
        voice()
     #pause & restart program
    elif 'jarvis' in speech:
        echo(speech)
        voice()
    #provides a cheatsheet for all the voice commands
    elif 'help' in speech:
        cheatsheet()
        voice()
     #checks if any new emails have arrived in my inbox
    elif "mail" or "email" in speech:
        check_mail(speech)
        voice()
    else:
        voice()
except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        voice()
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    voice()
    
'''Putting jarvis to sleep'''
def echo(speech):
    if "sleep" in speech:
        speak("I'm going to nap")
        wake_up = input("Type anything to wake me up...\n")
        if len(wake_up) > 0:
            speak("Hey, I'm awake, do you need anything?")
    else:
        speak("I'm here, what's up?")

'''Main web searches'''
def searching(audio):
    audio_sentence = " ".join(audio)
    # search google maps
    if "google maps" in audio_sentence:
        #General Maps search
        print("Entering Google Maps search")
        location = audio[2:]
        webbrowser.open('https://www.google.nl/maps/place/' + "+".join(location) + "/&amp;")
        speak("I opened Google Maps for " + " ".join(location))

    #search google
    elif "google" in audio:
        #Google search
        search_phrase = "+".join(audio)
        webbrowser.open('https://www.google.ca/#q=' + search_phrase)
    #full google maps directions from location to destination
    elif "directions from" in audio_sentence:
        #Maps directions from [location] to [destination]
        audio = audio_sentence.split(" ")
        index_to = audio.index("to")
        location = audio[2:index_to]
        destination = audio[index_to + 1:]
        speak_location = " ".join(location)
        location = "+".join(location)
        speak_destination = " ".join(destination)
        destination = "+".join(destination)
        webbrowser.open('https://www.google.ca/maps/dir/' + location + "/" + destination)
        speak("Directions from " + speak_location  + " to " + speak_destination)
    #find directions to google maps destination with location missing
    elif "directions" in audio:
        #Maps directions to destination, requires location
        location = audio[1:]
        location = "+".join(location)
        webbrowser.open('https://www.google.nl/maps/dir//' + location )
        speak("Please enter your current location")
    #play next youtube video
    elif "next" in audio:
        print("I'm here")
        pyautogui.hotkey('shift', 'command', 'right')
    #searches youtube
    elif "search" in audio:
        print("searching youtube")
        # Searches a youtube video
        search_phrase = audio_sentence.replace("youtube", "").replace("search", "").replace(" ", "+")
        webbrowser.open('https://www.youtube.com/results?search_query=' + search_phrase)
    #Pause/play youtube videos
    elif "play" or "pause" in audio:
        pyautogui.hotkey('shift', 'command', ' ')

'''Running python scripts'''
def scripts(speech):
    if "soccer" in speech:
        os.system("cd /Users/Add_Folder_Path/ && python3 Soccer_streams.py")
    else:
        os.system("cd /Users/Add_Folder_Path/ && python3 Instalinks.py")

'''Check if any new emails'''
def check_mail(speech):
    obj = imaplib.IMAP4_SSL('imap.gmail.com', '993')
    obj.login('jeanclaude.tca@gmail.com', 'jc2549333')
    obj.select()
    obj.search(None, 'UnSeen')
    unseen_message = len(obj.search(None, 'UnSeen')[1][0].split()) - 5351
    if unseen_message > 1:
        speak("You have " + str(unseen_message) + " new messages!")
        webbrowser.open('mail.google.com')
    else:
        speak("There isn't any new emails!")

'''Google casting media to ChromeCast'''
def google_cast(speech):
    #format = cast [media] to [monitor or laptop]
    if "monitor" in speech:
        if "youtube" in speech:
            monitor_cast(media='youtube')
        elif "netflix" in speech:
            monitor_cast(media='netflix')
        else:
            monitor_cast(media= speech[1])
    elif "laptop" in speech:
        if "youtube" in speech:
            laptop_cast(media='youtube')
        elif "netflix" in speech:
            laptop_cast(media='netflix')
        else:
            laptop_cast(media=speech[1])

def monitor_cast(media):
    # Cast for 34-inch UltraWide Monitor
    subprocess.call(["/usr/bin/open", "/Applications/Google Chrome.app"])
    time.sleep(0.5)
    pyautogui.hotkey('shift', 'up')
    time.sleep(0.5)
    pyautogui.hotkey('command', 'e')
    pyautogui.typewrite(media, interval=0.02)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.click(2150, 50)
    time.sleep(1.1)
    pyautogui.moveTo(1200, 150)
    pyautogui.moveTo(1200, 160)
    pyautogui.click(1200, 150)
    time.sleep(0.5)
    pyautogui.press('esc')
    pyautogui.hotkey('command', 'tab')

def laptop_cast(media):
    # Cast for 15-inch macbook
    subprocess.call(["/usr/bin/open", "/Applications/Google Chrome.app"])
    time.sleep(0.5)
    pyautogui.hotkey('shift', 'up')
    time.sleep(0.5)
    pyautogui.hotkey('command', 'e')
    pyautogui.typewrite(media, interval=0.02)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.click(1030, 50)
    time.sleep(1.5)
    pyautogui.moveTo(640, 160)
    pyautogui.click(650, 160)
    time.sleep(0.3)
    pyautogui.press('esc')
    pyautogui.hotkey('command', 'tab')
