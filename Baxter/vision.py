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

def componentRegonition():
	components = []	
	img = cv2.imread('/home/jimmi/ros_ws/camera_image.jpeg')

	#Crop image to component locations [ymin:ymax,xmin:xmax]
	topCover = img [550-10:550+10,650-10:650+10]
	bottomCover = img [610-10:610+10,520-10:520+10]	
	PCB = img [490-10:490+10,800-10:800+10] #location if placed in fixture
#	PCB = img [630-10:630+10,790-10:790+10] #location in image used for development

	meanTopCover = cv2.mean(topCover)
	meanBottomCover = cv2.mean(bottomCover)
	meanPCB = cv2.mean(PCB)

	print meanTopCover
	if meanTopCover[0] > 250 and meanTopCover[1] > 250 and meanTopCover[2] > 250:
		components.append('whiteTopCover')
	elif meanTopCover[0] > 50 and meanTopCover[1] > 30 and meanTopCover[2] < 50 : 
		components.append('blueTopCover')
	elif meanTopCover[0] < 50 and meanTopCover[1] < 50 and meanTopCover[2] < 50: 
		components.append('blackTopCover')
	else: components.append('missing')

	if 20 < meanBottomCover[0] < 40 and 20 < meanBottomCover[1] < 40 and 20 < meanBottomCover[2] < 40:
		components.append('BottomCover')
	else: components.append('missing')	
	#print meanPCB
	if  meanPCB[1] > meanPCB[2]+5:
		components.append('PCB')
	else: components.append('missing')

	return components

def image_callback(msg):
    print("Received an image!")
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = CvBridge().imgmsg_to_cv2(msg, "bgr8")
	
    except CvBridgeError, e:
        print(e)
    else:
	cv2.imwrite('camera_image.jpeg', cv2_img)
	print 'img saved'
        # Save your OpenCV2 image as a jpeg 
	#head = baxter_interface.Head()
	#head.command_nod()        
	#cv2.imshow('raw', cv2_img)
	#cv2.imshow('modifi',img)

def take_image():
	ik_client_example.cameraPos()
	camera = baxter_interface.CameraController('left_hand_camera')
    	camera.resolution=(1280,800)
	image_topic = "/cameras/left_hand_camera/image"

	time.sleep(2)
#	rospy.Subscriber(image_topic, Image, image_callback)
	img = rospy.wait_for_message(image_topic, Image)
	image_callback(img)	

def send_image(path):
    img = cv2.imread(path)
#    cv2.imshow('1', img)
#    cv2.waitKey(0)
    msg = cv_bridge.CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
    pub = rospy.Publisher('/robot/xdisplay', Image, latch=True, queue_size=1)
    pub.publish(msg)
    # Sleep to allow for image to be published.
    rospy.sleep(1)
    print 'img shown'


#rospy.init_node('image_listener')
#takeImg()
#image = cv2.imread('/home/jimmi/ros_ws/camera_image.jpeg')
#test = componentRegonition(image)
#print(test)
