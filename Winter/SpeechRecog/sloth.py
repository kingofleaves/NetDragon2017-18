#!/usr/bin/env python3

import speech_recognition as sr
from gtts import gTTS
import os
import tkinter
import vlc
import time
import bluetooth

# NOTE: this example requires PyAudio because it uses the Microphone class

# recognize speech using Microsoft Bing Voice Recognition
BING_KEY = "11dfb0a39e174cdbbb5d4b35cf6a16a5"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings
# Note: The way to get api key:
# Free: https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
# Paid: https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0

root = tkinter.Tk()
language = 'en'

def speak(text):
  try:
    print(text + '\n')
    tts = gTTS(text, language)
    filename = 'temp.mp3'
    tts.save(filename)
    p = vlc.MediaPlayer(filename)
    p.play()
    time.sleep(1)
    while(p.is_playing()):
      time.sleep(0.2)
    os.remove(filename)
  except WindowsError as exc:
    print("Could not delete %s because %s" % (filename, exc))
    # continue
  # else:
    # print("Deleted %s" % file)

def listen(self):
  try: 
    with sr.Microphone() as source:
      self.r.adjust_for_ambient_noise(source)
      audio = self.r.listen(source, timeout = 15)
    return self.r.recognize_bing(audio, key=BING_KEY)
  except sr.WaitTimeoutError:
    speak("Sorry, I could not hear you.")

## Bluetooth
    
def connectToRobot():
  target_name = "HC-05"
  target_address = None

  while(target_address is None):
    nearby_devices = bluetooth.discover_devices()
    print(nearby_devices)

    for bdaddr in nearby_devices:
      print(bluetooth.lookup_name( bdaddr ))
      if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        # break
              
      if target_address is not None:
        print("found target bluetooth device with address ", target_address)
        sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

        print("Trying connection")

        i=0 # ---- your port range starts here
        maxPort = 15 # ---- your port range ends here
        err = True
        while err == True and i <= maxPort:
          print("Checking Port ",i)
          port = i
          try:

            sock.connect((target_address, port))
            err = False
          except Exception:
            ## print the exception if you like
            i += 1
            if i > maxPort:
              print("Port detection Failed.")
              return

        # print("Trying sending")
        # self.sock.send("1 2 3")
        # print("Finished sending")
        else:
          print("could not find target bluetooth device nearby")
  return sock

#### Main Code:

# Connect to Robot via BlueTooth
sock = connectToRobot()

# List of commands to the robot:
# b"p" = Opens arm / signal that robot will speak
# b"n" = Continuous nodding, keeps nodding (send b"m" to stop)
# b"m" = Stop nodding
# b"l" = Nods once-ish
# b"u" = Point to user
# b"t" = "Thinking," Closes arm and looks down
# b"w" = Wave arm
# b"m" = Nods once


# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:

  while True:
    print("Say something! It may take up to 15 seconds to process, so please be patient.")
    audio = r.listen(source)
    try:
      sock.send(b"n") #Nods as user speaks
      user_text = r.recognize_bing(audio, key=BING_KEY)
      sock.send(b"m") #Nods as user speaks
      sock.send(b"t") #Thinks before speaking
      # Parse user_text into substrings
      # check substring against fixed texts
      if user_text == "Hello.":
        sock.send(b"p")
        response = "Hi! Can you help me with this question?"
        sock.send(b"p") # point to screen
      elif user_text == "Goodbye.":
        sock.send(b"p")
        response = "Thanks for helping me out. Goodbye!"
        sock.send(b"w") # point to screen
        speak(response)
        raise SystemExit
      elif user_text == "Yes.":
        sock.send(b"p")
        response = "Great! Can you show me how to cut this pizza into eight equal slices? Please say finish when you're done."
        sock.send(b"u") # point to user
      elif user_text == "Finish.":
        sock.send(b"p")
        response = "Thank you! That looks great."
        sock.send(b"m") # nod once

        speak(response)
        raise SystemExit
      else:
        sock.send(b"p")
        response = 'You said, "' + user_text + '"'
      speak(response)
    except sr.UnknownValueError:
      sock.send(b"p")
      speak("Sorry, I didn't understand that.")
    except sr.RequestError as e:
      speak("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))


