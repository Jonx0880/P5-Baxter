#!/usr/bin/env python

import time

import rospy

import numpy as np

import math as m

# http://api.rethinkrobotics.com/baxter_interface/html/index.html
import baxter_interface

# https://github.com/ricardodeazambuja/BaxterRobotUtils/blob/master/ik_client.py
from ik_client import ik_service

import time

def euler_to_quaternion(roll, pitch, yaw): #x, y, z

        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

        return [qx, qy, qz, qw] 

class ik_move:
	def __init__(self,limb , PosX, PosY, PosZ, RotX, RotY, RotZ, RotW):
		#	limb = 'left'
		# Receives a list of poses / gripper commands
		ik = ik_service(limb, speed=0.3)
		#print (euler_to_quaternion(0,0,20))
	
		# Creates two empty lists
		movements = []
		gripper_state = []
		
		# The values can be easily copied from the command:
		
		# rostopic echo /robot/limb/<left/right>/endpoint_state/pose -n 1 -p
		
		# Store position in list
		movements.append([PosX,PosY,PosZ,
				   RotX,RotY,RotZ,RotW])
		
		
		
		#
		# Goes through the lists commanding the robot
		#
		
		for mv_i in movements:
		    if not ik.ik_call(mv_i[:3], mv_i[3:]):
		        ik.ik_move_to(timeout=15)
		    else:
		        print ("IK returned an error...")
class gripper:
	def __init__(self,limb,grip):
		gripper_force_threshold = 30 # in percentage
		gripper_vacuum_threshold = 18 # in percentage

	
		# checks which gripper type is attached to the given limb
		gripper = baxter_interface.Gripper(limb)
	
		print ("Using the " + gripper.type() + " gripper.")
	
		if gripper.type() == 'electric':
			print ("Calibrating the electric gripper")
			gripper.calibrate()
			gripper.set_holding_force(gripper_force_threshold)
		else:
			gripper.set_vacuum_threshold(gripper_vacuum_threshold)
			gripper.set_blow_off(0.4)
	
		print ("Gripper parameters: ",gripper.parameters())
		time.sleep(0.5)
		if grip == 1:
			gripper.close(False,100)	
		elif grip == 0:
			gripper.open()

def PCB_assemble():
	#        limb, gripper, x, y, z, rotx, roty, rotz, rotw
	ik_move('left', 0.668666615156,0.159488855161,0.10,0.0,1.0,0.0,0.0) # Above pcb
	ik_move('left', 0.660130532232,0.160065985279,0.0380676342796,0,1.0,0,0) # on pcb ready to pick up
	gripper('left',1)	
	time.sleep(0.3)
	ik_move('left', 0.668666615156,0.159488855161,0.10,0.0,1.0,0.0,0.0) # above pcb
	ik_move('left', 0.565135933659,-0.0635259045333,0.10,0.67,0.740,0.0,0.0) # above assembly (PCB)
	ik_move('left', 0.564383557023,-0.045235812403,0.0623267765158,0.713801016942,0.693439129467,-0.0608133789334,0.0770195746494) # assembly (PCB)
	ik_move('left', 0.564383557023,-0.037235812403,0.0483267765158,0.713801016942,0.693439129467,-0.0608133789334,0.0770195746494) # assembly2(PCB)
	#time.sleep(0.5)
	gripper('left',0)
	#time.sleep(1)
	ik_move('left', 0.565135933659,-0.0635259045333,0.10,0.67,0.740,0.0,0.0) # above assembly (PCB)
	#time.sleep(1)
	ik_move('left', 0.68329649123,0.18177703246,0.246791880359,0.663637947219,0.747921095688,-0.0125461365671,-0.00642682600638) # not in the way


def top_cover_assemble():

	ik_move('left' ,0.720810785058,-0.0669336354737,0.10,0.721748800287,0.691977710377,0.0,0.0) #above top cover (PCB)
	ik_move('left', 0.720810785058,-0.0669336354737,0.0453176457979,0.672713129189,0.739894165709,-0.000215698722715,-0.00369091320901) # on topCover ready to pick up
	gripper('left',1)
	time.sleep(0.3)
	ik_move('left' ,0.720810785058,-0.0669336354737,0.10,0.721748800287,0.691977710377,0.0,0.0) #above top cover (PCB)
	ik_move('left', 0.565135933659,-0.059259045333,0.10,0.67,0.740,0.0,0.0) # above assembly (Topcover)
	ik_move('left', 0.559376469705,-0.0509358172209,0.0516951628245,0.677452757938,0.735101133829,-0.0153609097875,0.0211689927869) # assembly (Topcover)
	gripper('left',0)
	ik_move('left', 0.565135933659,-0.05000259045333,0.10,0.67,0.740,0.0,0.0) # above assembly (Topcover)
	ik_move('left',0.5688646857,-0.532649892752,0.0541724278493,0.977369436987,0.104709231467,0.0319209765893,-0.181013844063) # push
	ik_move('left', 0.565135933659,-0.05000259045333,0.10,0.67,0.740,0.0,0.0) # above assembly (Topcover)
	ik_move('left', 0.68329649123,0.18177703246,0.246791880359,0.663637947219,0.747921095688,-0.0125461365671,-0.00642682600638) # not in the way

	
def bottom_cover_assemble():
	ik_move('right', 0.763522888409,-0.204866932424,0.10,-0.0380316529013,0.999233981816,-0.00382488902191,0.00839125651855) # above bottom cover
	gripper('right',0)
	ik_move('right', 0.763522888409,-0.204866932424,-0.0263100533637,-0.0380316529013,0.999233981816,-0.00382488902191,0.00839125651855) #on bottom cover ready to pick up
	gripper('right',1)
	time.sleep(1)
	ik_move('right', 0.763522888409,-0.204866932424,0.10,-0.0380316529013,0.999233981816,-0.00382488902191,0.00839125651855) # above bottom cover
	ik_move('right', 0.572835700064,-0.0190278391633,0.10,0.682854617314,0.729508427933,-0.0127610687722,0.0369348116492) # above assembly (BottomCover)
	ik_move('right', 0.572835700064,-0.0190278391633,-0.0190634955226,0.682854617314,0.729508427933,-0.0127610687722,0.0369348116492) # assembly (BottomCover)
	gripper('right',0)
	ik_move('right', 0.572835700064,0.0240278391633,0.10,0.682854617314,0.729508427933,-0.0127610687722,0.0369348116492) # above assembly (BottomCover)
	ik_move('right',0.561262336509,-0.546388798027,0.0538522879858,0.978079507015,0.0839344049776,0.0361222833187,-0.187111395339) # not in the way


#bottom_cover_assemble()
#PCB_assemble()
#top_cover_assemble()
ik_move('left', 0.5551010122,-0.0425577565842,0.471185105074,0.999774873809,-0.01936871865,-0.00137352179243,0.0085538222863) # camera position

#0.565087287226,-0.0306361978582,0.0442198731717,0.608885219703,0.712085248122,-0.223134576498,0.269080563039 # position for holding down pcb while mounting fuse furthest from left gripper

#,0.557048197213,-0.0195353149855,0.0441155470975,0.582978888627,0.733247775487,-0.209561432909,0.280298628244 # position for holding down pcb while mounting fuse closest to left gripper




#ik_move('left', 0.564383557023,-0.037235812403,0.0483267765158,0.713801016942,0.693439129467,-0.0608133789334,0.0770195746494)


print (euler_to_quaternion(0,0,0))



