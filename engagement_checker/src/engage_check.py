#!/usr/bin/env python
# encoding: utf-8

import roslib
import numpy as np
roslib.load_manifest('engagement_checker')
import rospy
import tf

from strands_perception_people_msgs.msg import PedestrianLocations

LAST = rospy.Time(0)

def callback_pose(data):
    global A
    if len(data.ids)>0:
	x = range(100)
	for i in list(data.ids):
	    x.remove(i)
	for i in x:
	    A[i] = 0

	for i in range(len(data.distances)):
	    if data.distances[i]<1.3:
		A[data.ids[i]] += 1
		print 'found one!',data.ids[i],A[data.ids[i]] 
	    else:
		A[data.ids[i]] = 0

	    if A[data.ids[i]] == 10:
		print 'stop robot for',data.ids[i]
	    if A[data.ids[i]] == 20:
		print data.ids[i],'is interested'
			
    	#print A

class Kinect:

    def __init__(self, name='kinect_listener'):
        rospy.init_node(name, anonymous=True)



    def get_posture(self):
	global A
	A = {}
	for i in range(100):
	    A[i] = 0
 
    	rospy.Subscriber('/pedestrian_localisation/localisations', PedestrianLocations, callback_pose)
    	r = rospy.Rate(15) # 120hz				# set the ROS rate

        while not rospy.is_shutdown():
	    
	    """
	    if result[0] != 0: 					# This is set if a user is interested
		pan = np.arctan2(result[1][1], result[1][0])*180/np.pi
		tilt = np.arctan2(result[1][2], result[1][0])*180/np.pi
		print self.user,result[0],pan,tilt
		# Head tracker
	    else:
	    	self.user += 1
	    	if self.user == 9:
			self.user = 1
	    """
	    r.sleep()
	   


if __name__ == '__main__':

    kin = Kinect()
    print('Engagement checker running ...')
    #espeak.synth("Hello.")


# Get values                                                                                                                                         
     
#    for i in range 10:
    kin.get_posture()
