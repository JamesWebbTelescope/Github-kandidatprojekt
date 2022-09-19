# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 12:58:47 2022

@author: Near-field scanner
"""

import Classfiles.Oscilloscope as Oscilloscope
import Classfiles.Settings as Settings

oscilloscope = Oscilloscope.Oscilloscope(Settings.voltages)

if __name__ == "__main__":
    oscilloscope.start()
    
    oscilloscope.join()