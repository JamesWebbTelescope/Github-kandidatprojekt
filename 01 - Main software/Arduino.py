# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 08:42:42 2022

@author: Near-field scanner
"""

from threading import Thread

class Arduino(Thread):
    def __init__(self, cleandata, text, voltages, button_state):
        Thread.__init__(self)
        self.cleandata = cleandata
        self.text = text
        self.voltages = voltages
        self.button_state = button_state
        self.data = b''
        self.connectToArduino()
        return None
    
    def run(self):
        global text
        global FSR_voltage
        global distance_measured
        while True:
            self.data = self.readLines()
         #   print(self.data)
            #cleandata = arduino_control.cleanData(data)
            self.cleandata = self.data.decode()
            split = self.cleandata.split()
          #  print("Received from Arduino")
          #  print(split)
            if len(split) > 1:
                FSR_voltage = float(split[0].replace(',', ''))
           #     print(FSR_voltage)
            #    print(type(FSR_voltage))
                #print("Distance")
                distance_measured = int(float(split[1].replace(',', '')))
                #print(distance_measured)
               # print(type(distance))
            else:
                FSR_voltage = 0.0
                distance_measured = 1000
            #if len(split) <= 1:
            self.text = self.cleandata.strip() + "\n" + "Voltage: " + '\n' + str(self.voltages) + '\n' + "Button: " + str(self.button_state)
            
          #  print(self.text)
            text = self.text
            if terminateFlag == 1:
                break
        self.close()
        
    def connectToArduino(self):
        try:
            self.comm = serial.Serial('COM3', 115200, timeout=.1)
        except:
            print("Couldn't connect to Arduino")
    
    def readLines(self):
        data = self.comm.readline()[:-2]
        return data
    
    def cleanData(self, data):
        newl = []
        for i in range(len(data)):
            temp = data[i][2:]
            newl.append(temp)
        return newl
    
    def close(self):
        self.comm.close()