# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 12:52:08 2022

@author: Near-field scanner
"""

import Arduino
import Settings

arduino_control = Arduino.Arduino(Settings.cleandata, Settings.text, Settings.voltages, Settings.button_state)

if __name__ == "__main__":
    arduino_control.start()
    
    arduino_control.join()