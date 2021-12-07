#! /usr/bin/env python


import rospy
import actionlib
import ik_client_example
from baxter_tools.msg import assemblyAction, assemblyFeedback, assemblyResult

class ActionServer:
	def __init__(self):
		self.server = actionlib.SimpleActionServer('assembly', assemblyAction, self.execute, False)
		self.server.start()
		print'2'

	def execute(self, goal):
	# Do lots of awesome groundbreaking robot stuff here
		success = True
		print'1'
		last_component_installed = ''
		feedback = assemblyFeedback()
		result = assemblyResult()
		rate = rospy.Rate(1)
    		print goal
		for i in range(0,int(len(goal.components_needed))):
			if self.server.is_preempt_requested():
				self.server.set_preempted()
				success = False
				break
			elif goal.components_needed[0] == 'bottomCover':
				ik_client_example.bottom_cover_assemble()
				last_component_installed = 'bottomCover'
			
			elif goal.components_needed[i] == 'PCB':
				ik_client_example.PCB_assemble()
				last_component_installed = 'PCB'

			elif goal.components_needed[i] == 'topCover':
				ik_client_example.top_cover_assemble()
				last_component_installed = 'topCover'


			feedback.last_component_installed = last_component_installed
			result.components_installed.append(last_component_installed)
			rate.sleep()
		if success:
			
			self.server.set_succeeded(result)


if __name__ == '__main__':
  rospy.init_node('action_server')
  s = ActionServer()
  rospy.spin()


