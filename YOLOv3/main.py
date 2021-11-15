import cv2
import numpy as np

#Capture Video Stream as cap and states the width and height for darknet (both are set as 320 here)
cap = cv2.VideoCapture(0)
whT = 320
#sets confidence threshold so we can remove too low confidence
confThreshold = 0.5
#sets threshold for our nonmaximum supression (higher threshold results in fewer boxes)
nmsThreshold = 0.3

#Loads class names as classesFile and print them out
classesFile = "coco.names"
classNames = []
with open(classesFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")
print(classNames)

#Loads the YOLOv3 configuration file and weights as new variables
modelConfiguration = "yolov3.cfg"
modelWeights = "yolov3.weights"

#Create a darknet network based on the model configuration and weights based on opencv
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

#Finding bounding boxes function
def findObjects(outputs, img):
    #height, width, channels of img
    hT, wT, cT = img.shape
    bbox = [] #bounding box list that will contain value of x,y,w,h
    classIds = [] #list that contains class ID's
    confs = [] #list of confidence values

    #here we find the maximum confidence value and saves it as confidence
    for output in outputs:
        for detection in output:
            scores = detection[5:] #removing first 5 elements as they are not ID's
            classId = np.argmax(scores) #finds the max confidence value
            confidence = scores[classId]
            if confidence > confThreshold: #finding parameters for bounding boxes
                w,h = int(detection[2]*wT), int(detection[3]*hT)
                x,y = int((detection[0]*wT)-w/2), int((detection[1]*hT)-h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))

    indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        box = bbox[i]
        x,y,w,h = box[0], box[1], box[2], box[3]
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
        cv2.putText(img,f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%',
                    (x,y-10), cv2.FONT_HERSHEY_PLAIN,0.6,(255,0,255),2)

while True:
    success, img = cap.read()

    #Converts it to blob format, as this is what the network uses
    blob = cv2.dnn.blobFromImage(img, 1/255,(whT, whT),[0,0,0], crop=False )
    net.setInput(blob)

    layerNames = net.getLayerNames()
    #print(layerNames)
    #print(net.getUnconnectedOutLayers())
    outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]

    #when we print the shape of the first output layer (there are 3 layers) we get (300,85)
    #the first five values are (x,y,w,h,highest confidence number) and then the confidene of the 80 classes
    outputs = net.forward(outputNames)
    #print(outputs[0].shape)

    findObjects(outputs, img)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
