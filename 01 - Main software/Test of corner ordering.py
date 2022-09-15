# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 08:27:33 2022

@author: Near-field scanner
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 16:48:36 2022

@author: Viktor From
"""

import Video_corners
import Interface

interface = Interface.Interface()
video = Video_corners.Video("Run")

if __name__ == "__main__":
    video.start()
    interface.start()
    
    video.join()
    interface.join()