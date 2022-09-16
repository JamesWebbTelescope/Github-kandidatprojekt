# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 09:05:30 2022

@author: Near-field scanner
"""

import Classfiles.Video_corners as Video_corners
import Classfiles.Robot_TCP_comm as Robot_TCP_comm
import Classfiles.Interface as Interface

interface = Interface.Interface()
camera_video = Video_corners.Video("Run")
robot_control = Robot_TCP_comm.Robot_TCP_comm()

if __name__ == "__main__":
    interface.start()
    camera_video.start()
    robot_control.start()
    
    interface.join()
    camera_video.join()
    robot_control.join()