# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 09:52:16 2022

@author: Near-field scanner
"""

import Classfiles.Video_test_xy_grid_version as Video
import Classfiles.Interface as Interface
import Classfiles.Robot_TCP_comm as Robot_TCP_comm
import Classfiles.Settings as Settings

camera_video = Video.Video("Run")
interface = Interface.Interface()
robot_control = Robot_TCP_comm.Robot_TCP_comm()

if __name__ == "__main__":
    camera_video.start()
    robot_control.start()
    interface.start()
    
    camera_video.join()
    robot_control.join()
    interface.join()