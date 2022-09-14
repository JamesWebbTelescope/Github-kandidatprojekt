# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 09:52:16 2022

@author: Near-field scanner
"""

import Video_test_version
import Interface
import Robot_TCP_comm
import Settings

camera_video = Video_test_version.Video(Settings.text)
interface = Interface.Interface()
robot_control = Robot_TCP_comm.Robot_TCP_comm()

if __name__ == "__main__":
    camera_video.start()
    robot_control.start()
    interface.start()
    
    camera_video.join()
    robot_control.join()
    interface.join()