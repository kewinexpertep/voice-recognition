#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
from pygame import mixer
import speech_recognition as sr
import microgear.client as microgear
from time import ctime
import time
import os
from gtts import gTTS
import playsound

key = 'key'
secret = 'secret key'
app = 'APP_ID'
microgear.create(key,secret,app,{'debugmode': True})
connected = False

def connection():
    global connected
    connected = True
    
    print("Connected")
    
def subscription(topic,msg):
    console.log(msg)
    name = msg.decode("utf-8") 
    
    #speak("Welcome " + name)
    #if msg == "b'?'":
        #microgear.publish("/countPeople",countPeople)
def disconnect():
    print("disconnected")
def speak(audioString):
    print(audioString)
    microgear.publish('/speech',audioString)
    tts = gTTS(text=audioString, lang='en')
    fileName = str(time.time()) + ".mp3"
    tts.save(fileName)
    os.system("mpg321 " + fileName)
    playsound.playsound(fileName,True)
    #playsound(fileName,True)
    os.remove(fileName)
 
def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
 
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        #speak("I not understand you.")
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data
 
def reaction(data):
    if data is not '':
        microgear.publish('/speech',"You : " + data)
        if "how are you" in data or data in ("how are you","how do you feel") :
            speak("I am fine")
    
        if "what time" in data:
            speak(ctime())

        if "turn on light" in data:
            speak("Ok turn on the light")
            microgear.chat("lightEdge",'1')

        if "turn off light" in data:
            speak("Ok turn off the light")
            microgear.chat("lightEdge",'0')

        if "turn off air" in data:
            speak("Ok turn off Air condition")
            microgear.chat("AIRCONSWITCH",'10')

        if "turn on air" in data:
            speak("Ok turn on Air condition")
            microgear.chat("AIRCONSWITCH",'11')

        if "where is" in data:
            data = data.split(" ")
            location = data[2]
            speak("Hold on, I will show you where " + location + " is.")
            os.system("chromium-browser https://www.google.nl/maps/place/" + location + "/&amp;")

# initialization
microgear.setalias("speech")
microgear.on_connect = connection
microgear.on_disconnect = disconnect
microgear.on_message = subscription
microgear.connect(False)

time.sleep(2)
speak("Hi everyone, what can I do for you?")
while 1:
    data = recordAudio()
    reaction(data)