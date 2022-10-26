# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 14:04:04 2022

@author: Viktor From

Taken from here: https://machinelearningknowledge.ai/image-segmentation-in-python-opencv/#Types_of_Image_Segmentation_Approaches

"""

import matplotlib as plt
import numpy as np
import cv2 as cv
from skimage.filters import threshold_otsu
import time
path = "C:/Users/Viktor From/OneDrive/Kandidat/Kandidatprojekt/02 - Code/01 - Samples/822 mm height above table.jpg"

def filter_image(image, mask):
    r = image[:,:,0] * mask
    g = image[:,:,1] * mask
    b = image[:,:,2] * mask
    return np.dstack([r,g,b])


img = cv.imread(path)

orig_img = cv.resize(img, (620, 480))

fromCenter = False
r = cv.selectROI("Select region of interest", orig_img, fromCenter)
print(r)

'''
Segmenting by K-Means
'''
img = orig_img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

start_time = time.time()

img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
twoDimage = img.reshape((-1,3))
twoDimage = np.float32(twoDimage)

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 3
attempts=100

ret,label,center=cv.kmeans(twoDimage,K,None,criteria,attempts,cv.KMEANS_PP_CENTERS)
center = np.uint8(center)
res = center[label.flatten()]
result_image = res.reshape((img.shape))


end_time = time.time()

print("The time of execution of k-means segmentation is :", (end_time-start_time) * 10**3, "ms")

#print(label)

cv.imshow("K-Means segmentation", result_image)
cv.imwrite("K-Means segmentation.png", result_image)

'''result_image  = cv.threshold(result_image, 0, 2, cv.THRESH_BINARY)

cv.imshow("Thresholded", result_image)'''

'''
Segmenting by contour detection
'''

start = time.time()

gray = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
_,thresh = cv.threshold(gray, np.mean(gray), 255, cv.THRESH_BINARY_INV)
edges = cv.dilate(cv.Canny(thresh,230,255),None)

cnt = sorted(cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[-2], key=cv.contourArea)[-1]
mask = np.zeros((r[3],r[2]), np.uint8)
masked = cv.drawContours(mask, [cnt],-1, 255, -1)

cv.imshow("Masked", masked)
cv.imwrite("Masked.png", masked)

dst = cv.bitwise_and(img, img, mask=mask)
segmented = cv.cvtColor(dst, cv.COLOR_BGR2RGB)

cv.imshow("Contour segmentation", segmented)
cv.imwrite("Contour segmentation.png", segmented)

end = time.time()

print("The time of execution of segmentation by contour detection is :",
      (end-start) * 10**3, "ms")

'''
Segmentation by thresholding
'''
start = time.time()

img_rgb=cv.cvtColor(img,cv.COLOR_BGR2RGB)
img_gray=cv.cvtColor(img_rgb,cv.COLOR_RGB2GRAY)

thresh = threshold_otsu(img_gray)
img_otsu  = img_gray < thresh
filtered = filter_image(img, img_otsu)

cv.imshow("Segmentation by thresholding", filtered)
cv.imwrite("Segmentation by thresholding.png", filtered)

end = time.time()

print("The time of execution of segmentation by thresholding is :", (end-start) * 10**3, "ms")

'''
Segmentation by color
'''

start = time.time()

rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
hsv_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2HSV)

light_blue = (90, 0.4*255, 0.7*255)
dark_blue = (255, 255, 255)
# You can use the following values for green
# light_green = (40, 40, 40)
# dark_greek = (70, 255, 255)
mask = cv.inRange(hsv_img, light_blue, dark_blue)

result = cv.bitwise_and(img, img, mask=mask)

cv.imshow("Color segmentation", result)
cv.imwrite("Color segmentation.png", result)

result = cv.cvtColor(result, cv.COLOR_RGB2GRAY)

end = time.time()

print("The time of execution of segmentation by color is :", (end-start) * 10**3, "ms")

contours, _ = cv.findContours(result, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
largest_contours = sorted(contours, key = cv.contourArea, reverse = True)[0:5]
img_points = []
for c in range(len(largest_contours)):
    #print("Drawing boxes")
    rect = cv.minAreaRect(largest_contours[c])
    box = cv.boxPoints(rect)
    box = np.int0(box)
    box_x, box_y, box_w, box_h = cv.boundingRect(box)
    img_rect = cv.drawContours(orig_img, [box], 0, (255, 0, 0), offset = (r[0], r[1]), thickness = 2)
    img_points.append([box_x, box_y, box_w, box_h])
cv.imshow("Rectangles", img_rect)
cv.imwrite("Rectangles color segmentation.png", img_rect)

path = "C:/Users/Viktor From/OneDrive/Kandidat/Kandidatprojekt/02 - Code/01 - Samples/102 mm height above table.jpg"

closeup_image = cv.imread(path)
closeup_image = cv.resize(closeup_image, (620, 480))

rgb_img = cv.cvtColor(closeup_image, cv.COLOR_BGR2RGB)
hsv_img = cv.cvtColor(rgb_img, cv.COLOR_RGB2HSV)

light_blue = (90, 0.4*255, 0.7*255)
dark_blue = (255, 255, 255)
# You can use the following values for green
# light_green = (40, 40, 40)
# dark_greek = (70, 255, 255)
mask = cv.inRange(hsv_img, light_blue, dark_blue)

result = cv.bitwise_and(closeup_image, closeup_image, mask=mask)

cv.imshow("Color segmentation closeup", result)

result = cv.cvtColor(result, cv.COLOR_RGB2GRAY)

contours, _ = cv.findContours(result, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
largest_contours = sorted(contours, key = cv.contourArea, reverse = True)[0:5]
img_points = []
for c in range(len(largest_contours)):
    #print("Drawing boxes")
    rect = cv.minAreaRect(largest_contours[c])
    box = cv.boxPoints(rect)
    box = np.int0(box)
    box_x, box_y, box_w, box_h = cv.boundingRect(box)
    img_rect = cv.drawContours(orig_img, [box], 0, (255, 0, 0), offset = (r[0], r[1]), thickness = 2)
    img_points.append([box_x, box_y, box_w, box_h])
cv.imshow("Rectangles closeup", img_rect)


cv.waitKey()
cv.destroyAllWindows()

