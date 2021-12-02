import time
import sys
import json
json_file = open('data.json')
data = json.load(json_file)
# some_file.py
import sys
specsList = ["tell me about","talk about", "specifications", "specs"] 
highList = ["height", "tall", "how high"]
widhtList = ["how wide", "width", "depth"]
longList = ["how long", "length"]
colorList = ["color"]
weightList = ["weight", "how heavy"]
materialList = ["material"]
installationList = ["how to install", "how do you install", "installation"]
purposeList = ["purpose", "function","functionality"]

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
    def installPCB(self, install):
        if self.bottomPlaced and install:
            self.pcbInstalled = True
            print("Installing PCB")
    def placeTopCover(self, install):
        if self.bottomPlaced and install:
            self.topCoverInstalled = True
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
    currentJobDetails = None    elif any(x in talk for x in specsList):
        for x in data:
            if (data[x]["type"].lower() in talk):
                if (x in talk for x in highList):
                    print(data[x]["type"] +" is "+data[x]["height"]+ "mm tall")
                elif (x in talk for x in specsList):
                    print("FUCK")
    previousJobDetail = None
def helloBaxter(talk):
    Phone = phone()
    talk = talk.lower()
    if ("assemble" in talk or "make a phone" in talk):
        Phone.placeBottom()
        Order = order
        order.installPcb = determinePcb(talk)
        order.fuses = determineFuses(talk)
        order.installCoverTop = determineTop(talk)
        Phone.installPCB(order.installPcb)
        Phone.installFuses(order.fuses)
        Phone.placeTopCover(order.installCoverTop)
    elif any(x in talk for x in specsList):
        for x in data:
            if (data[x]["type"].lower() in talk):
                if (x in talk for x in highList):
                    print(data[x]["type"] +" is "+data[x]["height"]+ "mm tall")
                elif (x in talk for x in specsList):
                    print("FUCK")
# while True:
#     if talk == 
talks = raw_input("Prompt:")
helloBaxter(talks)
