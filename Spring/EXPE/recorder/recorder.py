#!/usr/bin/env python3
import sys
from google.cloud import texttospeech
import os

### male voice ###
# GOOGLE_VOICE = "en-US-Wavenet-D"
### female voice ###
GOOGLE_VOICE = "en-US-Wavenet-F"
SPEED = 1.1
PITCH = 4.5

def record(filename, text):
    filepath = filename + '.mp3'
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.types.SynthesisInput(text=text)
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        name=GOOGLE_VOICE)
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        speaking_rate=SPEED,
        pitch=PITCH)
    response = client.synthesize_speech(input_text, voice, audio_config)
    with open(filepath, 'wb') as out:
        out.write(response.audio_content)
    os.system('mpg123 -q ' + filepath)
    print('Created ' + filepath + ': ' + text)

if len(sys.argv) == 2:
    with open(sys.argv[1], 'r') as tsv:
        memory = [line.strip().split('\t') for line in tsv]
    for row in memory:
        record(row[0], row[1])

else:
    print("Usage: python recorder.py [FILENAME.tsv]")