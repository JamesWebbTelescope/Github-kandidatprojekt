# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 08:49:11 2022

@author: Near-field scanner
"""

import cv2 as cv
from threading import Thread
import numpy as np
import Settings
import Convert
import time
import matplotlib as plt

class Video(Thread):
    def __init__(self, text):
        self.text = text
        self.model = []
        self.class_names = ['DP700B750T105518', 'DP900N1200TU104204']
        Thread.__init__(self)
        self.camera_matrix = np.array([[3.81, 0, 2.018], [0, 3.81, 2.018], [0, 0, 1]])
        self.camera_distance_2 = 100000.0
        self.sensor_width = 4.54
        self.sensor_height = 3.4565
        self.focal_length = 3.916
        self.cap = 0
        #self.cap, square_flag = self.startVideo(text)
        return None
    def run(self):
        global box_x
        global box_y
        global terminateFlag
        global takePicFlag
        global img_points
        
        img, square_flag = self.startVideo(self.text)
        
        while True:
            Settings.camera_event.wait()
        
            self.B,self.G,self.R = (100, 100, 200)
            
            #ret, img = self.cap.read()
            cv.waitKey(1)
            print(img.shape)
        
            fromCenter = False
            r = cv.selectROI("Select region of interest", img, fromCenter)
            print("Here rectangle", r)
            Settings.img_points = self.floodFill(img, r)
            #print(r)
            #print(Settings.img_points)
            #cv.imshow("Original image", img)
            print(img.shape)
            #Settings.img_points.append([r[0],r[1],r[2],r[3]])
            #for i in range(len(img_points)):
            rxp, ryp = Convert.Convert.findDistance(img_points[0][0], img_points[0][1])
            Settings.rx_mm, Settings.ry_mm = Convert.Convert.convertPixeltoMM(rxp, ryp)
            print("Rectangles mm", Settings.rx_mm, Settings.ry_mm)
            '''ret, img_show = self.cap.read()
            cv.imshow("Live camera feed", img_show)'''
            if Settings.terminateFlag == 1:
                break
        self.close()
        
        '''while True:
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
                break'''
    
        
    def startVideo(self, run):
        if run == "Run":
            try:
               cap = cv.VideoCapture(0, cv.CAP_DSHOW)
               cap.set(cv.CAP_PROP_AUTOFOCUS, Settings.autofocus)
               cap.set(cv.CAP_PROP_BRIGHTNESS, Settings.auto_brightness) 
               cap.set(cv.CAP_PROP_FRAME_WIDTH, Settings.img_width)
               cap.set(cv.CAP_PROP_FRAME_HEIGHT, Settings.img_height)
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
        largest_contours = sorted(contours, key = cv.contourArea, reverse = True)[0:1]
        img_points = []
        for c in range(len(largest_contours)):
            #print("Drawing boxes")
            rect = cv.minAreaRect(largest_contours[c])
            box = cv.boxPoints(rect)
            box = np.int0(box)
            box_x, box_y, box_w, box_h = cv.boundingRect(box)
            img_rect = cv.drawContours(orig_img, [box], 0, (255, 0, 0), offset = (r[0], r[1]), thickness = 2)
            img_points.append([box[0][0]+r[0], box[0][1]+r[1], box_w, box_h])
            for i in box:
                cv.circle(orig_img,(i[0]+r[0],i[1]+r[1]), 3, (0,255,0), -1)
                cv.imshow("Corner nr " + str(i), orig_img)
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
    
    def close(self):
        self.cap.release()
        cv.destroyAllWindows()
