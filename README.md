# ros_msgdict

Have you ever wanted to parameterise your ROS application using ROS messages as parameters? Sure loading a yaml file with some nice strings and ints is nice, but what about a RobotState or a standard ik-request? This helper helps save/load dictionaries of ros messages to yaml files and param server.

## API

The helper deals with a dict of ROS messages (msgdict in short) e.g. {"red" : ColorRGBA(1,0,0,1), "blue" : ColorRGBA(0,0,1,1) }.

- msgdict2yaml: Turn a dict of ros messages into a yaml file
- yaml2msgdict: Read a dict of ros messages from yaml
- msgdict2params: Upload a dict of ros messages to param server
- msgdict2params: Retrieve a dict of ros messages from param server

## Example:

See example.py for full examples

```python
#Create a dict of ros messages for exmple:
complex_dict = dict()
complex_dict["My_fav_robot_traj"] = RobotTrajectory()
# complex_dict["My_fav_robot_traj"].<Fields> = ... some values that I want to save
complex_dict["DA_best_colour"] = ObjectColor()
complex_dict["I_always_forget_this_request"] = GetPositionIKRequest()
complex_dict["But I never forget this response"] = ListRobotStatesInWarehouseResponse()

#You can save your dict to a yaml
msg2param.msg_dict2yaml(complex_dict, save_path)

#Later in life you can read it
loaded_dict = msg2param.yaml2msg_dict(save_path)

#complex_dict and loaded_dict are identical
```

This is how a save msgdict looks like:

```yaml
arrow_scale:
dict: {x: 0.3, y: 0.02, z: 0.02}
type: geometry_msgs/Vector3
control_scale:
dict: {data: 0.35}
type: std_msgs/Float32
default_mesh:
dict: {data: 'package://interactive_waypoints/res/generic_flag.stl'}
type: std_msgs/String
marker_color:
dict: {a: 0.6, b: 0.8, g: 0.8, r: 0.8}
type: std_msgs/ColorRGBA
```

## Usecases:

- Saving colours, mesh_strings etc.
- Saving robot poses or states in a human readable way.
- Create a yaml files of common constant messages and load it from a launch file.
