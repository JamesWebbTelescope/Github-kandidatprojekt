# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 17:23:21 2022

@author: Viktor From
"""

import cv2 
import numpy as np

image = cv2.resize(cv2.imread("C:/Users/Viktor From/OneDrive/Kandidat/Kandidatprojekt/02 - Code/01 - Samples/822 mm height above table.jpg"), (640, 520))
image2 = cv2.resize(cv2.imread("C:/Users/Viktor From/OneDrive/Kandidat/Kandidatprojekt/02 - Code/01 - Samples/202 mm height above table.jpg"), (640, 520))

fromCenter = False
r = cv2.selectROI("Select region of interest", image, fromCenter)
print(r)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

image_cropped = gray[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
_, threshold = cv2.threshold(image_cropped, 230, 255, cv2.THRESH_BINARY)

cv2.imwrite("Threshold floodfill.png", threshold)

M,N = threshold.shape

n_objects = 0
for i in range(M):
    for j in range(N):
        if threshold[i, j] == 255:
            n_objects += 1
            cv2.floodFill(threshold, None, (j, i), n_objects)
cv2.imshow("Flood fill", threshold)
cv2.imwrite("Flood fill.png", threshold)

contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest_contours = sorted(contours, key = cv2.contourArea, reverse = True)[0:5]
img_points = []
for c in range(len(largest_contours)):
    #print("Drawing boxes")
    rect = cv2.minAreaRect(largest_contours[c])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    box_x, box_y, box_w, box_h = cv2.boundingRect(box)
    img_rect = cv2.drawContours(image, [box], 0, (255, 0, 0), offset = (r[0], r[1]), thickness = 2)
    img_points.append([box_x, box_y, box_w, box_h])
cv2.imshow("Rectangles", img_rect)
cv2.imwrite("Rectangles floodfill.png", img_rect)

gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)


_, threshold = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)

cv2.imshow("Threshold second image", threshold)
cv2.imwrite("Threshold second image floodfill.png", threshold)

M,N = threshold.shape

n_objects = 0
for i in range(M):
    for j in range(N):
        if threshold[i, j] == 255:
            n_objects += 1
            cv2.floodFill(threshold, None, (j, i), n_objects)
cv2.imshow("Flood fill second image", threshold)
cv2.imwrite("Floodfill second image.png", threshold)

contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest_contours = sorted(contours, key = cv2.contourArea, reverse = True)[0:5]
img_points = []
for c in range(len(largest_contours)):
    #print("Drawing boxes")
    rect = cv2.minAreaRect(largest_contours[c])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    box_x, box_y, box_w, box_h = cv2.boundingRect(box)
    img_rect = cv2.drawContours(image2, [box], 0, (255, 0, 0), thickness = 2)
    img_points.append([box_x, box_y, box_w, box_h])
cv2.imshow("Rectangles second image", img_rect)
cv2.imwrite("Rectangles second image.png", img_rect)
cv2.waitKey(0)
cv2.destroyAllWindows()