# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 08:42:42 2022

@author: Near-field scanner
"""

from threading import Thread
import Classfiles.Settings as Settings
import serial

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
        while True:
            self.data = self.readLines() #Receive data from the Teensy.
         #   print(self.data)
            #cleandata = arduino_control.cleanData(data)
            self.cleandata = self.data.decode() #Decode the data from the Teensy.
            split = self.cleandata.split() #Split the data into separate parts, so they can be assigned to separate variables.
          #  print("Received from Arduino")
          #  print(split)
            if len(split) > 1: #Check that the message isn't empty.
                Settings.FSR_voltage = float(split[0].replace(',', '')) #Get the voltage of the force-sensitive resistor and make sure that it doesn't contain any commas.
           #     print(FSR_voltage)
            #    print(type(FSR_voltage))
                #print("Distance\n")
                Settings.distance_measured = int(float(split[1].replace(',', ''))) #Get the distance to the DUT and make sure there are no commas.
                #print(Settings.distance_measured)
               # print(type(distance))
            else:
                Settings.FSR_voltage = 0.0 #In case the connection to the Teensy is lost. 
                Settings.distance_measured = 1000
            #if len(split) <= 1:
            self.text = self.cleandata.strip() + "\n" + "Voltage: " + '\n' + str(self.voltages) + '\n' + "Button: " + str(self.button_state) #If everything is received correctly, store it all so it cna be printed later.
            
          #  print(self.text)
            Settings.text = self.text
            if Settings.terminateFlag == 1: #If the main program calls for a termination, stop the communication.
                break
        self.close()
        
    def connectToArduino(self):
        try:
            self.comm = serial.Serial('COM3', 115200, timeout=.1) #Open the port to the Teensy.
        except:
            print("Couldn't connect to Arduino") #In case no port can be opened, print out "Couldn't connect to Arduino"
    
    def readLines(self):
        data = self.comm.readline()[:-2] #Receive data from the Teensy, ignore the last two characters.
        return data
    
    def cleanData(self, data):
        newl = []
        for i in range(len(data)):
            temp = data[i][2:]
            newl.append(temp)
        return newl
    
    def close(self):
        self.comm.close() #Close the port