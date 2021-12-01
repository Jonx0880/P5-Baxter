#!/usr/bin/env python

import Phone
import rospy

try:
	rospy.init_node('action_client')
except rospy.ROSInterruptException as e:
	print 'something went wrong with: ', e
Phone.helloBaxter('assemble')


