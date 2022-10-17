# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 08:13:30 2022

@author: Viktor From
"""
import sys
from threading import Thread
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import Classfiles.Settings as Settings

class Interface(Thread):
    def __init__(self, robot_control_thread):
        Thread.__init__(self)
        self.robot_thread = robot_control_thread
    
    def run(self):
        self.window()
    
    def window(self):
        app = QApplication(sys.argv)
        widget = QWidget()
       
        button1 = QPushButton(widget)
        button1.setText("Start camera")
        button1.move(64,32)
        button1.clicked.connect(self.button1_clicked)

        button2 = QPushButton(widget)
        button2.setText("Stop camera")
        button2.move(64,64)
        button2.clicked.connect(self.button2_clicked)
        
        button3 = QPushButton(widget)
        button3.setText("Start robot")
        button3.move(64,96)
        button3.clicked.connect(self.button3_clicked)
        
        button4 = QPushButton(widget)
        button4.setText("Stop robot")
        button4.move(64,128)
        button4.clicked.connect(self.button4_clicked)
        
        button5 = QPushButton(widget)
        button5.setText("Terminate program")
        button5.move(64,160)
        button5.clicked.connect(self.button5_clicked)
        
        button6 = QPushButton(widget)
        button6.setText("Close connection to robot")
        button6.move(64,200)
        button6.clicked.connect(self.button6_clicked)
        
        button7 = QPushButton(widget)
        button7.setText("Open connection to robot")
        button7.move(64,240)
        button7.clicked.connect(self.button7_clicked)

        widget.setGeometry(50,50,320,300)
        widget.setWindowTitle("ESD Test control")
        widget.show()
        sys.exit(app.exec_())


    def button1_clicked(self):
        print("Camera started")
        Settings.camera_event.set()

    def button2_clicked(self):
        global camera_event
        print("Camera stopped") 
        Settings.camera_event.clear()
        
    def button3_clicked(self):
        global robot_event
        print("Robot started") 
        Settings.robot_event.set()
        
    def button4_clicked(self):
        global robot_event
        print("Robot stopped") 
        Settings.robot_event.clear()
        
    def button5_clicked(self):
        global terminateFlag
        global robot_event
        global camera_event
        Settings.robot_event.set()
        Settings.camera_event.set()
        Settings.terminateFlag = 1
        Settings.robot_event.clear()
        Settings.camera_event.clear()
        print("Program terminated") 
    
    def button6_clicked(self):
        self.robot_thread.close()
        print("Connection to robot closed") 
    
    def button7_clicked(self):
        self.robot_thread.open_connection()
        print("Connection to robot opened") 
        