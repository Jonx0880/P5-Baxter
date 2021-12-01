import time
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
    currentJobDetails = None
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

# while True:
#     if talk == 
