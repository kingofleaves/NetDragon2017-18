#!/usr/bin/env python3

from google.cloud import texttospeech
import os

### male voice ###
# GOOGLE_VOICE = "en-US-Wavenet-D"
### female voice ###
GOOGLE_VOICE = "en-US-Wavenet-F"

def speak(text):
  print(text)
  client = texttospeech.TextToSpeechClient()
  input_text = texttospeech.types.SynthesisInput(text=text)
  voice = texttospeech.types.VoiceSelectionParams(
      language_code='en-US',
      name=GOOGLE_VOICE)
  audio_config = texttospeech.types.AudioConfig(
      audio_encoding=texttospeech.enums.AudioEncoding.MP3,
      speaking_rate=1.1,
      pitch=4.5)
  response = client.synthesize_speech(input_text, voice, audio_config)
  with open('output.mp3', 'wb') as out:
      out.write(response.audio_content)

  os.system('mpg123 -q "output.mp3"')
  os.remove('output.mp3')

def type_record(filename):
  text = raw_input('Enter the input for ' + filename + ': ')
  client = texttospeech.TextToSpeechClient()
  input_text = texttospeech.types.SynthesisInput(text=text)
  voice = texttospeech.types.VoiceSelectionParams(
      language_code='en-US',
      name=GOOGLE_VOICE)
  audio_config = texttospeech.types.AudioConfig(
      audio_encoding=texttospeech.enums.AudioEncoding.MP3,
      speaking_rate=1.1,
      pitch=6.0)
  response = client.synthesize_speech(input_text, voice, audio_config)
  with open(filename, 'wb') as out:
      out.write(response.audio_content)
  if confirm(filename):
    return text
  else:
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