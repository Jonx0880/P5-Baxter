#! /usr/bin/env python

import rospy
import actionlib
import time
from baxter_tools.msg import assemblyAction, assemblyGoal, assemblyFeedback
import sys
sys.path.append('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/SpeechRecognitionGoogle')
import talk


goal = assemblyGoal()
feedback = assemblyFeedback()

client = actionlib.SimpleActionClient('assembly', assemblyAction)

def feedback_cb(msg):
	print 'feedback recieved', msg
	feedback.last_component_installed = msg
	string = str(feedback.last_component_installed)
	string = string.split()[-1]
	if string == 'Missing':
		print 'Component missing'


def call_server(components = []):
	print'1'
	goal.components_needed = []
	feedback.last_component_installed = ''
	client.wait_for_server()
	print'2'
	
	for i in range (0,len(components)):
		goal.components_needed.append(components[i])
#	print goal
	client.send_goal(goal, feedback_cb=feedback_cb)

def get_result():
	client.wait_for_result()
	result = client.get_result()
	return result

def cancel_goal():
	client.cancel_goal()
	feedback.last_component_installed = 'Waiting'

def continue_goal():
	talk.talk('phoneAssembly')
	print 'goal1'	
	print goal.components_needed
	print feedback.last_component_installed
	string = str(feedback.last_component_installed)
	print string
	if string != '':
		string = string.split()[-1]
	print string
#	print goal.components_needed.index(string)
#	print goal.components_needed[0]
#	print goal.components_needed[0+1]
	print feedback.last_component_installed
	print goal.components_needed
	if string in goal.components_needed:
		
		goal.components_needed = goal.components_needed[goal.components_needed.index(string)+1:]
		print 'sending goal'
		client.send_goal(goal, feedback_cb=feedback_cb)
	else:
		print 'not sending goal'
		client.send_goal(goal, feedback_cb=feedback_cb)

def current_action():
	print feedback.last_component_installed
	string = str(feedback.last_component_installed)
	if string != '':
		string = string.split()[-1]
	try:
		if string == '' and goal.components_needed[0] == 'bottomCover_pickUp': 
			talk.talk('bottomCover_pickUp')
		print string
	except:
		talk.talk('not doing anything')

	if string == 'fuse':
		talk.talk('waiting for fuse to be installed')	
	elif string in goal.components_needed:
		talk.talk(str(goal.components_needed[goal.components_needed.index(string)+1]))

#if __name__ == '__main__':

#rospy.init_node('action_client')
#call_server()
#time.sleep(10)
#cancel_goal()
#print get_result()
