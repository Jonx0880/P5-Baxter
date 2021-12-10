#! /usr/bin/env python

import rospy
import actionlib
import time

from baxter_tools.msg import assemblyAction, assemblyGoal, assemblyFeedback


goal = assemblyGoal()
feedback = assemblyFeedback()
def feedback_cb(msg):
	print 'feedback recieved', msg
	feedback.last_component_installed = msg
	string = str(feedback.last_component_installed)
	string = string.split()[-1]
	if string == 'Missing':
		print 'Component missing'

client = actionlib.SimpleActionClient('assembly', assemblyAction)
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

def continue_goal():
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



#if __name__ == '__main__':

#rospy.init_node('action_client')
#call_server()
#time.sleep(10)
#cancel_goal()
#print get_result()
