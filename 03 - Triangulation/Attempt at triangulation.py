# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 08:07:22 2022

@author: Viktor From
"""

import cv2 as cv
import numpy as np

img_width = 640 #Width of the images taken in pixels
img_height = 480 #Height of the images taken in pixels
camera_distance = 833.0 #The distance of the camera above the table
camera_distance_2 = 100.0 #Deprecated
sensor_width = 4.54 #The camera onstants
sensor_height = 3.4565
focal_length = 3.916
focal_length = 3.916
b = 10

def floodFill(img, r):
    global img_points
    orig_img = img
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #Convert to grayscale
    image_cropped = gray[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])] #Crop the image
    print(image_cropped.shape)
    _, threshold = cv.threshold(image_cropped, 200, 255, cv.THRESH_BINARY) #Convert to binary
    
    cv.imwrite("Threshold floodfill.png", threshold)
    
    M,N = threshold.shape
    
    n_objects = 0 #Apply thresholding ot the entire image
    for i in range(M):
        for j in range(N):
            if threshold[i, j] == 255:
                n_objects += 1
                cv.floodFill(threshold, None, (j, i), n_objects)
    cv.imshow("Flood fill", threshold)
    contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) #Detect contours in the resulting image
    largest_contours = sorted(contours, key = cv.contourArea, reverse = True)[0:5] #Sort the contours by their area and only keep the five biggest
    img_points = []
    for c in range(len(largest_contours)): 
        #print("Drawing boxes")
        rect = cv.minAreaRect(largest_contours[c])
        box = cv.boxPoints(rect)
        box = np.int0(box)
        box_x, box_y, box_w, box_h = cv.boundingRect(box)
        img_rect = cv.drawContours(orig_img, [box], 0, (255, 0, 0), offset = (r[0], r[1]), thickness = 2)
        target_x = box_x+int(box_w/3)+r[0]
        target_y = box_y+int(box_h/3)+r[1]
        img_points.append([target_x, target_y])
        cv.circle(orig_img,(box_x+int(box_w/3)+r[0],box_y+int(box_h/3)+r[1]), 3, (0,255,0), -1)
        cv.imshow("Target nr " + str(c), orig_img)
        cv.imwrite("Target nr " + str(c) + ".png", orig_img)
        '''for i in box:
            corners = corners + 1
            cv.circle(orig_img,(i[0]+r[0],i[1]+r[1]), 3, (0,255,0), -1)
            cv.imshow("Corner nr " + str(corners), orig_img)'''
    cv.imshow("Rectangles", img_rect)
    cv.imwrite("Rectangles floodfill.png", img_rect)
    return img_points

if __name__ == "__main__":

    img1 = cv.imread("First picture triangulation (0,0,0).jpg")
    img2 = cv.imread("Second picture triangulation (-10 mm, 0, 0).jpg")
    img1 = cv.resize(img1, (640,480))
    img2 = cv.resize(img2, (640, 480))

    fromCenter = False
    r1 = cv.selectROI("Select region of interest", img1, fromCenter) #Prompt the user to indicate where the region of interest is in the image.
    print("Here rectangle", r1)
    r2 = cv.selectROI("Select region of interest", img2, fromCenter) #Prompt the user to indicate where the region of interest is in the image.
    print("Here rectangle", r2)
    
    img_points1 = floodFill(img1, r1)
    img_points2 = floodFill(img2, r2)
    
    for i in range(len(img_points2)):
        diff = img_points2[i][0] - img_points1[i][0]
        diff = float((camera_distance*diff*sensor_width)/(focal_length*img_width));
        z = (focal_length*b)/diff
        print(z)
    
    
    cv.waitKey()
    cv.destroyAllWindows()