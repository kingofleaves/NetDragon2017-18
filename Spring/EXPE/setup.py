#!/usr/bin/env python3

import speech_recognition as sr
from gtts import gTTS
import os
import tkinter
import time

# NOTE: this example requires PyAudio because it uses the Microphone class

# recognize speech using Microsoft Bing Voice Recognition
BING_KEY = "94a54eca13074b93958fd66fd9c968bf"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
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
  os.system('mpg123 -q ' + filename)
  os.remove(filename)

def record(filename):
  audio = r.listen(source)
  try:
    name = r.recognize_bing(audio, key=BING_KEY)
    tts = gTTS(name, language)
    tts.save(filename)
    response = 'Your name is ' + name
    speak(response)
    return name
  except sr.UnknownValueError:
    speak("Sorry, I didn't understand that.")
    return None
  except sr.RequestError as e:
    speak("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
    return None

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
  A_NAME = None
  B_NAME = None
  C_NAME = None
  D_NAME = None
  while not (A_NAME and B_NAME and C_NAME and D_NAME):
    if not A_NAME:
      speak("A, what is your name?")
      try:
        A_NAME = record('A.mp3')
      except:
        pass
    if not B_NAME:
      speak("B, what is your name?")
      try:
        B_NAME = record('B.mp3')
      except:
        pass
    if not C_NAME:
      speak("C, what is your name?")
      try:
        C_NAME = record('C.mp3')
      except:
        pass
    if not D_NAME:
      speak("D, what is your name?")
      try:
        D_NAME = record('D.mp3')
      except:
        pass