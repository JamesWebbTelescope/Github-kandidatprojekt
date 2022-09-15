# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 09:30:03 2022

@author: Near-field scanner
"""

import Classfiles.Interface as Interface

interface = Interface.Interface()

if __name__ == "__main__":
    interface.start()
    
    interface.join()