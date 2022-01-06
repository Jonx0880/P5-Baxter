#!/usr/bin/env python

import cv2
import ik_client_example
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import baxter_interface
import rospy
import cv_bridge
from sensor_msgs.msg import (
    Image,
)
import time

# function for checking if components are pressent
def componentRegonition():
        #mage empty list
	components = []
	# read image
	img = cv2.imread('/home/jimmi/ros_ws/camera_image.jpeg')

	#Crop image to component locations [ymin:ymax,xmin:xmax]
	topCover = img [550-10:550+10,650-10:650+10]
	bottomCover = img [610-10:610+10,520-10:520+10]	
	PCB = img [490-10:490+10,800-10:800+10]

        # get the mean for R, G and B in each cropped image
	meanTopCover = cv2.mean(topCover)
	meanBottomCover = cv2.mean(bottomCover)
	meanPCB = cv2.mean(PCB)

	# use mean values to check if the top cover is missing (top cover can be 3 different colors)
	if meanTopCover[0] > 250 and meanTopCover[1] > 250 and meanTopCover[2] > 250:
                # write in list that top cover white
		components.append('whiteTopCover')
	elif meanTopCover[0] > 50 and meanTopCover[1] > 30 and meanTopCover[2] < 50 :
                # write in list that top cover blue
		components.append('blueTopCover')
	elif meanTopCover[0] < 50 and meanTopCover[1] < 50 and meanTopCover[2] < 50:
                # write in list that top cover black
		components.append('blackTopCover')
	else: components.append('missing') # write in list that top cover is missing

        # same as above but for bottom cover
	if 20 < meanBottomCover[0] < 40 and 20 < meanBottomCover[1] < 40 and 20 < meanBottomCover[2] < 40:
		components.append('BottomCover')
	else: components.append('missing')	

	# same as above but for PCB
	if  meanPCB[1] > meanPCB[2]+5: # unlike the two other he the difference between blue and red mean is checked. instead of checkin if the r, g, b, calue are within set values.
		components.append('PCB')
	else: components.append('missing')

        #returns components list
	return components

# function used to save an image
def image_callback(msg):
    print("Received an image!")
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = CvBridge().imgmsg_to_cv2(msg, "bgr8")
	
    except CvBridgeError, e:
        print(e)
    else: # happens every time there is no error
	cv2.imwrite('camera_image.jpeg', cv2_img) #saves image
	print 'img saved'
        # Save your OpenCV2 image as a jpeg 
	#head = baxter_interface.Head()
	#head.command_nod()        
	#cv2.imshow('raw', cv2_img)
	#cv2.imshow('modifi',img)

# function used to take an image
def take_image():
        #move to image position
	ik_client_example.cameraPos()

	# set camera parameters
	camera = baxter_interface.CameraController('left_hand_camera')
    	camera.resolution=(1280,800)

    	# image topic
	image_topic = "/cameras/left_hand_camera/image"

        # wait 2 seconds (makes sure camera is stabalized after the movement)
	time.sleep(2)

        # reads one messege from the image topic
        img = rospy.wait_for_message(image_topic, Image)
        # calls function for saving the image
	image_callback(img)	

# sends image to baxters interface
def send_image(path):
    img = cv2.imread(path) # reads image

    # convers image from open cv image to image message used in ROS
    msg = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")

    # publishes image to the topic baxters screen uses to display images
    pub = rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=1)
    pub.publish(msg)
    # Sleep to allow for image to be published.
    rospy.sleep(1)


