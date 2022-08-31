# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 10:37:25 2022

@author: Viktor From
"""

'''
Created 26-08-2022

Taken from here: https://pythonbasics.org/pyqt-buttons/

'''

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import cv2 as cv
import numpy as np
import random as rng
global cameraStart
global cameraStop
import argparse
import time
from threading import Thread
cameraStart = 0
cameraStop = 0

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
       button2.setText("Button2")
       button2.move(64,64)
       button2.clicked.connect(self.button2_clicked)

       widget.setGeometry(50,50,320,200)
       widget.setWindowTitle("PyQt5 Button Click Example")
       widget.show()
       sys.exit(app.exec_())


    def button1_clicked(self):
        global cameraStart
        print("Button 1 clicked")
        cameraStart = 1

    def button2_clicked(self):
        global cameraStop
        print("Button 2 clicked") 
        cameraStop = 1

class Segmentation(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        parser = argparse.ArgumentParser(description='Code for Image Segmentation with Distance Transform and Watershed Algorithm.\
            Sample code showing how to segment overlapping objects using Laplacian filtering, \
            in addition to Watershed and Distance Transformation')
        parser.add_argument('--input', help='Path to input image.', default="C:/Users/Viktor From/OneDrive/Kandidat/Kandidatprojekt/02 - Code/01 - Samples/822 mm height above table.jpg")
        args = parser.parse_args()
        while cameraStart == 0:
            pass
        first_image = cv.resize(cv.imread(cv.samples.findFile(args.input)), (620,460))
        gray = cv.cvtColor(first_image, cv.COLOR_BGR2GRAY)

        if first_image is None:
            print('Could not open or find the image:', args.input)
            exit(0)
        # Show source image

        cv.imshow('First image', first_image)
        fromCenter = False
        r = cv.selectROI("Select region of interest", first_image, fromCenter)
        print(r)
        first_image = first_image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
        self.watershed(first_image)
        cv.waitKey()
        second_image = cv.resize(cv.imread("102 mm height above table.jpg"), (620, 460))
        cv.imshow("Second image", second_image)
        self.watershed(second_image)
        while cameraStop == 0:
            time.sleep(0.1)
            if cameraStop == 1:
                cv.destroyAllWindows()
    
    def watershed(self, img):
        img[np.all(img == 255, axis=2)] = 0
        # Show output image
        cv.imshow('Black Background Image', img)
        kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=np.float32)
        # do the laplacian filtering as it is
        # well, we need to convert everything in something more deeper then CV_8U
        # because the kernel has some negative values,
        # and we can expect in general to have a Laplacian image with negative values
        # BUT a 8bits unsigned int (the one we are working with) can contain values from 0 to 255
        # so the possible negative number will be truncated
        imgLaplacian = cv.filter2D(img, cv.CV_32F, kernel)
        sharp = np.float32(img)
        imgResult = sharp - imgLaplacian
        # convert back to 8bits gray scale
        imgResult = np.clip(imgResult, 0, 255)
        imgResult = imgResult.astype('uint8')
        imgLaplacian = np.clip(imgLaplacian, 0, 255)
        imgLaplacian = np.uint8(imgLaplacian)
        #cv.imshow('Laplace Filtered Image', imgLaplacian)
        #cv.imshow('New Sharped Image', imgResult)
        bw = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        _, bw = cv.threshold(bw, 200, 255, cv.THRESH_BINARY)
        cv.imshow('Binary Image', bw)
        cv.imwrite("Binary image.png", bw)
        kernel1 = np.ones((3,3), dtype=np.uint8)
        opening = cv.morphologyEx(bw, cv.MORPH_OPEN, kernel, iterations=8)
        cv.imshow('Opened image', opening)
        	## After opening, will perform dilation
        sure_bg = cv.dilate(opening, kernel, iterations=8)
        dist = cv.distanceTransform(bw, cv.DIST_L2, 3)
        # Normalize the distance image for range = {0.0, 1.0}
        # so we can visualize and threshold it
        cv.normalize(dist, dist, 0, 1.0, cv.NORM_MINMAX)
        cv.imshow('Distance Transform Image', dist)
        _, dist = cv.threshold(dist, 0.5, 1.0, cv.THRESH_BINARY)
        # Dilate a bit the dist image
        kernel1 = np.ones((3,3), dtype=np.uint8)
        opening = cv.morphologyEx(dist, cv.MORPH_OPEN, kernel, iterations=5)
        cv.imshow('Open', opening)
        	## After opening, will perform dilation
        sure_bg = cv.dilate(opening, kernel, iterations=5)
        cv.imshow('Peaks', dist)
        dist_8u = dist.astype('uint8')
        # Find total markers
        contours, _ = cv.findContours(dist_8u, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # Create the marker image for the watershed algorithm
        markers = np.zeros(dist.shape, dtype=np.int32)
        # Draw the foreground markers
        for i in range(len(contours)):
            cv.drawContours(markers, contours, i, (i+1), -1)
        # Draw the background marker
        cv.circle(markers, (5,5), 3, (255,255,255), -1)
        markers_8u = (markers * 10).astype('uint8')
        cv.imshow('Markers', markers_8u)
        cv.watershed(img, markers)
        #mark = np.zeros(markers.shape, dtype=np.uint8)
        mark = markers.astype('uint8')
        mark = cv.bitwise_not(mark)
        # uncomment this if you want to see how the mark
        # image looks like at that point
        #cv.imshow('Markers_v2', mark)
        # Generate random colors
        colors = []
        for contour in contours:
            colors.append((rng.randint(0,256), rng.randint(0,256), rng.randint(0,256)))
        # Create the result image
        dst = np.zeros((markers.shape[0], markers.shape[1], 3), dtype=np.uint8)
        # Fill labeled objects with random colors
        for i in range(markers.shape[0]):
            for j in range(markers.shape[1]):
                index = markers[i,j]
                if index > 0 and index <= len(contours):
                    dst[i,j,:] = colors[index-1]
        # Visualize the final image
        cv.imshow('Final Result', dst)
        dst = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
        contours, _ = cv.findContours(dst, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        largest_contours = sorted(contours, key = cv.contourArea, reverse = True)[0:5]
        img_points = []
        for c in range(len(largest_contours)):
            #print("Drawing boxes")
            rect = cv.minAreaRect(largest_contours[c])
            box = cv.boxPoints(rect)
            box = np.int0(box)
            box_x, box_y, box_w, box_h = cv.boundingRect(box)
            img_rect = cv.drawContours(img, [box], 0, (0, 0, 255))
            img_points.append([box_x, box_y, box_w, box_h])
        cv.imshow("Rectangles", img_rect)
        return img_points
    

if __name__ == '__main__':
   
  interface = Interface()
  segment = Segmentation() 
  
  interface.start()
  segment.start()
  
  interface.join()
  segment.join()