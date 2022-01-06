#! /usr/bin/env python


import rospy
import actionlib
import ik_client_example
from baxter_tools.msg import assemblyAction, assemblyFeedback, assemblyResult
import vision
import sys
sys.path.append('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/SpeechRecognitionGoogle')
import talk


class ActionServer:
	def __init__(self):
                # initialize and start the action server
		self.server = actionlib.SimpleActionServer('assembly', assemblyAction, self.execute, False)
		self.server.start()

        #function to execute when a goal is recieved
	def execute(self, goal):
                #set up variables
		success = True
		last_component_installed = ''
		feedback = assemblyFeedback()
		result = assemblyResult()

    		#take image of workspace
		vision.take_image()

		#run the component regonition form vision.py
		component = vision.componentRegonition()
		componentPresent = True

		#set baxter face to standard face
		vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/face.png')

		# checks if bottom cover is missing and needed for the goal.
		if component[1] == 'missing' and  'bottomCover_pickUp' in goal.components_needed:
                        # as user for help with the bottom cover
			talk.talk('Bottom cover is missing please place Bottom cover in fixture')
			componentPresent = False
			# shows bottom cover on screen
			vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/bottomcover.png')
				
		


                # checks if top cover is missing and a random color top cover is need for the goal
		if component[0] == 'missing' and 'topCover_pickUp' in goal.components_needed:
                        #asks for help with missing top cover
			componentPresent = False			
			talk.talk('Top cover is missing please place Top cover in fixture')
			vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/topcover.png')
			
                # checks if white top cover is missing and needed
		if component[0] != 'whiteTopCover' and 'whitetopCover_pickUp' in goal.components_needed:
			componentPresent = False
			talk.talk('White top cover is missing please place a white top cover in fixture')
			vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/topcover.png')
			


		# checks if blue top cover is missing and needed
		if component[0] != 'blueTopCover' and 'bluetopCover_pickUp' in goal.components_needed:
			componentPresent = False			
			talk.talk('Blue top cover is missing please place a blue top cover in fixture')
			vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/topcover.png')


			
                # checks if black top cover is missing and needed
		if  component[0] != 'blackTopCover' and 'blacktopCover_pickUp' in goal.components_needed:
			componentPresent = False			
			talk.talk('Black top cover is missing please place a black top cover in fixture')
			vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/topcover.png')


                # checks if PCB is missing and needed
		if component[2] == 'missing' and  'PCB_pickUp' in goal.components_needed:
			talk.talk('PCB is missing please place PCB in fixture')
			componentPresent = False
			vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/pcb.png')
			
		
                # if no components were missing starts the assembly
		if componentPresent == True:
                        #set baxters face to standard face
			vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/face.png')

			#loop through goal components list
			for i in range(0,int(len(goal.components_needed))):
                                # check if the server is preempted (done using the cancel goal in action client)
				if self.server.is_preempt_requested():
					self.server.set_preempted(last_component_installed)
					success = False
					break

				# checks if component in list is bottomcover pick up
				if goal.components_needed[i] == 'bottomCover_pickUp':
                                        #uses ik_client_example script to pick up bottom cover
					ik_client_example.bottom_cover_pickUp()
					# sets last installed component to bottom cover picked up
					last_component_installed = 'bottomCover_pickUp'

                                # same as previous but for bottom cover assemble
				elif goal.components_needed[i] == 'bottomCover_assemble':
					ik_client_example.bottom_cover_assemble()
					last_component_installed = 'bottomCover_assemble'

                                # same as previous but for PCB pick up
				elif goal.components_needed[i] == 'PCB_pickUp':
					ik_client_example.PCB_pickUp()
					last_component_installed = 'PCB_pickUp'

                                # same as previous but for PCB assembly
				elif goal.components_needed[i] == 'PCB_assemble':
					ik_client_example.PCB_assemble()
					last_component_installed = 'PCB_assemble'

                                # checks if components in list is fuse
				elif goal.components_needed[i] == 'fuse':
					#points at the fuse
					ik_client_example.pointAt('fuse')
					#shows how to install fuse on screen
					vision.send_image('/home/jimmi/ros_ws/src/baxter_tools/scripts/P5-Baxter/Baxter/img/pcbInstall0.png')

					#sets last component installed to fuse
					last_component_installed = 'fuse'
					# sets feedback
					feedback.last_component_installed = last_component_installed
					# publishes feedback
					self.server.publish_feedback(feedback)
					# asks for help installing the fuse
					talk.talk('Please install the fuse as seen on the image displayed on screen')
					# preemptes the server to cancel the goal and wait for fuse to be installed
					self.server.set_preempted(last_component_installed)

                                # checks if component in list is a top cover (color can be either not specified, white, black or blue)
				elif goal.components_needed[i] == 'topCover_pickUp' or goal.components_needed[i] == 'blacktopCover_pickUp' or goal.components_needed[i] == 'whitetopCover_pickUp' or goal.components_needed[i] == 'bluetopCover_pickUp':
                                        # uses ik_client_example script to pick up top cover
                                        ik_client_example.top_cover_pickUp()
                                        # sets last component installed to top cover
					last_component_installed = 'topCover_pickUp'

                                # same as above but with top cover assemble. (does not need specified color)
				elif goal.components_needed[i] == 'topCover_assemble':
					ik_client_example.top_cover_assemble()
					last_component_installed = 'topCover_assemble'
				
				# checks if this is last loop through the goal list.
				if i == int(len(goal.components_needed))-1:
					talk.talk("finished assembly")

                                # sets feedback to the last component installed
				feedback.last_component_installed = last_component_installed

				#publish the feedback
				self.server.publish_feedback(feedback)

				# append the last component installed to the result list.
				result.components_installed.append(last_component_installed)
				#time.sleep(1)
			#checks if assembly is finished correctly (tror ikke det bliver brugt)
			if success:
                                #sends the goal result
				self.server.set_succeeded(result)


if __name__ == '__main__':
  rospy.init_node('action_server')
  s = ActionServer()
  rospy.spin()



