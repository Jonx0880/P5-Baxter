#! /usr/bin/env python

import rospy
import actionlib
import time
from baxter_tools.msg import assemblyAction, assemblyGoal, assemblyFeedback
import sys
sys.path.append('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/SpeechRecognitionGoogle')
import talk


#set up variables for goal and feedback
goal = assemblyGoal()
feedback = assemblyFeedback()

#initialize the action client
client = actionlib.SimpleActionClient('assembly', assemblyAction)

# function for handeling the feedback recieved from action server
def feedback_cb(msg):
	print 'feedback recieved', msg
	feedback.last_component_installed = msg
	string = str(feedback.last_component_installed)
	string = string.split()[-1]
	if string == 'Missing':
		print 'Component missing'

# function for sending a goal to the action server.
def call_server(components = []):
        #uses talk script to say out loud that it will atempt to assemble a phone
	talk.talk('phoneAssembly')

	goal.components_needed = []
	feedback.last_component_installed = ''
	client.wait_for_server()

	#take input data from components list and add to the goal list.
	for i in range (0,len(components)):
		goal.components_needed.append(components[i])

        #sends goal to action server
	client.send_goal(goal, feedback_cb=feedback_cb)

#function for reading the result of a goal after its completed
def get_result():
	client.wait_for_result()
	result = client.get_result()
	return result

#function for canceling a goal
def cancel_goal():
	client.cancel_goal()
	feedback.last_component_installed = 'Waiting'

#function for continueing a cancled goal
def continue_goal():
	print goal.components_needed
	print feedback.last_component_installed

	# make a string of the last feedback recieved and splice it to only keep the last word
	string = str(feedback.last_component_installed)
	if string != '':
		string = string.split()[-1]

        # check if the last word in the last feedback is in the goal list
	if string in goal.components_needed:
                # last word of the feedback is in the goal list, remove it and everything before it from the goal list.
		goal.components_needed = goal.components_needed[goal.components_needed.index(string)+1:]
		print 'sending goal'
		# send the new goal list to action server
		client.send_goal(goal, feedback_cb=feedback_cb)
	else:
		print 'not sending goal'
		client.send_goal(goal, feedback_cb=feedback_cb)

# function for checing what baxter is currently doing
def current_action():
	print feedback.last_component_installed

	#splice the feedback like in function above
	string = str(feedback.last_component_installed)
	if string != '':
		string = string.split()[-1]


	try:
		if string == '' and goal.components_needed[0] == 'bottomCover_pickUp':
                # if the feedback is empty and a bottomCover_pickUp is in the goal list, the baxter is currently picking up the bottom cover
			talk.talk('bottomCover_pickUp')
		print string
	except:
		talk.talk('not doing anything')

	if string == 'fuse':
		talk.talk('waiting for fuse to be installed')	
	elif string in goal.components_needed:
                # says which action is currently being performed by baxter (eccept fuse and bottomcover pickup
		talk.talk(str(goal.components_needed[goal.components_needed.index(string)+1]))

#if __name__ == '__main__':

#rospy.init_node('action_client')
#call_server()
#time.sleep(10)
#cancel_goal()
#print get_result()
