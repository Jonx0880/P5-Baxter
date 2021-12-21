#!/usr/bin/env python

import time
import sys
import json
import talk as tlk
json_file = open('data.json') #Knowledge database
data = json.load(json_file) #Parsed data
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

def determineFuses(command): #Will check if Fuse in mentioned in command
    if "fuse" in command or "fuses" in command:
        commandList = command.split(" ")
        try: #Find "fuse" location in string
            commandPlacement = commandList.index("fuse")
        except:
            commandPlacement = commandList.index("fuses")
        commandList = (command.split(' ')[commandPlacement-2: commandPlacement+2]) #Splices string 2 chr before and after "fuse"
        if "0" in commandList or "without" in commandList or "zero" in commandList or "no" in commandList: #Checking if any numbers or other modifiers have been mentioned
            return 0
        elif "1" in commandList or "one" in commandList or "single" in commandList:
            return 1
    else: #If fuse is not mentioned, return standard (2)
        return 2

def determineTop(command): #Basically same thing happening here, just with top cover.
    if "top" in command or "top cover" in command or "topcover" in command:
        commandList = command.split(" ")
        try:
            commandPlacement = commandList.index("top")
        except:
            commandPlacement = commandList.index("topcover")
        commandList = (command.split(' ')[commandPlacement-2: commandPlacement+2])
        if "no" in commandList or "without" in commandList:#Now its a bool and not int, but same thing really
            return False
        else:
            return True
    else:
        return True

def determinePcb(command): #Again, same thing really. Just with pcb.
    if "pcb" in command or "circuit board" in command:
        commandList = command.split(" ")
        try:
            commandPlacement = commandList.index("pcb")
        except:
            commandPlacement = commandList.index("circuit")
        commandList = (command.split(' ')[commandPlacement-2: commandPlacement+2])
        if "no" in commandList or "without" in commandList: #Returns bool again
            return False
        else:
            return True
    else:
        return True

class phone: #Class used to manage phone components.
    pcbInstalled = False  #All components installation progress
    bottomPlaced = False
    fusesInstalled = False
    topCoverInstalled = False  
    components = []#Empty list... Will be filled with the installation steps, and sent on to the action server.
    def installFuses(self, amount = 2): #Checks if pcb is installed, since it cant install fuses without pcb.
        if self.pcbInstalled == True and amount > 0: #Also checks if it should install fuses (Amount > 0)
            print("Installing " + str(amount) + " fuses")
            self.components.append('fuse') #Appends fuse to components list, so fuse will now get installed.
        else:
            print("Can not install fuses without pcb")     
    def placeBottom(self): #It can always install the bottom cover, so it will just set bottomPlaced to true always. No checkups needed
        self.bottomPlaced = True
        print("Placing up bottom")
        self.components.append('bottomCover_pickUp') #Adds the processes to components list
        self.components.append('bottomCover_assemble')
    def installPCB(self, install): #Works exactly like installFuses(), except it checks for bottomPlaced
        if self.bottomPlaced and install:
            self.pcbInstalled = True
            self.components.append('PCB_pickUp')
            self.components.append('PCB_assemble')
    def placeTopCover(self, install, talk):#Once again, checks if bottom is placed, and if it should be installed.
        if self.bottomPlaced and install:
            self.topCoverInstalled = True
            if "blue" in talk: #Now checks if any color modifiers had been set
                color="blue"
            elif "black" in talk:
                color="black"
            elif "white" in talk:
                color="white"
            else:
                color=""
            self.components.append(color+'topCover_pickUp')#Adds the processes to components list, with potential color. If no color was found color will be empty.
            self.components.append('topCover_assemble')
            print("Installing top cover")
        else:
            print("Will not install topcover")
    
def helloBaxter(talk): #Main function that is called, upon receiving string from TCP_client
    talk = talk.lower() #Makes sure the string is lowercase
    tempList = specsList + highList + longList + widthList + longList + colorList + weightList + materialList + installationList + purposeList #Temp list is a list of all list regarding specs. Should in theory make faster code
    response = "" #Initialises empty response.
    if any(x in talk for x in dummyphoneList): #Checks if any string from list dummyphoneList, is present in the string talk
        Phone = phone() #If they are, a phone object will be made.
        Phone.components = []
        Phone.placeBottom()#Always install bottom
        Phone.installPCB(determinePcb(talk)) #Tries to install pcb, with determinePcb(talk) as parameter. determinePcb(talk) will return bool
        Phone.installFuses(determineFuses(talk)) #Same thing, but determineFuses will return int
        Phone.placeTopCover(determineTop(talk), talk) #Now bool again
        ActionClient.call_server(Phone.components) #Sends the Phone.components list to ActionClient 
    elif any(x in talk for x in tempList): #In case Baxter was not asked to assemble a phone, it now checks if any string inside tempList is in string talk.
        for x in data: #Runs through all components in database.
            if (data[x]["type"].lower() in talk): #Checks if component[x] is in string talk
                if any(x in talk for x in highList):#Now it checks more specifically what spec is requested
                    response = (data[x]["type"] +" is "+data[x]["height"]+ "mm tall") #Changes respone to a string, that is conveying the information requested
                elif any(x in talk for x in widthList): #Again same thing. Now just check if width has been requested
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
                elif any(x in talk for x in specsList): #This one is in case user want s to hear every spec... Sorry for the ugly formatted string...
                    response = ("All the specs for the "+data[x]["type"] +" is width:"+data[x]["width"]+ "mm. height: "+data[x]["height"]+ "mm. Length:"
                    +data[x]["length"]+"mm color:"+data[x]["colors"]+ "weight:"+data[x]["weight"]+ " grams. material: "+data[x]["material"]+ " installation:"+data[x]["installation"]+ 
                    " Purpose:"+data[x]["purpose"])
                break #Breaks function afterward so below code wont be run, in case the component was known
            else: #In case of else, no known component was mentioned
                response = "I dont know anything about this component. Please try again with another component"
		tlk.talk_raw(response) #Talk function. This will make Baxter speak in a dope Stephen Hawking voice. He will say the response string out loud.
    elif any(x in talk for x in showMe): #Basically same thing as on line 133, but for showMe list. This list is for making Baxter show you a component.
        for x in data:
            if (data[x]["type"].lower() in talk): #Checks if there is known component mentioned.
                #Send goal to action client.
                ik_client_example.pointAt(data[x]["type"])
                #Some fancy string splicing to make component names compatible with picture names B)
                component = data[x]["type"]
                component.replace(" ","")
                component = component.lower()
                #Shows picture of component on screen B)
                vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/'+component+'.png')
     
    elif any(x in talk for x in pickUpList): #Same thing as earlier. New list, pickuplist used to make Baxter pick up a component
        for x in data:
            if (data[x]["type"].lower() in talk): #Checks which component Baxter should lift
                if data[x]["type"] == 'bottom cover':
                    ik_client_example.bottom_cover_pickUp()

                elif data[x]["type"] == 'top cover':
                    ik_client_example.top_cover_pickUp()
                    
                elif data[x]["type"] == 'PCB':
                    ik_client_example.PCB_pickUp()
    elif any(x in talk for x in stopList): #Same thing again. Will make baxter pause current task
        ActionClient.cancel_goal()
    elif any(x in talk for x in continueList):#Continue
        ActionClient.continue_goal()
    elif any(x in talk for x in noList):#Will not do anything, but just a nice list to have in case it is needed.
        print "Proceeding"
    elif any(x in talk for x in yesList): #Same thing. Could delete them though...
        print "Proceeding"
    elif any(x in talk for x in statusList): #This is used to make Baxter say what he is currently doing
        ActionClient.current_action()
    
