# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 08:10:03 2022

@author: Viktor From
"""

import Classfiles.Settings as Settings

class Convert():
    def __init__():
        return 0
    
    def findDistance(x_pix, y_pix):
        #print(type(self.robot_origin_fixed[0]))
        #print(x_pix, y_pix)
        x_dist_pix = Settings.robot_origin_fixed[0] - x_pix
        y_dist_pix = y_pix - Settings.robot_origin_fixed[1]
        #print("Distance in x: ", x_dist_pix)
        return (x_dist_pix), (y_dist_pix)
    
        '''
    Returns the distance in x and y between origin and center point of the detected point in pixels.
    -------
    int
        DESCRIPTION.
        '''
    
    def convertPixeltoMM(x_dist_pix, y_dist_pix):
        
        x_dist_mm = float((Settings.camera_distance*x_dist_pix*Settings.sensor_width)/(Settings.focal_length*Settings.img_width));
        y_dist_mm = float((Settings.camera_distance*y_dist_pix*Settings.sensor_height)/(Settings.focal_length*Settings.img_height));
        return x_dist_mm, y_dist_mm
    
    def closeupConvertPixeltoMM(self,x_dist_pix, y_dist_pix, distance_measured):
        
        x_dist_mm = float((distance_measured*x_dist_pix*Settings.sensor_width)/(Settings.focal_length*Settings.img_width));
        y_dist_mm = float((distance_measured*y_dist_pix*Settings.sensor_height)/(Settings.focal_length*Settings.img_height));
        return x_dist_mm, y_dist_mm
        
        '''
    
    Returns x and y in mm
    -------
    int
        DESCRIPTION.
        This function takes the distance between origin and the test point in pixels and converts it to mm.
        '''
        return x_dist_mm, y_dist_mm