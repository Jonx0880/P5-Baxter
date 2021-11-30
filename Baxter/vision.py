#!/usr/bin/env python

import cv2



def componentRegonition(img):
	components = []	

	#Crop image to component locations [ymin:ymax,xmin:xmax]
	topCover = img [550-10:550+10,650-10:650+10]
	bottomCover = img [610-10:610+10,520-10:520+10]	
	PCB = img [490-10:490+10,800-10:800+10] #location if placed in fixture
#	PCB = img [630-10:630+10,790-10:790+10] #location in image used for development

	meanTopCover = cv2.mean(topCover)
	meanBottomCover = cv2.mean(bottomCover)
	meanPCB = cv2.mean(PCB)

	if meanTopCover[0] > 250 and meanTopCover[1] > 250 and meanTopCover[2] > 250:
		components.append('whiteTopCover')
	#elif meanTopCover[0] > 250 and meanTopCover[1] > 250 and meanTopCover[2] > 250: change values in if statements to match color of covers
	#	components.append('blueTopCover')
	#elif meanTopCover[0] > 250 and meanTopCover[1] > 250 and meanTopCover[2] > 250: 
	#	components.append('blackTopCover')
	else: components.append('missing')

	if 20 < meanBottomCover[0] < 40 and 20 < meanBottomCover[1] < 40 and 20 < meanBottomCover[2] < 40:
		components.append('BottomCover')
	else: components.append('missing')	

	if 35 < meanPCB[0] < 50 and 35 < meanPCB[1] < 50 and meanPCB[2] < 20:
		components.append('PCB')
	else: components.append('missing')

	return components

image = cv2.imread('/home/jimmi/ros_ws/camera_image.jpeg')
test = componentRegonition(image)
print(test)
