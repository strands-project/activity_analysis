#!/usr/bin/env python
# encoding: utf-8

import rospy
import std_msgs.msg
from strands_perception_people_msgs.msg import PedestrianLocations

class EngagementChecker:
    def __init__(self, name='engagement_checker'):
        rospy.init_node(name)

        self.detections = dict()

        pub_topic = rospy.get_param("~detections",name+"/engaged")
        self.threshold = rospy.get_param("~threshold", 20)

        self.pub = rospy.Publisher(pub_topic,std_msgs.msg.Bool,queue_size=100)
        rospy.Subscriber('/pedestrian_localisation/localisations', PedestrianLocations, self.callback_pose)

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
            if data.distances[i]<1.3:
                self.detections[data.ids[i]] += 1
                rospy.loginfo('found one! %s %s',data.ids[i],self.detections[data.ids[i]])
            else:
                self.detections[data.ids[i]] = 0

            if self.detections[data.ids[i]] == self.threshold:
                result = std_msgs.msg.Bool()
                result.data = True
                self.pub.publish(result)

if __name__ == '__main__':
    ec = EngagementChecker()
    rospy.loginfo('Engagement checker running ...')
    rospy.spin()
