#!/usr/bin/env python
# encoding: utf-8

import rospy
import std_msgs.msg
from strands_perception_people_msgs.msg import PedestrianLocations
from strands_perception_people_msgs.msg import HeadOrientations

class EngagementChecker:
    def __init__(self, name='engagement_checker'):
        rospy.init_node(name)

        self.detections = dict()

        pub_topic = rospy.get_param("~detections",name+"/engaged")
        self.threshold = rospy.get_param("~threshold", 20)

        self.pub = rospy.Publisher(pub_topic,std_msgs.msg.Bool,queue_size=1)
        rospy.Subscriber('/pedestrian_localisation/localisations', PedestrianLocations, self.callback_pose)
	rospy.Subscriber('/head_orientation/head_ori', HeadOrientations, self.callback_ori)

    def callback_pose(self, data):
        # Add new detections
        for idx in data.ids:
            if not idx in self.detections.keys():
                self.detections[idx] = 0

        # Remove old detections
        for idx in self.detections.keys():
            if not idx in data.ids:
                del(self.detections[idx])

        # Check for engagement
        for i in range(len(data.distances)):

            if data.distances[i]<1.3 and self.detections[data.ids[i]] >= self.threshold:
                result = std_msgs.msg.Bool()
                result.data = True
                self.pub.publish(result)
		print 'engaging with',data.ids[i]
            elif data.distances[i]<1.3 and self.detections[data.ids[i]] < self.threshold:
                self.detections[data.ids[i]] += 1
                rospy.logdebug('found person to probably engage with %s %s',data.ids[i],self.detections[data.ids[i]])
		print 'found person to probably engage with',data.ids[i],self.detections[data.ids[i]]
            else:
                self.detections[data.ids[i]] = 0


    def callback_ori(self, data):
	print data.angles


if __name__ == '__main__':
    ec = EngagementChecker()
    rospy.loginfo('Engagement checker running ...')
    rospy.spin()
