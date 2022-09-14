# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 08:17:01 2022

@author: Near-field scanner
"""

import socket
import sys
import time
from threading import Thread
import Settings


class Robot_TCP_comm(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv.settimeout(2)
        self.send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send.settimeout(2)
        self.open_connection()
        
    def run(self):
        print("Start")
        print(Settings.img_points)
        Settings.robot_event.wait()
        while True:
            if len(Settings.img_points) > 0:
                #print(Settings.img_points)
                #print(type(Settings.Settings.img_points[0][0]))
                print("Start")
                #button_state = self.checkButton()
                #button_state_decoded = button_state.decode()
                #  print(Settings.Settings.img_points[i][0])
                #  print(type(Settings.Settings.img_points[i][0]))
                #x_dist_pix, y_dist_pix = Convert.Convert.findDistance((Settings.img_points[0][0]), (Settings.img_points[0][1]))
                #x_mm, y_mm = Convert.Convert.convertPixeltoMM(x_dist_pix, y_dist_pix)
                print(Settings.rx_mm, Settings.ry_mm)
                # print("Distance to point:")
                #print(x_mm, y_mm)
                self.moveRobot(Settings.rx_mm, Settings.ry_mm)
                print("Done")
                if Settings.terminateFlag == 1:
                    break
        print("Closing")
        self.recv.sendall(b"takepic = 1\n")
        time.sleep(1)
        self.close()
                
    def open_connection(self):
        # Create a TCP/IP socket

        # Connect the socket to the port where the server is listening
            receive_address = ("192.168.11.2", 23)
            send_address = ("192.168.11.2", 49152)
            print('connecting to %s port %s' % receive_address)
            try:
               self.recv.connect(receive_address)
               message = b''
               print(sys.stderr, 'sending "%s"' % message)

               self.recv.sendall(message)
               time.sleep(0.2)
               self.recv.sendall(b"as\n")
               time.sleep(0.8)
               self.recv.sendall(b"ZPOWER ON\n")
               time.sleep(1)
               self.recv.sendall(b"EXECUTE main\n")
               time.sleep(1)
               self.recv.sendall(b"open_flag = 1\n")
               time.sleep(1)
               self.send.connect(send_address)
               received = self.send.recv(1024)
               print("Connection made")
               print(received)
               self.recv.sendall(b"takepic = 1\n")
               time.sleep(1)
            except socket.error as e:
                print(e)
            except:
                print("No connection")
    
    def close(self):
        self.recv.sendall(b"close_flag = 1\n")

        time.sleep(1)

        self.send.close()
        self.recv.close()
    
    def moveRobot(self, x_dist_mm, y_dist_mm):
        global voltage, FSR_voltage, distance_measured, takePicFlag
        '''time.sleep(1)
        self.recv.sendall(b"zShift = -200\n")
        time.sleep(1)
        self.recv.sendall(b"zShift = 0\n")
        time.sleep(1)'''
        send_x = "xShift = " + str(x_dist_mm) + "\n"
        send_y = "yShift = " + str(y_dist_mm) + "\n"
        send_x_encoded = send_x.encode('utf-8')
        send_y_encoded = send_y.encode('utf-8')
        #print("Moving")
        #print(x_dist_mm)
        print(send_y_encoded)
        print(send_x_encoded)
        #self.recv.sendall(b"xShift = ")
        #self.recv.sendall(np.byte(x_dist_mm))
        #self.recv.sendall(b"\n")
        self.recv.sendall(send_x_encoded)
        time.sleep(1)
        print("Sent x coordinates")
        #self.recv.sendall(b"yShift = ")
        #self.recv.sendall(np.byte(y_dist_mm))
        #self.recv.sendall(b"\n")
        self.recv.sendall(send_y_encoded)
        time.sleep(2)
        print("Sent y coordinate")
        print("Found the test point")
        self.recv.sendall(b"yShift = 65\n")
        time.sleep(1)
        '''for i in range(55):
            self.recv.sendall(b"yShift = 1\n")
            time.sleep(0.1)'''
        #print("Moving to probe")
        #time.sleep(0.1)
        turns = 0
        while (Settings.distance_measured > 20 and Settings.voltages < str(1)):
            Settings.robot_event.wait()
            self.recv.sendall(b"zShift = -1\n")
            #print("Moving down")
            time.sleep(0.1)
            turns = turns + 1
            #print(turns)
            if turns == 600:
                takePicFlag = 1
                self.recv.sendall(b"zShift = 0\n")
                '''while len(Settings.Settings.img_points) == 1: #This is to ensure that the thread doesn't break if the list of points isn't bigger than one point set
                    if len(Settings.Settings.img_points) > 1:
                        break
                x_dist_pix, y_dist_pix = self.findDistance(Settings.Settings.img_points[1][0], Settings.Settings.img_points[1][1])
                x_mm, y_mm = self.closeupConvertPixeltoMM(x_dist_pix, y_dist_pix)
                send_x = "xShift = " + str(x_dist_mm) + "\n"
                send_y = "yShift = " + str(y_dist_mm) + "\n"
                print(x_mm, y_mm)
                send_x_encoded = send_x.encode('utf-8')
                send_y_encoded = send_y.encode('utf-8')
                self.recv.sendall(send_x_encoded)
                time.sleep(0.1)
                self.recv.sendall(send_y_encoded)
                time.sleep(0.1)'''
            if turns > 1800:
                self.recv.sendall(b"zShift = 0\n")
                time.sleep(1)
                self.recv.sendall(b"takepic = 1\n")
                time.sleep(1)
                print("Robot stopeed to avoid crash!")
                time.sleep(0.1)
                break
            if  (Settings.voltages > str(1)):
                self.recv.sendall(b"zShift = 0\n")
                #print("Robot stopped")
                time.sleep(1)
                self.recv.sendall(b"takepic = 1\n")
                time.sleep(1)
                break
            if Settings.terminateFlag == 1:
                self.recv.sendall(b"zShift = 0\n")
                #print("Robot stopped")
                time.sleep(1)
                self.recv.sendall(b"takepic = 1\n")
                time.sleep(1)
                break
            if (Settings.distance_measured < 20):
                self.recv.sendall(b"zShift = 0\n")
                #print("Robot stopped")
                time.sleep(1)
                self.recv.sendall(b"takepic = 1\n")
                time.sleep(1)
                break
    '''
        Returns nothing
        -------
        int
            DESCRIPTION.
            This function sends the distance in x and y in mm to the robot for the robot to move.
             '''
    def checkButton(self):
        self.recv.sendall(b"BUTTON_FLAG = 1\n")
        BITS = self.send.recv(1024)
        print(BITS)
        return BITS
    
    
    def scanHeight(self):
        x_1 = 0
        x_2 = 0
        y = 0
        height = 100
        while x_1 < 100:
          print("Move x")
          print("Moved ", x_1)
          self.recv.sendall(b"xshift = 0.05")
          self.recv.sendall(b"\n")          #recv.sendall(b"F_POS_Z = 1")
        #received = send.receive()
          line = Settings.text
          line = line.decode()
          x_1 = x_1 + 0.05
          write = [line.strip() + ',' + str(x_1) + ','+ str(y) + "\n"]
          #f.writelines(write)
          #print(write)
          #print(line)
          time.sleep(0.1)
        print("Stopped")
        while x_2 < 100:
           #recv.sendall(b"xshift = 0")
            self.recv.sendall(b"xshift = -5\n")
            print("Moving back")
            #line = ser.readline()
            #line = line.decode()
            #print(line)
            x_2 = x_2 + 5
            time.sleep(0.1)
    #recv.sendall(b"-20")
        for k in range(1):
            self.recv.sendall(b"yshift = -0.05\n")
            #line = ser.readline()
            #line = line.decode()
            #print(line)
            y = y + 0.05
            time.sleep(0.1)
        print("Reset")
        if y > 50:
            print("Measurement stopped")
        return height
    #recv.sendall(b"-2")
    #time.sleep(0.2)