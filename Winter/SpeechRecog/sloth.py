#!/usr/bin/env python3

import http.client
import urllib.parse
import json
import speech_recognition as sr
from xml.etree import ElementTree


# NOTE: this example requires PyAudio because it uses the Microphone class

# recognize speech using Microsoft Bing Voice Recognition
BING_KEY = "11dfb0a39e174cdbbb5d4b35cf6a16a5"  # Microsoft Bing Voice Recognition API keys 32-character lowercase hexadecimal strings


#Note: The way to get api key:
#Free: https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
#Paid: https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0

params = ""
headers = {"Ocp-Apim-Subscription-Key": BING_KEY}

#AccessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken";
AccessTokenHost = "api.cognitive.microsoft.com"
path = "/sts/v1.0/issueToken"

# Connect to server to get the Access Token
print ("Connect to server to get the Access Token")
conn = http.client.HTTPSConnection(AccessTokenHost)
conn.request("POST", path, params, headers)
response = conn.getresponse()
print(response.status, response.reason)

data = response.read()
conn.close()

accesstoken = data.decode("UTF-8")
print ("Access Token: " + accesstoken)

body = ElementTree.Element('speak', version='1.0')
body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
voice = ElementTree.SubElement(body, 'voice')
voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
voice.set('{http://www.w3.org/XML/1998/namespace}gender', 'Female')
voice.set('name', 'Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)')
voice.text = 'This is a demo to call microsoft text to speech service in Python.'

headers = {"Content-type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
            "Authorization": "Bearer " + accesstoken,
            "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
            "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
            "User-Agent": "TTSForPython"}

#Connect to server to synthesize the wave
print("\nConnect to server to synthesize the wave")
conn = http.client.HTTPSConnection("speech.platform.bing.com")
conn.request("POST", "/synthesize", ElementTree.tostring(body), headers)
response = conn.getresponse()
print(response.status, response.reason)

data = response.read()
conn.close()
print("The synthesized wave length: %d" %(len(data)))

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    while True:
        print("Say something!")
        audio = r.listen(source)
        user_text = r.recognize_bing(audio, key=BING_KEY)
        try:
            print("Microsoft Bing Voice Recognition thinks you said " + user_text)
        except sr.UnknownValueError:
            print("Microsoft Bing Voice Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
        if user_text == "End program.":
            raise SystemExit
