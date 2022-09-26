# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 08:45:50 2022

@author: Viktor From
"""

from threading import Thread
import pyvisa
import csv
import Classfiles.Settings as Settings
import datetime

class Oscilloscope(Thread):
    def __init__(self, voltages):
        Thread.__init__(self) #Assign this class to a thread and initialize the thread.
        self.voltages = voltages #Make sure that the voltages variable can be accessed by all the different functions in this class
        rm = pyvisa.ResourceManager() #Open a Resource Manager.
        print(rm.list_resources('?*')) #List all of the available instruments 
        try:
            self.inst = rm.open_resource('TCPIP0::192.168.11.8::inst0::INSTR', read_termination='\n', open_timeout=1000) #Open communication to the oscilloscope
            print(self.inst.query('*IDN?')) #Ask for the name of the oscilloscope to ensure that it is the correct one that's connected to.
            self.inst.write("RUN;*OPC?") #Begin a measurement.
            self.inst.write("TRIG:MODE AUTO") #Set the Trigger Mode to Auto
            self.inst.write("MEAS1:SOUR C1W1") # Set the source of the measurement to channel 1, waveform 1.
            self.inst.write("MEAS1:MAIN AMPL") # Set channel 1 to measure the amplitude of the signal.
            self.inst.write("MEAS1 ON") #Begin the measurement
            self.inst.write("*OPC?") #Wait for the oscilloscope to complete the commands
        except pyvisa.Error as e: #If something goes wrong in accessing the oscilloscope:
            print(e) #Print the error
        #inst.write("RUN")
    
    def run(self):
        global voltages
        while True:
            self.voltages = self.getVoltage() #Get the current voltage from the oscilloscope
            Settings.voltages = self.voltages #Make sure that the other threads can read the current voltage level as well.
            #print(Settings.voltages)
            now = datetime.datetime.now() #Get the current time
            filename = "C:/Users/Near-field scanner/Documents/Near_Field_Scanner_GUI_source/sandbox/Viktor From/Test capture.csv"
            #print(now)
            #print(type(str(now)))
            if(Settings.voltages > str(1)): #If the voltage level is above 1 V
                data = self.inst.query_ascii_values("CHAN1:WAV1:DATA?") #Get the full waveform from the oscilloscope
                self.inst.write("SYST:DISP:UPD ON")
                self.inst.write("HCOP:DEST 'MMEM'")
                self.inst.write("HCOP:DEV:LANG JPG") #Store a screenshot from the oscilloscope on the oscillosocpe's memory.
                self.inst.write("*OPC?")
                self.inst.write("MMEM:NAME 'D:\Test.jpg'")
                with open(filename, 'a', encoding='UTF-8', newline = "\n") as f: #Open or create a .csv-file.
    # create the csv writer
                     header = ['Voltage'] #Give it the header "Voltage"
                     writer = csv.writer(f) #Open a writer so it can be written to the .csv-file
                     writer.writerow(header) #Add the header.
                     '''for d in range(len(data)):
                         print(data[d:])'''
    # write a row to the csv file
                     writer.writerow(data) #Add the full waveform.
                     f.close() #Close the file.
            if Settings.terminateFlag == 1: #If the terminate button has been pressed:
                break #Stop the thread.
        self.close() #Close all communication
        
    def getVoltage(self):
        self.inst.write("TRIG:MODE:AUTO") #Set the trigger mode to Auto
        voltages = self.inst.query_ascii_values("MEAS1:RES:ACT?", 'f') #Get the current measurement results
        #print(type(voltages))
        for i in range(len(voltages)):
           voltages = str(voltages[i]) #Convert the voltages from floats to strings.
        #self.inst.write("TRIG:MODE:AUTO")
        return voltages
    def close(self):
        self.inst.close() #Close the communication with the oscilloscope.
        return None
    