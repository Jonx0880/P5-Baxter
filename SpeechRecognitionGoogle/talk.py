#!/usr/bin/env python

import sys
import json

import pyttsx3

engine = pyttsx3.init()

rate = engine.getProperty('rate')
print (rate) 
engine.setProperty('rate',125)
def talk(key):
    json_file = open('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/SpeechRecognitionGoogle/talk.json')
    data = json.load(json_file)
    engine.say(data[key])
    engine.runAndWait()
def talk_raw(key):
    engine.say(key)
    engine.runAndWait()
