#! /usr/bin/env python


import rospy
import actionlib
import ik_client_example
from baxter_tools.msg import assemblyAction, assemblyFeedback, assemblyResult
import vision

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
    		print goal
		vision.take_image()
		component = vision.componentRegonition()
		componentPresent = True
		vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/face.png')
		if component[1] == 'missing' and  'bottomCover_pickUp' in goal.components_needed:
			print 'Bottom cover is missing, place Bottom cover in fixture'
			componentPresent = False
			vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/bottomcover.png')
			
		


		if component[0] == 'missing' and  'topCover_pickUp' in goal.components_needed:
			print 'Top cover is missing, place Top cover in fixture'
			componentPresent = False
			vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/topcover.png')
			
		if component[2] == 'missing' and  'PCB_pickUp' in goal.components_needed:
			print 'PCB is missing, place PCB in fixture or assemble without PCB'
			componentPresent = False
			vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/pcb.png')
			
		

		if componentPresent == True:
			vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/face.png')
			for i in range(0,int(len(goal.components_needed))):
				if self.server.is_preempt_requested():
					self.server.set_preempted(last_component_installed)
					success = False
					break
				if goal.components_needed[i] == 'bottomCover_pickUp':
					ik_client_example.bottom_cover_pickUp()
					last_component_installed = 'bottomCover_pickUp'
			
				elif goal.components_needed[i] == 'bottomCover_assemble':
					ik_client_example.bottom_cover_assemble()
					last_component_installed = 'bottomCover_assemble'
			
				elif goal.components_needed[i] == 'PCB_pickUp':
					ik_client_example.PCB_pickUp()
					last_component_installed = 'PCB_pickUp'

				elif goal.components_needed[i] == 'PCB_assemble':
					ik_client_example.PCB_assemble()
					last_component_installed = 'PCB_assemble'

				elif goal.components_needed[i] == 'fuse':
					#ik_client_example.pointAt('fuse')
					ik_client_example.pointAt('fuse')
					vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/pcbInstall0.png')
					last_component_installed = 'fuse'
					feedback.last_component_installed = last_component_installed
					self.server.publish_feedback(feedback)
					print 'would you install the fuses pls'
					self.server.set_preempted(last_component_installed)

				elif goal.components_needed[i] == 'topCover_pickUp':
					ik_client_example.top_cover_pickUp()
					last_component_installed = 'topCover_pickUp'

				elif goal.components_needed[i] == 'topCover_assemble':
					ik_client_example.top_cover_assemble()
					last_component_installed = 'topCover_assemble'

				feedback.last_component_installed = last_component_installed
				self.server.publish_feedback(feedback)
				result.components_installed.append(last_component_installed)
				#time.sleep(1)
			if success:
			
				self.server.set_succeeded(result)


if __name__ == '__main__':
  rospy.init_node('action_server')
  s = ActionServer()
  rospy.spin()



