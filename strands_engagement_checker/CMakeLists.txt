cmake_minimum_required(VERSION 2.8.3)
project(strands_engagement_checker)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  bayes_people_tracker
)

###################################
## catkin specific configuration ##
###################################
catkin_package(
  CATKIN_DEPENDS rospy std_msgs bayes_people_tracker
)

#############
## Install ##
#############

install(PROGRAMS
  scripts/engage_check.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
