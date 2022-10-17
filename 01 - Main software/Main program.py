# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 09:16:17 2022

@author: Near-field scanner
"""

import Classfiles.Interface as Interface
import Classfiles.Arduino as Arduino
import Classfiles.Robot_TCP_comm as Robot_TCP_comm
import Classfiles.Oscilloscope as Oscilloscope
import Classfiles.Video_corners as Video
import Classfiles.Settings as Settings

arduino_control = Arduino.Arduino(Settings.cleandata, Settings.text, Settings.voltages, Settings.button_state)
robot_control = Robot_TCP_comm.Robot_TCP_comm()
osc_control = Oscilloscope.Oscilloscope(Settings.voltages)
camera_video = Video.Video("Test")
interface = Interface.Interface(robot_control)

if __name__ == "__main__": #Make sure that only the main thread is running.
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