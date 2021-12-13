import sys
import json
def talk(key):
    json_file = open('talk.json')
    data = json.load(json_file)
    print(data[key])