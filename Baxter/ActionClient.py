#! /usr/bin/env python

import rospy
import actionlib

from baxter_tools.msg import assemblyAction, assemblyGoal


def feedback_cb(msg):
	print 'feedback recieved', msg

def call_server():
	client = actionlib.SimpleActionClient('assembly', assemblyAction)
	print'1'
	client.wait_for_server()
	print'2'
	goal = assemblyGoal()
	goal.components_needed.append('bottomCover')
	goal.components_needed.append('PCB')
	

	client.send_goal(goal, feedback_cb=feedback_cb)

	client.wait_for_result()

	result = client.get_result()

	return result

if __name__ == '__main__':
	try:
		rospy.init_node('action_client')
		result = call_server()
		print 'The result is: ', result
	except rospy.ROSInterruptException as e:
		print 'something went wrong with: ', e



