#!/usr/bin/env python3

import speech_recognition as sr
from gtts import gTTS
import os
import tkinter
import vlc
import time

# NOTE: this example requires PyAudio because it uses the Microphone class

# recognize speech using Microsoft Bing Voice Recognition
BING_KEY = "11dfb0a39e174cdbbb5d4b35cf6a16a5"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
# Note: The way to get api key:
# Free: https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
# Paid: https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0

root = tkinter.Tk()
language = 'en'

def speak(text):
  print(text + '\n')
  tts = gTTS(text, language)
  filename = 'temp.mp3'
  tts.save(filename)
  p = vlc.MediaPlayer(filename)
  p.play()
  time.sleep(1)
  while(p.is_playing()):
    time.sleep(0.1)
  os.remove(filename)

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
  while True:
    print("Say something! It may take up to 15 seconds to process, so please be patient.")
    audio = r.listen(source)
    try:
      user_text = r.recognize_bing(audio, key=BING_KEY)
      if user_text == "Secret.":
        response = "You found the secret!"
      elif user_text == "Goodbye.":
        response = "Thanks for playing with me. Goodbye!"
        speak(response)
        raise SystemExit
      else:
        response = 'You said, "' + user_text + '"'
      speak(response)
    except sr.UnknownValueError:
      speak("Sorry, I didn't understand that.")
    except sr.RequestError as e:
      speak("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))


