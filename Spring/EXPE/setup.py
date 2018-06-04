#!/usr/bin/env python3

import speech_recognition as sr
from gtts import gTTS
import os

# NOTE: this example requires PyAudio because it uses the Microphone class

# recognize speech using Microsoft Bing Voice Recognition
BING_KEY = "94a54eca13074b93958fd66fd9c968bf"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
# Note: The way to get api key:
# Free: https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
# Paid: https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0

language = 'en'

def speak(text):
  print(text)
  tts = gTTS(text, language)
  filename = 'temp.mp3'
  tts.save(filename)
  os.system('mpg123 -q ' + filename)
  os.remove(filename)

def listen_record(filename):
  audio = r.listen(source)
  try:
    name = r.recognize_bing(audio, key=BING_KEY)
    tts = gTTS(name, language)
    tts.save(filename)
    os.system('mpg123 -q ' + filename)
    return name
  except sr.UnknownValueError:
    speak("Sorry, I didn't understand that.")
    return None
  except sr.RequestError as e:
    speak("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
    return None

def type_record(filename):
  name = raw_input('Enter the input for ' + filename + ': ')
  try:
    tts = gTTS(name, language)
    tts.save(filename)
    if confirm(filename):
      return name
    else:
      return None
  except:
    return None

def confirm(filename):
  os.system('mpg123 -q ' + filename)
  choice = raw_input('Is this correct? [Y/n]: ').lower()
  while True:
    if choice == 'y' or choice == 'yes' or choice == '':
      return True
    elif choice == 'n' or choice == 'no':
      return False
    else:
      print("Please choose 'y' or 'n'.")
      choice = raw_input('Is this correct? [Y/n]: ').lower()


# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
  A_NAME = None
  B_NAME = None
  C_NAME = None
  D_NAME = None
  while not (A_NAME and B_NAME and C_NAME and D_NAME):
    while not A_NAME:
      speak("A, what is your name?")
      try:
        A_NAME = type_record('A.mp3')
      except:
        pass
    while not B_NAME:
      speak("B, what is your name?")
      try:
        B_NAME = type_record('B.mp3')
      except:
        pass
    while not C_NAME:
      speak("C, what is your name?")
      try:
        C_NAME = type_record('C.mp3')
      except:
        pass
    while not D_NAME:
      speak("D, what is your name?")
      try:
        D_NAME = type_record('D.mp3')
      except:
        pass