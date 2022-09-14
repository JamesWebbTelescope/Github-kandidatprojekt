# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 08:45:50 2022

@author: Near-field scanner
"""

from threading import Thread
import pyvisa
import csv
import Settings

class Oscilloscope(Thread):
    def __init__(self, voltages):
        Thread.__init__(self)
        self.voltages = voltages
        rm = pyvisa.ResourceManager()
        print(rm.list_resources('?*'))
        try:
            self.inst = rm.open_resource('TCPIP0::192.168.11.8::inst0::INSTR', read_termination='\n', open_timeout=1000)
            print(self.inst.query('*IDN?'))
            self.inst.write("RUN;*OPC?")
            self.inst.write("TRIG:MODE AUTO")
            self.inst.write("MEAS1:SOUR C1W1") # Configure frequency measurement
            self.inst.write("MEAS1:MAIN AMPL")
            self.inst.write("MEAS1 ON")
            self.inst.write("*OPC?")
        except pyvisa.Error as e:
            print(e)
        #inst.write("RUN")
    
    def run(self):
        global voltages
        while True:
            self.voltages = self.getVoltage()
            Settings.voltages = self.voltages
            print(Settings.voltages)
            if(Settings.voltages > str(1)):
                data = self.inst.query_ascii_values("CHAN1:WAV1:DATA?")
                self.inst.write("SYST:DISP:UPD ON")
                self.inst.write("HCOP:DEST 'MMEM'")
                self.inst.write("HCOP:DEV:LANG JPG")
                self.inst.write("*OPC?")
                self.inst.write("MMEM:NAME 'D:\Test.jpg'")
                with open('C:/Users/Near-field scanner/Documents/Near_Field_Scanner_GUI_source/sandbox/Viktor From/Test of voltage capture 16/08/2022.csv', 'a', encoding='UTF-8', newline = "\n") as f:
    # create the csv writer
                     header = ['Voltage']
                     writer = csv.writer(f)
                     writer.writerow(header)
                     '''for d in range(len(data)):
                         print(data[d:])'''
    # write a row to the csv file
                     writer.writerow(data)
                     f.close()
            if Settings.terminateFlag == 1:
                break
        self.close()
        
    def getVoltage(self):
        self.inst.write("TRIG:MODE:AUTO")
        voltages = self.inst.query_ascii_values("MEAS1:RES:ACT?", 'f')
        #print(type(voltages))
        for i in range(len(voltages)):
           voltages = str(voltages[i])
        #self.inst.write("TRIG:MODE:AUTO")
        return voltages
    def close(self):
        self.inst.close()
        return None
    