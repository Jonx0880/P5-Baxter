#!/usr/bin/env python

#import Phone
import rospy
import time
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.append('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter')
import vision
import ActionClient

#sys.path.append('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter')


rospy.init_node('action_client')
#time.sleep(2)
vision.take_image()
components = vision.componentRegonition()
print components[0]
print components[1]
#print components
#vision.send_image('/home/jimmi/ros_ws/camera_image.jpeg')
###### make code that checks if needed components are precent in components list #########
#asdf = ['bottomCover_pickUp','bottomCover_assemble','PCB_pickUp', 'PCB_assemble', 'topCover_pickUp', 'topCover_assemble'] # 
#ActionClient.call_server(asdf)
#Phone.helloBaxter('assemble')

#ActionClient.cancel_goal()
#print 'cancel'
#print 'continue'
#ActionClient.continue_goal()
