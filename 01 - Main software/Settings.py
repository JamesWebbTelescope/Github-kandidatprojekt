# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 08:27:59 2022

@author: Near-field scanner
"""

from threading import Event
    
distance_measured = 0
img_width = 640
img_height = 480
test_points = [[0,0], [0,0], [0,0], [0,0], [0,0]]
box_w, box_h, img_rect, circles, img_text, box_x, box_y = [0,0,0,0,0,0,0]
voltages = str(0)
button_state = b''
button_state_decoded = ''
text = 'Text'
cleandata = 'Nothing'
img_points = []
circles_x = 0
circles_y = 0
takePicFlag = 0
x_mm, y_mm = [0,0]
camera_event = Event()
robot_event = Event()
terminateFlag = 0
robot_origin_fixed = (img_width/2, img_height/2)
camera_distance = 833.0
camera_distance_2 = 100.0
sensor_width = 4.54
sensor_height = 3.4565
focal_length = 3.916
