cmake_minimum_required(VERSION 2.8.3)

project(ros_msgdict)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
)

#This will set it up in python path
catkin_python_setup()

catkin_package(
  LIBRARIES ${PROJECT_NAME}
  CATKIN_DEPENDS rospy std_msgs
)
