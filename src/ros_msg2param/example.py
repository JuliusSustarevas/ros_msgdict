#!/usr/bin/env python
import rospy
import rosparam
import actionlib
import rospkg
from rospy_message_converter import message_converter
import msgdict
from moveit_msgs.msg import RobotTrajectory, ObjectColor
from moveit_msgs.srv import GetPositionIKRequest, ListRobotStatesInWarehouseResponse

# Setup some paths to test
rospack = rospkg.RosPack()
path_load = rospack.get_path('ros_msgdict')+"/res/params_load.yaml"
path_save = rospack.get_path('ros_msgdict')+"/res/params_save.yaml"
path_save_complex = rospack.get_path(
    'ros_msgdict')+"/res/params_save_complex.yaml"


# Loading/saving msg_dict to yaml
print("Loading msg_dict...")
loaded_params = msgdict.yaml2msgdict(path_load)
for key in loaded_params.keys():
    print(loaded_params[key].__class__)

print("Saving msg_dict...")
msgdict.msgdict2yaml(loaded_params, path_save)
saved_params = msgdict.yaml2msgdict(path_save)
if cmp(loaded_params, saved_params) == 0:
    print("Params loaded/saved from yaml are identical")

# Loading/saving Complex messages, responses and requests are supported too
print("Loading/Saving complex messages, responses and requests")
complex_dict = dict()
complex_dict["My_fav_robot_traj"] = RobotTrajectory()
complex_dict["DA_best_colour"] = ObjectColor()
complex_dict["I_always_forget_this_request"] = GetPositionIKRequest()
complex_dict["But I never forget this response"] = ListRobotStatesInWarehouseResponse()

msgdict.msgdict2yaml(complex_dict, path_save_complex)
path_save_complex_params = msgdict.yaml2msgdict(path_save_complex)
if cmp(path_save_complex_params, complex_dict) == 0:
    print("Complex dicts are identical")

# Loading saveing msg_dict to param server
print("Saving msg_dict to param server...")
rospy.init_node("test")
msgdict.msgdict2params(complex_dict, "~namespace")
#
print("Loading msg_dict to param server...")
read_params = msgdict.params2msgdict("~namespace")
if cmp(complex_dict, read_params) == 0:
    print("msg_dict loaded/saved from param server are identical")
