#!/usr/bin/env python

import time
import sys
import json
json_file = open('data.json')
data = json.load(json_file)
# some_file.py
import sys
#This list below is all the phrases that can be used to get information about a specific component
dummyphoneList = ["assemble a dummyphone", "assemble dummyphone", "assemble the dummyphone", "make a phone", "do a demo", "do a demonstration"]
specsList = ["tell me about","talk about", "specifications", "specs"] 
highList = ["height", "tall", "how high"]
widthList = ["how wide", "width", "depth"]
longList = ["how long", "length"]
colorList = ["color"]
weightList = ["weight", "how heavy"]
materialList = ["material"]
installationList = ["how to install", "how do you install", "installation"]
purposeList = ["purpose", "function","functionality"]
showMe["show me", "where is", "look like"]
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.append('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter')

import ActionClient

def determineFuses(command):
    if "fuse" in command or "fuses" in command:
        commandList = command.split(" ")
        try:
            fusePlacement = commandList.index("fuse")
        except:
            fusePlacement = commandList.index("fuses")
        commandList = (command.split(' ')[fusePlacement-2: fusePlacement+2])
        if "0" in commandList or "without" in commandList or "zero" in commandList or "no" in commandList:
            return 0
        elif "1" in commandList or "one" in commandList or "single" in commandList:
            return 1
        else:
            return 2
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
    def installFuses(self, amount = 2):
        if self.pcbInstalled == True:
            print("Installing " + str(amount) + " fuses")
        else:
            print("Can not install fuses without pcb")     
    def placeBottom(self):
        self.bottomPlaced = True
        print("Placing up bottom")
	ActionClient.call_server('bottomCover')
    def installPCB(self, install):
        if self.bottomPlaced and install:
            self.pcbInstalled = True
	    ActionClient.call_server('PCB')
            print("Installing PCB")
    def placeTopCover(self, install):
        if self.bottomPlaced and install:
            self.topCoverInstalled = True
	    ActionClient.call_server('topCover')
            print("Installing top cover")
        else:
            print("Will not install topcover")
class order:
    fuses = 2
    installPcb = True
    installCoverBottom = True
    installCoverTop = True
class baxter:
    currentJob = "Nothing"
    previousJob = "I havent done anything yet"
    currentJobDetails = None
    previousJobDetail = None
    
def helloBaxter(talk):
    Phone = phone()
    talk = talk.lower()
    tempList = specsList + widthList + longList + colorList + weightList + materialList + installationList + purposeList
    response = ""
    if any(x in talk for x in dummyphoneList):
        Phone.placeBottom()
        Order = order
        order.installPcb = determinePcb(talk)
        order.fuses = determineFuses(talk)
        order.installCoverTop = determineTop(talk)
        Phone.installPCB(order.installPcb)
        Phone.installFuses(order.fuses)
        Phone.placeTopCover(order.installCoverTop)
    elif any(x in talk for x in tempList):
        for x in data:
            if (data[x]["type"].lower() in talk):
                if (x in talk for x in highList):
                    response = (data[x]["type"] +" is "+data[x]["height"]+ "mm tall")
                elif (x in talk for x in widthList):
                    response = (data[x]["type"] +" is "+data[x]["width"]+ "mm wide")
                elif (x in talk for x in longList):
                    response = (data[x]["type"] +" is "+data[x]["length"]+ "mm long")
                elif (x in talk for x in colorList):
                    response = (data[x]["type"] +" is "+data[x]["colors"])
                elif (x in talk for x in materialList):
                    response = (data[x]["type"] +" is made from "+data[x]["materials"])
                elif (x in talk for x in installationList):
                    response = (data[x]["type"] +" "+data[x]["installation"])
                elif (x in talk for x in purposeList):
                    response = (data[x]["type"] +"'s purpose is "+data[x]["purpose"]+ "mm wide")
                elif (x in talk for x in specsList):
                    response = ("All the specs for the "data[x]["type"] +" is width:"+data[x]["width"]+ "mm. height:"+data[x]["height"]+ "mm. Length:"+data[x]["length"]+
                    "mm color:"+data[x]["colors"]+ "weight:"+data[x]["weight"]+ "grams. material:"+data[x]["material"]+ "installation:"+data[x]["installation"]+ 
                    "Purpose:"+data[x]["purpose"])
    elif any(x in talk for x in showMe):
        for x in data:
            if (data[x]["type"].lower() in talk):
                #TODO, make baxter show component on screen and point to it
                print(data[x]["type"] + "Is here")
    elif any(x in talk for x in showMe):
        print "Proceeding"
    print(response)
                    

talks = input("Prompt:")
helloBaxter(talks)