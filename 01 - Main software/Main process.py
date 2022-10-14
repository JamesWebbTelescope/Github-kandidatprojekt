# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 17:16:01 2022

@author: Viktor From
"""

import Classprocesses.Arduino as Arduino
import Classprocesses.Settings as Settings
import Classprocesses.Interface as Interface
import Classprocesses.Robot_TCP_comm as Robot_TCP_comm
import Classprocesses.Oscilloscope as Oscilloscope
import Classprocesses.Video_corners as Video

interface = Interface.Interface()
arduino_control = Arduino.Arduino(Settings.cleandata, Settings.text, Settings.voltages, Settings.button_state)
robot_control = Robot_TCP_comm.Robot_TCP_comm()
osc_control = Oscilloscope.Oscilloscope(Settings.voltages)
camera_video = Video.Video("Run")

if __name__ == "__main__":
    interface.start()
    arduino_control.start()
    robot_control.start()
    osc_control.start()
    camera_video.start()
    
    interface.join()
    arduino_control.join()
    robot_control.join()
    osc_control.join()
    camera_video.join()