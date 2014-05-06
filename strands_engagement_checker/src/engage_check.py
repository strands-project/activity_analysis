#!/usr/bin/env python
# encoding: utf-8

import rospy
import std_msgs.msg
from strands_perception_people_msgs.msg import PedestrianLocations

class EngagementChecker:
    def __init__(self, name='engagement_checker'):
        rospy.init_node(name)

        self.detections = {}
        for i in range(100): #TODO: Find nicer solution
            self.detections[i] = 0

        pub_topic = rospy.get_param("~detections",name+"/engaged")
        self.pub = rospy.Publisher(pub_topic,std_msgs.msg.Bool,queue_size=100)
        rospy.Subscriber('/pedestrian_localisation/localisations', PedestrianLocations, self.callback_pose)

    def callback_pose(self, data):
        if len(data.ids)>0:
            x = range(100)
    	for i in list(data.ids):
    	    x.remove(i)
    	for i in x:
    	    self.detections[i] = 0

        for i in range(len(data.distances)):
            if data.distances[i]<1.3:
                self.detections[data.ids[i]] += 1
                rospy.loginfo('found one! %s %s',data.ids[i],self.detections[data.ids[i]])
            else:
                self.detections[data.ids[i]] = 0

            if self.detections[data.ids[i]] == 20:
                result = std_msgs.msg.Bool()
                result.data = True
                self.pub.publish(result)


if __name__ == '__main__':

    kin = EngagementChecker()
    print('Engagement checker running ...')
    kin.get_posture()
    rospy.spin()
