# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 16:48:36 2022

@author: Viktor From
"""

import Video_corners
import Settings
import Interface

interface = Interface.Interface()
video = Video_corners.Video("Test")

if __name__ == "__main__":
    video.start()
    interface.start()
    
    video.join()
    interface.join()