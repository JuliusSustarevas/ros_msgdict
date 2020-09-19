# ros_msgdict

msgdict2yaml

yaml2msgdict

msgdict2params

params2msgdict

complex_dict = dict()
complex_dict["My_fav_robot_traj"] = RobotTrajectory()
complex_dict["DA_best_colour"] = ObjectColor()
complex_dict["I_always_forget_this_request"] = GetPositionIKRequest()
complex_dict["But I never forget this response"] = ListRobotStatesInWarehouseResponse()

msg2param.msg_dict2yaml(complex_dict, path_save_complex)
path_save_complex_params = msg2param.yaml2msg_dict(path_save_complex)
if cmp(path_save_complex_params, complex_dict) == 0:
print("Complex dicts are identical")
