# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 09:08:31 2022

@author: Near-field scanner
"""

import Video
import Interface
import Settings

camera_video = Video.Video(Settings.text)
interface = Interface.Interface()

if __name__ =="__main__":
    interface.start()
    camera_video.start()
    
    
    camera_video.join()
    interface.join()
