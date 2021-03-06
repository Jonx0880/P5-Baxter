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

# function converting from cartecian(euler) orientation to quaternions
def euler_to_quaternion(roll, pitch, yaw): #x, y, z

        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

        return [qx, qy, qz, qw] 

# class for moving baxter (should have been a function)
class ik_move:
        # needs an input of which limb to move, and which coordinates and orientation to move to
	def __init__(self,limb , PosX, PosY, PosZ, RotX, RotY, RotZ, RotW):
                # makes an ik_service object from the ik_client script. including which limb used and how fast it should move
		ik = ik_service(limb, speed=0.3)
		
	
		# Creates empty lists
		movements = []
		
		# The values for baxters current position can be found from the command:
		# rostopic echo /robot/limb/<left/right>/endpoint_state/pose -n 1 -p
		
		# Store position and orientation in list
		movements.append([PosX,PosY,PosZ,
				   RotX,RotY,RotZ,RotW])
		
		
		
		# Goes through the list commanding the robot
		for mv_i in movements:
		    if not ik.ik_call(mv_i[:3], mv_i[3:]):
		        ik.ik_move_to(timeout=15)
		    else:
		        print ("IK returned an error...")

#class for controling the gripper (should have been a function)
class gripper:
        #takes input of which limb, and 1 or 0 if it should be closed or opened
	def __init__(self,limb,grip):
                #sets parameters
		gripper_force_threshold = 30 # in percentage
		gripper_vacuum_threshold = 18 # in percentage

	
		# checks which gripper type is attached to the given limb
		gripper = baxter_interface.Gripper(limb)

                # checks the gripper type
		if gripper.type() == 'electric':
                        # if electric gripper is used calibarate it
			print ("Calibrating the electric gripper")
			gripper.calibrate()
			gripper.set_holding_force(gripper_force_threshold)
		else:
                        # set vacum gripper parameters
			gripper.set_vacuum_threshold(gripper_vacuum_threshold)
			gripper.set_blow_off(0.4)
	
		# sleep 0.5 seconds (vacum gripper does not work if we dont wait)
		time.sleep(0.5)
		# open or close based on input. (0 or 1)
		if grip == 1:
			gripper.close(False,50)	
		elif grip == 0:
			gripper.open()
def PCB_pickUp():
	ik_move('left', 0.668666615156,0.159488855161,0.10,0.0,1.0,0.0,0.0) # Above pcb
	ik_move('left', 0.660130532232,0.160065985279,0.0380676342796,0,1.0,0,0) # on pcb ready to pick up
	gripper('left',1) #close the left gripper	
	time.sleep(0.3)
	ik_move('left', 0.668666615156,0.159488855161,0.10,0.0,1.0,0.0,0.0) # above pcb

def PCB_assemble():
	#        limb, gripper, x, y, z, rotx, roty, rotz, rotw

	ik_move('left', 0.565135933659,-0.0635259045333,0.10,0.67,0.740,0.0,0.0) # above assembly (PCB)
	ik_move('left', 0.564383557023,-0.045235812403,0.0623267765158,0.713801016942,0.693439129467,-0.0608133789334,0.0770195746494) # assembly (PCB)
	ik_move('left', 0.564383557023,-0.037235812403,0.0483267765158,0.713801016942,0.693439129467,-0.0608133789334,0.0770195746494) # assembly2(PCB)
	#time.sleep(0.5)
	gripper('left',0) # open the left gripper
	#time.sleep(1)
	ik_move('left', 0.565135933659,-0.0635259045333,0.10,0.67,0.740,0.0,0.0) # above assembly (PCB)
	#time.sleep(1)
	ik_move('left', 0.68329649123,0.18177703246,0.246791880359,0.663637947219,0.747921095688,-0.0125461365671,-0.00642682600638) # not in the way

def top_cover_pickUp():
	ik_move('left' ,0.720810785058,-0.0669336354737,0.10,0.721748800287,0.691977710377,0.0,0.0) #above top cover (PCB)
	ik_move('left', 0.720810785058,-0.0669336354737,0.0453176457979,0.672713129189,0.739894165709,-0.000215698722715,-0.00369091320901) # on topCover ready to pick up
	gripper('left',1)
	time.sleep(0.3)
	ik_move('left' ,0.720810785058,-0.0669336354737,0.10,0.721748800287,0.691977710377,0.0,0.0) #above top cover (PCB)

def top_cover_assemble():
	ik_move('left', 0.565135933659,-0.059259045333,0.10,0.67,0.740,0.0,0.0) # above assembly (Topcover)
	ik_move('left', 0.559376469705,-0.0509358172209,0.0516951628245,0.677452757938,0.735101133829,-0.0153609097875,0.0211689927869) # assembly (Topcover)
	gripper('left',0)
	ik_move('left', 0.565135933659,-0.05000259045333,0.10,0.67,0.740,0.0,0.0) # above assembly (Topcover)
	#ik_move('left',0.5688646857,-0.532649892752,0.0541724278493,0.977369436987,0.104709231467,0.0319209765893,-0.181013844063) # push
	ik_move('left', 0.565135933659,-0.05000259045333,0.10,0.67,0.740,0.0,0.0) # above assembly (Topcover)
	ik_move('left', 0.565135933659,-0.05000259045333,0.0474175991624,0.67,0.740,0.0,0.0) # push down (Topcover)
	ik_move('left', 0.565135933659,-0.05000259045333,0.10,0.67,0.740,0.0,0.0) # above assembly (Topcover)

	ik_move('left', 0.68329649123,0.18177703246,0.246791880359,0.663637947219,0.747921095688,-0.0125461365671,-0.00642682600638) # not in the way

def bottom_cover_pickUp():
	ik_move('right', 0.763522888409,-0.204866932424,0.10,-0.0380316529013,0.999233981816,-0.00382488902191,0.00839125651855) # above bottom cover
	gripper('right',0)
	ik_move('right', 0.763522888409,-0.204866932424,-0.0263100533637,-0.0380316529013,0.999233981816,-0.00382488902191,0.00839125651855) #on bottom cover ready to pick up
	gripper('right',1)
	time.sleep(1)
	ik_move('right', 0.763522888409,-0.204866932424,0.10,-0.0380316529013,0.999233981816,-0.00382488902191,0.00839125651855) # above bottom cover

def bottom_cover_assemble():

	ik_move('right', 0.572835700064,-0.0190278391633,0.10,0.682854617314,0.729508427933,-0.0127610687722,0.0369348116492) # above assembly (BottomCover)
	ik_move('right', 0.572835700064,-0.0190278391633,-0.0190634955226,0.682854617314,0.729508427933,-0.0127610687722,0.0369348116492) # assembly (BottomCover)
	gripper('right',0)
	ik_move('right', 0.572835700064,0.0240278391633,0.10,0.682854617314,0.729508427933,-0.0127610687722,0.0369348116492) # above assembly (BottomCover)
	ik_move('right',0.561262336509,-0.546388798027,0.0538522879858,0.978079507015,0.0839344049776,0.0361222833187,-0.187111395339) # not in the way

#def show_component():

def pointAt(component):
	if component == 'fuse':
		ik_move('left', 0.714024503234,0.110450093207,0.0686220852913,0.624882128713,0.743709436784,-0.182203629403,0.152382532747) # fuse pointing
	
	if component == 'bottom cover':
		ik_move('left', 0.767969058365,-0.188372769437,0.071732767529,0.93780123435,-0.268460881526,0.182275254927,0.123423382647) #top cover pointing
	if component == 'top cover':
		ik_move('left',0.698067200146,-0.0303753339945,0.0745926677905,0.958461162839,-0.193433938101,0.131825138203,0.162965161485) #top cover pointing

	if component == 'PCB':
		ik_move('left', 0.643554063898,0.182602030692,0.0816508803921,0.983731771394,-0.102194976263,0.108204942991,0.100596615694) #pcb pointing


#bottom_cover_assemble()
#PCB_assemble()
#top_cover_assemble()
def cameraPos():
	
	ik_move('left', 0.5551010122,-0.0425577565842,0.471185105074,0.999774873809,-0.01936871865,-0.00137352179243,0.0085538222863) # camera position
	ik_move('right',0.561262336509,-0.546388798027,0.0538522879858,0.978079507015,0.0839344049776,0.0361222833187,-0.187111395339) # not in the way



#0.565087287226,-0.0306361978582,0.0442198731717,0.608885219703,0.712085248122,-0.223134576498,0.269080563039 # position for holding down pcb while mounting fuse furthest from left gripper

#,0.557048197213,-0.0195353149855,0.0441155470975,0.582978888627,0.733247775487,-0.209561432909,0.280298628244 # position for holding down pcb while mounting fuse closest to left gripper




#ik_move('left', 0.564383557023,-0.037235812403,0.0483267765158,0.713801016942,0.693439129467,-0.0608133789334,0.0770195746494)


