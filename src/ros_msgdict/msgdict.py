#!/usr/bin/env python
import rosparam
import yaml
from rospy_message_converter import message_converter
from std_msgs.msg import Float32
import genpy


def msgdict2yaml(msg_dict, path):
    """[Turn a dict of ros messages into a yaml file]

    Args:
        _dict ([dict]): [Dictionary of ros messages as values]
        path ([Str]): [Full path to yaml file]
    """
    _dict = _msgdict2_dict(msg_dict)
    f = open(path, 'w')
    try:
        yaml.dump(_dict, f)
    except Exception as e:
        print("Failed to write to file: {}; {}".format(path, e))
    finally:
        f.close()


def yaml2msgdict(path):
    """[Convert yaml into a dict of ros message variables]

    Args:
        path ([Str]): [Full path to yaml]

    Returns:
        [dict]: [Dictionary of the ros messages saved]
    """
    with open(path, 'r') as stream:
        try:
            yaml_dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return _dict2msgdict(yaml_dict)


def msgdict2params(msg_dict, namespace):
    """[Save dict of ros messages on the parameter server. This requires that you have a node/master running]

    Args:
        _dict ([type]): [description]
        namespace ([type]): [description]
    """
    if _check_msgdict_format(msg_dict):
        rosparam.set_param_raw(namespace, _msgdict2_dict(msg_dict))


def params2msgdict(namespace):
    """[Turn parameters under a namespace into a ros message dictionary]

    Args:
        namespace ([str]): [namespace to be laoded]

    Returns:
        [dict]: [dict of ros messages]
    """
    _dict = rosparam.get_param(namespace)
    return _dict2msgdict(_dict)


def _check_dict_format(_dict):
    """[Checks if the _dict are in the expected format for conversion]

    Returns:
        [bool]: [is ok]
    """

    for key in _dict.keys():
        if not set(_dict[key].keys()) == {"type", "dict"}:
            print("Dict should only have type and dict as dict elements.")
            return False
        if not isinstance(_dict[key]["type"], str):
            print("type should be a string. e.g. geometry_msgs/PoseStamped")
            return False
        if not isinstance(_dict[key]["dict"], dict):
            print("dict should be a dict with message data")
            return False
    return True


def _check_msgdict_format(msg_dict):
    """[Check if msg_dict is a true dict of ros messages]

    Args:
        msg_dict ([dict]): [dict of ros messages]

    Returns:
        [bool]: [is as expected]
    """
    for key in msg_dict.keys():
        if not isinstance(msg_dict[key], genpy.Message):
            print("Message dictionary has elements that are not ros messages")
            return False
    return True


def _dict2msgdict(_dict):
    """[Turn a loaded yaml or rosparams dict into a ros message dict]

    Args:
        _dict ([dict]): [description]

    Returns:
        [dict]: [Dictionary of ros messages]
    """
    if _check_dict_format(_dict):
        msg_dict = dict()
        for key in _dict.keys():
            try:
                name, kind = _msgtype2kind(_dict[key]["type"])
                msg_dict[key] = message_converter.convert_dictionary_to_ros_message(
                    name, _dict[key]["dict"], kind=kind)
            except Exception as e:
                print("Reading message dictionary failed: {}".format(e))
                return None
        return msg_dict
    else:
        return None


def _msgdict2_dict(msg_dict):
    """[Convert a dict of ros messages into the _dict standard]

    Args:
        msg_dict ([dict]): [Dict of ros messages]

    Returns:
        [dict]: [Dictionary ready to be saved]
    """
    if _check_msgdict_format(msg_dict):
        _dict = dict()
        for key in msg_dict.keys():
            print("type is {};".format(type(msg_dict[key]._type)))
            __dict = _string_formatting(
                message_converter.convert_ros_message_to_dictionary(msg_dict[key]))
            _dict[key] = {"type": msg_dict[key]._type,
                          "dict": __dict}
        return _dict


def _string_formatting(_dict):    

    for key in _dict.keys():
        val = _dict[key]
        if isinstance(val, dict):
            _dict[key] = _string_formatting(val)
        elif "unicode" in str(type(val)):
            _dict[key] = str(val)
    return _dict


def _msgtype2kind(msg_name):
    """[message name string into type...]

    Args:
        msg_name ([str]): [message type/name]

    Returns:
        [str]: [message/response/request]
    """
    if "Response" in msg_name:
        return msg_name[:-8], "response"

    if "Request" in msg_name:
        return msg_name[:-7], "request"

    return msg_name, "message"
