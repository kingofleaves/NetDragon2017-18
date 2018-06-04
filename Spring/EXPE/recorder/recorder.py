#!/usr/bin/env python3
import csv
import sys
from gtts import gTTS

language = 'en'

def record(filename, text):
    filepath = filename + '.mp3'
    try:
        tts = gTTS(text, language)
        tts.save(filepath)
        print('Created ' + filepath + ': ' + text)
    except:
        print('Failed to create ' + filepath + ': ' + text)

if len(sys.argv) == 2:
    with open(sys.argv[1], 'r') as tsv:
        memory = [line.strip().split('\t') for line in tsv]
    for row in memory:
        record(row[0], row[1])

else:
    print("Usage: python recorder.py [FILENAME.tsv]")