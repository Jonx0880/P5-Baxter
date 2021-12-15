#!/usr/bin/env python

import time
import sys
import json
import talk
json_file = open('data.json')
data = json.load(json_file)
# some_file.py
import sys
#This list below is all the phrases that can be used to get information about a specific component
dummyphoneList = ["assemble a dummyphone", "assemble dummyphone", "assemble the dummyphone", "make a phone", "do a demo", "do a demonstration", "assemble a phone", "assemble phone"]
specsList = ["tell me about","talk about", "specifications", "specs"] 
highList = ["height", "tall", "how high"]
widthList = ["how wide", "width", "depth"]
longList = ["how long", "length"]
colorList = ["color"]
weightList = ["weight", "how heavy"]
materialList = ["material"]
installationList = ["how to install", "how do you install", "installation"]
purposeList = ["purpose", "function","functionality"]
showMe = ["show me", "where is", "look like"]
pickUpList = ["hand me", "give me", "reach me", "pick up"]
stopList = ["stop", "pause"]
continueList = ["continue"]
yesList = ["yes", "yeah"]
noList = ["no", "nope"]
statusList = ["what are you doing", "whats up", "what you doing"]

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.append('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter')

import ik_client_example
import ActionClient
import vision

def determineFuses(command):
        if "fuse" in command or "fuses" in command:
        commandList = command.split(" ")
        try:
            commandPlacement = commandList.index("fuse")
        except:
            commandPlacement = commandList.index("fuses")
        commandList = (command.split(' ')[commandPlacement-2: commandPlacement+2])
        if "0" in commandList or "without" in commandList or "zero" in commandList or "no" in commandList:
            return 0
        elif "1" in commandList or "one" in commandList or "single" in commandList:
            return 1
        else:
            return 2

def determineTop(command):
    if "top" in command or "top cover" in command or "topcover" in command:
        commandList = command.split(" ")
        try:
            commandPlacement = commandList.index("top")
        except:
            commandPlacement = commandList.index("topcover")
        commandList = (command.split(' ')[commandPlacement-2: commandPlacement+2])
        if "no" in commandList or "without" in commandList:
            return False
        else:
            return True
    else:
        return True

def determinePcb(command):
    if "pcb" in command or "circuit board" in command:
        commandList = command.split(" ")
        try:
            commandPlacement = commandList.index("pcb")
        except:
            commandPlacement = commandList.index("circuit")
        commandList = (command.split(' ')[commandPlacement-2: commandPlacement+2])
        if "no" in commandList or "without" in commandList:
            return False
        else:
            return True
    else:
        return True

class phone:
    pcbInstalled = False  
    bottomPlaced = False
    fusesInstalled = False
    topCoverInstalled = False  
    components = []
    def installFuses(self, amount = 2):
        if self.pcbInstalled == True and amount > 0:
            print("Installing " + str(amount) + " fuses")
            self.components.append('fuse')
        else:
            print("Can not install fuses without pcb")     
    def placeBottom(self):
        self.bottomPlaced = True
        print("Placing up bottom")
        self.components.append('bottomCover_pickUp')
        self.components.append('bottomCover_assemble')
    def installPCB(self, install):
        if self.bottomPlaced and install:
            self.pcbInstalled = True
            self.components.append('PCB_pickUp')
            self.components.append('PCB_assemble')
    def placeTopCover(self, install, talk):
        if self.bottomPlaced and install:
            self.topCoverInstalled = True
            if "blue" in talk:
                color="blue"
            elif "black" in talk:
                color="black"
            elif "white" in talk:
                color="white"
            else:
                color=""
            self.components.append(color+'topCover_pickUp')
            self.components.append('topCover_assemble')
                print("Installing top cover")
            else:
                print("Will not install topcover")
    
def helloBaxter(talk):
    talk = talk.lower()
    tempList = specsList + highList + longList + widthList + longList + colorList + weightList + materialList + installationList + purposeList
    response = ""
    if any(x in talk for x in dummyphoneList):
        Phone = phone()
	    Phone.components = []
        Phone.placeBottom()
        Phone.installPCB(determinePcb(talk))
        Phone.installFuses(determineFuses(talk))
        Phone.placeTopCover(determineTop(talk), talk)
	    ActionClient.call_server(Phone.components)
    elif any(x in talk for x in tempList):
        for x in data:
            if (data[x]["type"].lower() in talk):
                if any(x in talk for x in highList):
                    response = (data[x]["type"] +" is "+data[x]["height"]+ "mm tall")
                elif any(x in talk for x in widthList):
                    response = (data[x]["type"] +" is "+data[x]["width"]+ "mm wide")
                elif any(x in talk for x in longList):
                    response = (data[x]["type"] +" is "+data[x]["length"]+ "mm long")
                elif any(x in talk for x in colorList):
                    response = (data[x]["type"] +" is "+data[x]["colors"])
                elif any(x in talk for x in materialList):
                    response = (data[x]["type"] +" is made from "+data[x]["materials"])
                elif any(x in talk for x in installationList):
                    response = (data[x]["type"] +" "+data[x]["installation"])
                elif any(x in talk for x in purposeList):
                    response = (data[x]["type"] +"'s purpose is "+data[x]["purpose"]+ "mm wide")
                elif any(x in talk for x in weightList):
                    response = (data[x]["type"] +" weighs "+data[x]["weight"]+ " grams")    
                elif any(x in talk for x in specsList):
                    response = ("All the specs for the "+data[x]["type"] +" is width:"+data[x]["width"]+ "mm. height: "+data[x]["height"]+ "mm. Length:"
                    +data[x]["length"]+"mm color:"+data[x]["colors"]+ "weight:"+data[x]["weight"]+ " grams. material: "+data[x]["material"]+ " installation:"+data[x]["installation"]+ 
                    " Purpose:"+data[x]["purpose"])
    elif any(x in talk for x in showMe):
        for x in data:
            if (data[x]["type"].lower() in talk):
                #TODO, make baxter show component on screen and point to it
		        ik_client_example.pointAt(data[x]["type"])
                component = data[x]["type"]
                component.replace(" ","")
                component = component.lower()
                vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/'+component+'.png')
     
    elif any(x in talk for x in pickUpList):
        for x in data:
            if (data[x]["type"].lower() in talk):
		print "testing"
		if data[x]["type"] == 'bottom cover':
			ik_client_example.bottom_cover_pickUp()

		elif data[x]["type"] == 'top cover':
			ik_client_example.top_cover_pickUp()
			
		elif data[x]["type"] == 'PCB':
			print "pick up pcb"
			ik_client_example.PCB_pickUp()
    elif any(x in talk for x in stopList):
        print "Proceeding"
	    ActionClient.cancel_goal()
    elif any(x in talk for x in continueList):
        print "Proceeding"
	    ActionClient.continue_goal()
    elif any(x in talk for x in noList):
        print "Proceeding"
    elif any(x in talk for x in yesList):
        print "Proceeding"
    elif any(x in talk for x in statusList):
        print "proceeding"
	    ActionClient.current_action()
    print(response)
