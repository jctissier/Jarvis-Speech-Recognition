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

'''Controlling Messaging Apps'''
def messaging_app(speech):
    try:
        if "messenger" in speech:
            if speech[1] == "new":
                receiver = speech[4]
                message = " ".join(speech[5:])
                messenger_automator(receiver, message)
            else:
                message = " ".join(speech[2:])
                messenger_same_convo(message)
        elif "whatsapp" in speech:
            receiver = speech[3]
            message = " ".join(speech[4:])
            whatsapp(receiver, message)
    except IndexError:
        print("Index Error just occured, repeat what you were saying..")

#New Messenger = send new messenger to [recipient] [message_string]
def messenger_automator(receiver,message):
    #Getting Messenger to new person
    subprocess.call(["/usr/bin/open", "/Applications/Messenger.app"])
    time.sleep(1.5)
    pyautogui.press('tab',presses=1)
    pyautogui.typewrite(receiver, interval=0.2)
    pyautogui.press('down', presses=1)
    pyautogui.press('enter',presses=1)
    time.sleep(1)
    pyautogui.typewrite(message, interval=0.02)
    time.sleep(0.5)
    pyautogui.hotkey('command', 'tab')
    # pyautogui.press('enter')
    speak("Message has been sent to " + receiver)

#Same Messenger = send messenger [message_string]
def messenger_same_convo(message):
    subprocess.call(["/usr/bin/open", "/Applications/Messenger.app"])
    time.sleep(1)
    pyautogui.typewrite(message, interval=0.02)
    time.sleep(0.5)
    pyautogui.hotkey('command', 'tab')
    # pyautogui.press('enter')

# Message on Whatsapp = send whatsapp to [receiver] [message_string]
def whatsapp(receiver, message):
    subprocess.call(["/usr/bin/open", "/Applications/Whatsapp.app"])
    time.sleep(1.6)
    pyautogui.press('tab',presses=2,interval=0.5)
    pyautogui.typewrite(receiver, interval=0.2)
    time.sleep(1)
    pyautogui.press('enter', presses=1)
    time.sleep(1)
    pyautogui.typewrite(message, interval=0.02)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('tab',presses=1)
    time.sleep(0.4)
    pyautogui.hotkey('command' , 'tab')
    speak("Whatsapp has been sent to " + receiver)

'''Control Fantastical and set calendar events'''
#set calendar [entry_name] at [location] on the [date] at [time]
def set_calendar(speech):
    if "calendar" in speech:
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.2)
        pyautogui.typewrite(" ".join(speech[2:]), interval=0.03)
        pyautogui.press('enter')
        time.sleep(0.7)
        pyautogui.hotkey('ctrl', 'c')
        speak("I have created your calendar event")
    else:
        # Creating a new reminder
        # set reminder [message_string]
        subprocess.call(["/usr/bin/open", "/Applications/Reminders.app"])
        time.sleep(1)
        pyautogui.hotkey('command', 'n')
        time.sleep(0.2)
        pyautogui.typewrite(" ".join(speech[2:]), interval=0.02)
        time.sleep(0.1)
        pyautogui.press('enter')
        pyautogui.hotkey('command', 'tab')
        speak("I have created a new reminder")

'''Control Macbook Functions'''
def control_mac(speech):
    if "mute" in speech:
        cmd ="""osascript -e "set volume 0"
        """
        os.system(cmd)
#TODO - add extra functionalities if needed

'''Close Mac apps'''
def close_apps(speech):
#Closing mac apps with applescript
    print("Chosing method...")
    if "itunes" in speech:
        close ="""osascript -e 'quit app "iTunes"'"""
        os.system(close)
    elif "skype" in speech:
        close = """osascript -e 'quit app "Skype"'"""
        os.system(close)
    elif "evernote" in speech:
        close = """osascript -e 'quit app "Evernote"'"""
        os.system(close)
    elif "spotify" in speech:
        close = """osascript -e 'quit app "Spotify"'"""
        os.system(close)
    elif "messenger" in speech:
        close = """osascript -e 'quit app "Messenger"'"""
        os.system(close)
    elif "trello" in speech:
        close = """osascript -e 'quit app "Paws for Trello"'"""
        os.system(close)
    elif "chrome" in speech:
        close = """osascript -e 'quit app "Google Chrome"'"""
        os.system(close)
    elif "feedly" in speech:
        close = """osascript -e 'quit app "Feedly"'"""
        os.system(close)
    elif "preview" in speech:
        close = """osascript -e 'quit app "Preview"'"""
        os.system(close)

'''Open Mac apps'''
def open_apps(speech):
#Opening mac apps
    if "itunes" in speech:
        subprocess.call(["/usr/bin/open", "/Applications/iTunes.app"])
    elif "skype" in speech:
        subprocess.call(["/usr/bin/open", "/Applications/Skype.app"])
    elif "evernote" in speech:
        subprocess.call(["/usr/bin/open", "/Applications/Evernote.app"])
    elif "spotify" in speech:
        subprocess.call(["/usr/bin/open", "/Applications/Spotify.app"])
    elif "messenger" in speech:
        subprocess.call(["/usr/bin/open", "/Applications/Messenger.app"])
    elif "trello" in speech:
        subprocess.call(["/usr/bin/open", "/Applications/Paws for Trello.app"])
    elif "text" in speech:
        subprocess.call(["/usr/bin/open", "/Applications/TextEdit.app"])
    elif "feedly" in speech:
        subprocess.call(["/usr/bin/open", "/Applications/feedly.app"])
    elif "whatsapp" in speech:
        subprocess.call(["/usr/bin/open", "/Applications/WhatsApp.app"])
    elif "fantastical" in speech:
        subprocess.call(["/usr/bin/open", "/Applications/Fantastical 2.app"])
    elif "facebook" in speech:
        webbrowser.open("https://www.facebook.com/jean.c.tissier")
    elif "reddit" in speech:
        webbrowser.open("https://www.reddit.com")
    elif "livescore" in speech:
        webbrowser.open("https://www.livescore.com")
    elif "gmail" in speech:
        webbrowser.open("https://www.gmail.com")

'''Weather API data'''
def sunrise(data):
    # sunrise time
    print("Sunrise: " + datetime.datetime.fromtimestamp(data['sunrise_time']).strftime('%B %d %H:%M'))
    speak("Sunrise will be at " + datetime.datetime.fromtimestamp(data['sunrise_time']).strftime('%I:%M %p'))

def sunset(data):
    # sunset time
    print("Sunset: " + datetime.datetime.fromtimestamp(data['sunset_time']).strftime('%B %d %H:%M'))
    speak("Sunset will be at " + datetime.datetime.fromtimestamp(data['sunset_time']).strftime('%I:%M %p'))

def weather(speech, data, temp):
    # includes today, tomorrow and forecast
    weather_status = data['detailed_status'].strip("''")

    if "weather" and "today" in speech:
        # Today's weather
        speak("Today's weather: " + weather_status)
        speak("Temperature will average at " + str(round(temp['temp'])) + " Celcius")

    elif "weather" and "forecast" in speech:
        # Get Forecast for the next week
        forecast_week = owm.daily_forecast("Vancouver,ca", limit=7)
        f = forecast_week.get_forecast()
        print("\nForecast for the next 7 days: ")
        for weather in islice(f, 1, None):
            unix_time = weather.get_reference_time('unix')
            print("Date: " + datetime.datetime.fromtimestamp(unix_time).strftime('%B-%d') +
                  "   Weather: " + weather.get_detailed_status())

    elif "weather" and "tomorrow" in speech:
        # Tomorrow's weather
        forecast_week = owm.daily_forecast("Vancouver,ca", limit=2)
        f = forecast_week.get_forecast()
        print("\nTomorrow's Weather: ")
        for weather in f:
            unix_time = weather.get_reference_time('unix')
            tomorrow_weather = (datetime.datetime.fromtimestamp(unix_time).strftime('%B-%d') +
                                " " + weather.get_detailed_status())
        speak(tomorrow_weather)

def temperature(temp):
    #TODO - add temp for today and tomorrow
    # Temperature status
    speak("Temperature will average at " + str(round(temp['temp'])) + " Celcius")
    speak("Max Temperature will be " + str(round(temp['temp_max'])) + " Celcius")

def choose_weather(speech):
    # weather report for Vancouver
    observation = owm.weather_at_place('Vancouver,ca')
    w = observation.get_weather()
    data = json.loads(w.to_JSON())
    temperature_data = w.get_temperature(unit='celsius')

    # pick the right method
    if "weather" in speech:
        weather(speech, data, temperature_data)
    elif "temperature" in speech:
        temperature(temperature_data)
    elif "sunrise" in speech:
        sunrise(data)
    elif "sunset" in speech:
        sunset(data)

'''Provides dates information'''
def date(speech):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dayNumber = datetime.datetime.today().weekday()
    if "today" in speech:
        speak(days[dayNumber])
        speak(datetime.datetime.now().strftime("%B %d"))
    if "tomorrow" in speech:
        dayNumber = dayNumber + 1
        if dayNumber == 7:
            speak("Monday")
            speak((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%B %d"))
        else:
            speak(days[dayNumber])
            speak((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%B %d"))

# Run these methods
if __name__ == "__main__":
    run = login()
