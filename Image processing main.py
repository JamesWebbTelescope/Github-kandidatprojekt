
"""
Created on Fri Feb 25 09:12:53 2022
Taken from https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html
@author: Viktor From
"""

import cv2 as cv
import numpy as np
import serial
import socket
import sys
import time
import pyvisa
from threading import Thread, Event
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

global img2
global img_text
global rect
global box
global img_rect
global rect2
global box2
global img_rect2
global img_points
global img_points2
global text
global test_points
global FSR_voltage
global distance_measured
test_points = [[0,0], [0,0], [0,0], [0,0], [0,0]]
box_w, box_h, img_rect, circles, img_text, box_x, box_y = [0,0,0,0,0,0,0]
voltages = str(0)
button_state = b''
button_state_decoded = ''
text = 'Text'
cleandata = 'Nothing'
img_points = []
circles_x = 0
circles_y = 0
takePicFlag = 0
x_mm, y_mm = [0,0]
camera_event = Event()
robot_event = Event()
terminateFlag = 0

class Interface(Thread):
    def __init__(self):
        Thread.__init__(self)
    
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

        widget.setGeometry(50,50,320,200)
        widget.setWindowTitle("ESD Test control")
        widget.show()
        sys.exit(app.exec_())


    def button1_clicked(self):
        global camera_event
        print("Camera started")
        camera_event.set()

    def button2_clicked(self):
        global camera_event
        print("Camera stopped") 
        camera_event.clear()
        
    def button3_clicked(self):
        global robot_event
        print("Robot started") 
        robot_event.set()
        
    def button4_clicked(self):
        global robot_event
        print("Robot stopped") 
        robot_event.clear()
        
    def button5_clicked(self):
        global terminateFlag
        global robot_event
        global camera_event
        robot_event.set()
        camera_event.set()
        terminateFlag = 1
        robot_event.clear()
        camera_event.clear()
        print("Program terminated") 

class Robot_TCP_comm(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.robot_origin_fixed = (640, 360)
        self.camera_distance = 864.0
        self.camera_distance_2 = 100.0
        self.sensor_width = 4.54
        self.sensor_height = 3.4565
        self.focal_length = 3.916
        self.open_connection()
        
    def run(self):
        print("Start")
        print(img_points)
        robot_event.wait()
            
        while True:
            robot_event.wait()
            if len(img_points) > 0:
                print(img_points[0][0])
                #print(type(img_points[0][0]))
                for i in range(len(img_points)):
                    print("Start")
                    #button_state = self.checkButton()
                    #button_state_decoded = button_state.decode()
                 #   print(img_points[i][0])
                  #  print(type(img_points[i][0]))
                    x_dist_pix, y_dist_pix = self.findDistance(img_points[i][0]+(img_points[i][2]/4), img_points[i][1]+(img_points[i][3]/4))
                    x_mm, y_mm = self.convertPixeltoMM(x_dist_pix, y_dist_pix)
                   # print("Distance to point:")
                    #print(x_mm, y_mm)
                    self.moveRobot(x_mm, y_mm)
                    '''print(len(test_points))
                    for i in range(len(test_points)):
                        x_dist_pix, y_dist_pix = self.findDistance(test_points[i][0], test_points[i][1])
                        print(box_x, box_y)
                        x_mm, y_mm = self.convertPixeltoMM(x_dist_pix, y_dist_pix)
                        self.moveRobot(x_mm, y_mm)'''
                    if terminateFlag == 1:
                        break
                if terminateFlag == 1:
                    break
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
        time.sleep(1)
        self.recv.sendall(b"zShift = -200\n")
        time.sleep(1)
        self.recv.sendall(b"zShift = 0\n")
        send_x = "xShift = " + str(x_dist_mm) + "\n"
        send_y = "yShift = " + str(y_dist_mm) + "\n"
        send_x_encoded = send_x.encode('utf-8')
        send_y_encoded = send_y.encode('utf-8')
        #print("Moving")
        #print(x_dist_mm)
        #print(send_y_encoded)
        #self.recv.sendall(b"xShift = ")
        #self.recv.sendall(np.byte(x_dist_mm))
        #self.recv.sendall(b"\n")
        self.recv.sendall(send_x_encoded)
        time.sleep(0.1)
        #self.recv.sendall(b"yShift = ")
        #self.recv.sendall(np.byte(y_dist_mm))
        #self.recv.sendall(b"\n")
        self.recv.sendall(send_y_encoded)
        time.sleep(0.1)
        #print("Found the test point")
        self.recv.sendall(b"yShift = 135\n")
        #print("Moving to probe")
        time.sleep(0.1)
        turns = 200
        while (voltages < str(1) and distance_measured > 20):
            robot_event.wait()
            self.recv.sendall(b"zShift = -1\n")
            #print("Moving down")
            time.sleep(0.1)
            turns = turns + 1
            print(turns)
            if turns == 600:
                takePicFlag = 1
                self.recv.sendall(b"zShift = 0\n")
                x_dist_pix, y_dist_pix = self.findDistance(img_points[0][0]+(img_points[0][2]/4), img_points[0][1]+(img_points[0][3]/4))
                x_mm, y_mm = self.closeupConvertPixeltoMM(x_dist_pix, y_dist_pix)
                send_x = "xShift = " + str(x_dist_mm) + "\n"
                send_y = "yShift = " + str(y_dist_mm) + "\n"
                send_x_encoded = send_x.encode('utf-8')
                send_y_encoded = send_y.encode('utf-8')
                self.recv.sendall(send_x_encoded)
                time.sleep(0.5)
                self.recv.sendall(send_y_encoded)
                time.sleep(0.5)
                #print("Turns exceeded 600!")
            if turns > 1400:
                self.recv.sendall(b"zShift = 0\n")
                time.sleep(1)
                self.recv.sendall(b"takepic = 1\n")
                time.sleep(1)
                print("Robot stopeed to avoid crash!")
                break
                time.sleep(0.1)
            if (voltages > str(1)):
                self.recv.sendall(b"zShift = 0\n")
                #print("Robot stopped")
                time.sleep(1)
                self.recv.sendall(b"takepic = 1\n")
                time.sleep(1)
                break
            if terminateFlag == 1:
                self.recv.sendall(b"zShift = 0\n")
                #print("Robot stopped")
                time.sleep(1)
                self.recv.sendall(b"takepic = 1\n")
                time.sleep(1)
                break
            if (distance_measured < 20):
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
    
    def findDistance(self, x_pix, y_pix):
        #print(type(self.robot_origin_fixed[0]))
        #print(x_pix, y_pix)
        x_dist_pix = x_pix - self.robot_origin_fixed[0]
        y_dist_pix = y_pix - self.robot_origin_fixed[1]
        #print("Distance in x: ", x_dist_pix)
        return (x_dist_pix), (y_dist_pix)
    
        '''
    Returns the distance in x and y between origin and center point of the detected point in pixels.
    -------
    int
        DESCRIPTION.
        '''
    
    def convertPixeltoMM(self,x_dist_pix, y_dist_pix):
        
        x_dist_mm = float((self.camera_distance*x_dist_pix*self.sensor_width)/(self.focal_length*640.0));
        y_dist_mm = float((self.camera_distance*y_dist_pix*self.sensor_height)/(self.focal_length*480.0));
        return x_dist_mm, y_dist_mm
    
    def closeupConvertPixeltoMM(self,x_dist_pix, y_dist_pix):
        global distance_measured
        
        x_dist_mm = float((distance_measured*x_dist_pix*self.sensor_width)/(self.focal_length*640.0));
        y_dist_mm = float((distance_measured*y_dist_pix*self.sensor_height)/(self.focal_length*480.0));
        return x_dist_mm, y_dist_mm
        
        '''
    
    Returns x and y in mm
    -------
    int
        DESCRIPTION.
        This function takes the distance between origin and the test point in pixels and converts it to mm.
        '''
        return x_dist_mm, y_dist_mm
    
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
          line = text
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

class Video(Thread):
    def __init__(self, text):
        self.text = text
        self.model = []
        self.class_names = ['DP700B750T105518', 'DP900N1200TU104204']
        Thread.__init__(self)
        self.camera_matrix = np.array([[3.81, 0, 2.018], [0, 3.81, 2.018], [0, 0, 1]])
        self.camera_distance = 864.0
        self.camera_distance_2 = 100000.0
        self.sensor_width = 4.54
        self.sensor_height = 3.4565
        self.focal_length = 3.916
        self.cap = 0
        return None
    def run(self):
        global box_x
        global box_y
        global terminateFlag
        global takePicFlag
        global img_points
        
        camera_event.wait()
        
        self.cap, square_flag = self.startVideo("Run")
        self.B,self.G,self.R = (100, 100, 200)
        
        ret, img = self.cap.read()
        cv.waitKey(1)
        print(img.shape)
        
        fromCenter = False
        r = cv.selectROI("Select region of interest", img, fromCenter)
        print(r)
        img_points = self.floodFill(img, r)
        cv.imshow("Original image", img)
        print(img.shape)
        
        while True:
            camera_event.wait()
            try:
                #cv.imwrite("Original image.png", img)
                ret, img_show = self.cap.read()
                cv.imshow("Live camera feed", img_show)
                #cv.imshow("Background image", img_bg)
                #cv.imwrite("C:/Users/Viktor From/OneDrive/Kandidat/Kandidatprojekt/02 - Code/01 - Samples/Original image", img)
                #h, w, c = img.shape
               # cv.imshow("Cropped image", img_cropped)
            except:
                print("Couldn't show original image")
                img = 0
            if takePicFlag == 1:
                r = [0,0,0,0]
                ret, second_img = self.cap.read()
                cv.imshow("Close up", second_img)
                img_points = self.floodFill(second_img, r)
                takePicFlag = 0
            cv.waitKey(1)
            #print(img_points)
            if terminateFlag == 1:
                break
        self.cap.release()
        cv.destroyAllWindows()
    
        
    def startVideo(self, run):
        if run == "Run":
            try:
               cap = cv.VideoCapture(0, cv.CAP_DSHOW)
               cap.set(cv.CAP_PROP_AUTOFOCUS, 0.32)
               cap.set(cv.CAP_PROP_BRIGHTNESS, 0) 
               cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
               cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
               #cap.set(cv.CAP_PROP_AUTO_EXPOSURE, 1.0)
               time.sleep(1)
            except:
                print("Couldn't access camera")
        elif run == "Test":
            #cap = cv.VideoCapture("C:/Users/Viktor From/OneDrive/Kandidat/Kandidatprojekt/04 - Tests/Test video 5 IGBT.mp4")
            cap = cv.imread("C:/Users/Viktor From/OneDrive/Kandidat/Kandidatprojekt/02 - Code/Robot control sandbox/sandbox_v.1.5/Viktor From/Original image.PNG")
        square_flag = 0
        return cap, square_flag
    
    def floodFill(self, img, r):
        global img_points
        orig_img = img
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        image_cropped = gray[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        print(image_cropped.shape)
        _, threshold = cv.threshold(image_cropped, 200, 255, cv.THRESH_BINARY)
        
        cv.imwrite("Threshold floodfill.png", threshold)
        
        M,N = threshold.shape
        
        n_objects = 0
        for i in range(M):
            for j in range(N):
                if threshold[i, j] == 255:
                    n_objects += 1
                    cv.floodFill(threshold, None, (j, i), n_objects)
        cv.imshow("Flood fill", threshold)
        contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        largest_contours = sorted(contours, key = cv.contourArea, reverse = True)[0:5]
        img_points = []
        for c in range(len(largest_contours)):
            #print("Drawing boxes")
            rect = cv.minAreaRect(largest_contours[c])
            box = cv.boxPoints(rect)
            box = np.int0(box)
            box_x, box_y, box_w, box_h = cv.boundingRect(box)
            img_rect = cv.drawContours(orig_img, [box], 0, (255, 0, 0), offset = (r[0], r[1]), thickness = 2)
            img_points.append([box[0][0]+r[0], box[0][1]+r[1], box_w, box_h])
        cv.imshow("Rectangles", img_rect)
        cv.imwrite("Rectangles floodfill.png", img_rect)
        return img_points
            
    def detectBoxes(self, im):
        global box_x, box_y, box_w, box_h
        im = cv.resize(im, (0, 0), fx=0.8, fy=0.8)
        im = cv.bilateralFilter(im,7,20,20) #Smoothing filter to remove noiseq
#im = im[800:1800, 800:1800
        gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        cv.imshow("Gray", gray)
        cv.imwrite("Gray.png", gray)
        template = cv.resize(cv.imread("C:/Users/Viktor From/OneDrive/Kandidat/Kandidatprojekt/02 - Code/Robot control sandbox/sandbox_v.1.5/Viktor From/Template image.PNG", 0), (0, 0), fx=0.8, fy=0.8)
        h, w = template.shape

        methods = [cv.TM_CCOEFF]

        for method in methods:
            img2 = gray.copy()

            result = cv.matchTemplate(img2, template, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                location = min_loc
            else:
                location = max_loc
            bottom_right = (location[0] + w, location[1] + h)    
            cv.rectangle(img2, location, bottom_right, 255, 5)
            cv.imshow('Match', img2)
            cv.imwrite("Match.png", img2)
        grayCrop = gray[location[1]:location[1]+h,location[0]:location[0]+w]
        #imCrop = gray[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        #imCrop = gray[236:236+122,241:241+240] #Offsets found manually.
        
        _, threshold= cv.threshold(grayCrop, 200, 255, cv.THRESH_BINARY)
        cv.imwrite("Threshold image.png", threshold)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
        d_im = cv.dilate(threshold, kernel, iterations=0)
        e_im = cv.erode(d_im, kernel, iterations=0) 
        cv.imshow("Eroded image", e_im)
        cv.imwrite("Eroded image.png", e_im)
        contours_list, hierarchy = cv.findContours(e_im, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE, hierarchy = 1)  # Find contours
        largest_contours = sorted(contours_list, key = cv.contourArea, reverse = True)[0:5]
        img_points = []
        for c in range(len(largest_contours)):
            #print("Drawing boxes")
            rect = cv.minAreaRect(largest_contours[c])
            box = cv.boxPoints(rect)
            box = np.int0(box)
            box_x, box_y, box_w, box_h = cv.boundingRect(box)
            img_rect = cv.drawContours(im, [box], 0, (0, 0, 255), 2, offset=(location[0], location[1]))
            img_rect = cv.drawMarker(im, (location[0]-int(box_x/4),location[1]-int(box_y/4)), markerType = cv.MARKER_CROSS, markerSize = 20, thickness = 1, line_type = 8, color=(0,255,0))
            img_points.append([box_x, box_y, box_w, box_h])
            #img_rect = cv.cvtColor(img_rect, cv.COLOR_GRAY2RGB)
            cv.imshow("Threshold", threshold)
            cv.imwrite("Threshold.png", threshold)
            cv.imshow("Detected rectangles", img_rect)
            cv.imwrite("Detected rectangles.png", img_rect)
            if takePicFlag == 1:
                ret, img2 = self.cap.read()
                #self.cap.release()
                cv.imshow("Second picture", img2)
                cv.imwrite("Second picture.png", img2)
                im = cv.bilateralFilter(img2,7,20,20) #Smoothing filter to remove noise
#im = im[800:1800, 800:1800
                gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
                '''fromCenter = False
                r = cv.selectROI("Image", gray2, fromCenter)
                print(r)'''
                #imCrop2 = gray2[125:125+94,254:254+229] #Offsets found manually.
                #cv.imwrite("Cropped image.png", imCrop2)
            
                for method in methods:
                    img2_copy = gray2.copy()

                    result = cv.matchTemplate(img2_copy, template, method)
                    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
                    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                        location = min_loc
                    else:
                        location = max_loc
                    bottom_right = (location[0] + w, location[1] + h)    
                    cv.rectangle(img2_copy, location, bottom_right, 255, 5)
                    cv.imshow('Match', img2)
                    cv.imwrite("Match.png", img2)
                gray2Crop = gray[location[1]:location[1]+h,location[0]:location[0]+w]
                _, threshold= cv.threshold(gray2Crop, 200, 255, cv.THRESH_BINARY)
                cv.imshow("Threshold second image", threshold)
                cv.imwrite("Threshold second image.png", threshold)
                kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
                d_im = cv.dilate(threshold, kernel, iterations=0)
                e_im = cv.erode(d_im, kernel, iterations=0) 
                cv.imshow("Eroded image", e_im)
                contours_list, hierarchy = cv.findContours(e_im, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE, hierarchy = 1)  # Find contours
                largest_contours = sorted(contours_list, key = cv.contourArea, reverse = True)[0:5]
        #imCrop = gray[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                for c in range(len(largest_contours)):
                    rect = cv.minAreaRect(largest_contours[c])
                    box = cv.boxPoints(rect)
                    box = np.int0(box)
                    box_x, box_y, box_w, box_h = cv.boundingRect(box)
                    img_points.append([box_x, box_y, box_w, box_h])
                    #print(img_points)
                    img_rect = cv.drawContours(im, [box], 0, (0, 0, 255), 2, offset=(location[0], location[1]))
                    #img_rect = cv.line(img_rect, pt1=(int(box_x/4)-5, int(box_y/4)-5), pt2 =(int(box_x/4)+5, int(box_y/4)+5), color=(0, 255, 0), thickness=5, lineType=8, shift=0)
                    img_rect = cv.drawMarker(img2, (location[0]+int(box_x/4),location[1]+int(box_y/4)), markerType = cv.MARKER_CROSS, markerSize = 20, thickness = 1, line_type = 8, color = (0,255,0))
                    cv.imshow("Second detected rectangles", img_rect)
                    cv.imwrite("Second detected rectangles.png", img_rect)
        return img_points


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
            global text
            global FSR_voltage
            global distance_measured
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
                print("Distance")
                distance_measured = int(float(split[1].replace(',', '')))
                print(distance_measured)
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
        
        
class Oscilloscope(Thread):
    def __init__(self, voltages):
        Thread.__init__(self)
        self.voltages = voltages
        rm = pyvisa.ResourceManager()
        print(rm.list_resources('?*'))
        try:
            self.inst = rm.open_resource('TCPIP0::192.168.11.8::inst0::INSTR', read_termination='\n')
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
            voltages = self.voltages
            #qprint(voltages)
            if(voltages > str(1)):
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
            if terminateFlag == 1:
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
    
    

#robotcontrol = ctypes.CDLL("C:/Users/Near-field scanner/Documents/Near_Field_Scanner_GUI/sandbox/Near-Field_Scanner_GUI_v3.3/Near-Field_Scanner_GUI/TCP_IP/Robot/robot.cpp")

camera_video = Video(text)
robot_control = Robot_TCP_comm()
arduino_control = Arduino(cleandata, text, voltages, button_state)
oscilloscope = Oscilloscope(voltages)
interface = Interface()


#ret, mtx, dist, rvecs, tvecs = calibrateCamera()
#print(rvecs)
interface.start()
camera_video.start()
robot_control.start()
arduino_control.start()
oscilloscope.start()

robot_control.join()
camera_video.join()
arduino_control.join()
oscilloscope.join()
interface.join()
