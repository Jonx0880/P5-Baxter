#! /usr/bin/env python

import rospy
import actionlib

from baxter_tools.msg import assemblyAction, assemblyGoal


def feedback_cb(msg):
	print 'feedback recieved', msg

def call_server(component):
	client = actionlib.SimpleActionClient('assembly', assemblyAction)
	print'1'
	client.wait_for_server()
	print'2'
	goal = assemblyGoal()
	goal.components_needed.append(component)
	
	client.send_goal(goal, feedback_cb=feedback_cb)

	client.wait_for_result()

	result = client.get_result()

	return result

#if __name__ == '__main__':




