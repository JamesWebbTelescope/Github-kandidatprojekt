# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 08:27:59 2022

@author: Near-field scanner
"""

from threading import Event
    
distance_measured = 100
img_width = 640 #Width of the images taken in pixels
img_height = 480 #Height of the images taken in pixels
autofocus = 0.32 #The focus setting for the camera
auto_brightness = 2 #the brightness setting for the camera
test_points = [[0,0], [0,0], [0,0], [0,0], [0,0]] #Deprecated
box_w, box_h, img_rect, circles, img_text, box_x, box_y = [0,0,0,0,0,0,0] #Deprecated
voltages = str(0) #The voltages measured by the oscilloscope
button_state = b'' #Deprecated
button_state_decoded = '' #Deprecated
text = 'Text'#Deprecated
cleandata = 'Nothing'#Deprecated
img_points = [] #The list of points of interest in the image
circles_x = 0 #Deprecated
circles_y = 0 #Deprecated
takePicFlag = 0 #Deprecated
x_mm, y_mm = [0,0] #Deprecated
camera_event = Event() #The evnets used to control the camera and the robot
robot_event = Event()
terminateFlag = 0 #The flag used to indicate if the program should terminate or not.
robot_origin_fixed = (img_width/2, img_height/2) #The robot origin in the image, used to calculate the distance to the points in the img_points list
camera_distance = 833.0 #The distance of the camera above the table
camera_distance_2 = 100.0 #Deprecated
sensor_width = 4.54 #The camera onstants
sensor_height = 3.4565
focal_length = 3.916
rx_mm, ry_mm = [0,0] #The coordinate that the robot should go to.
