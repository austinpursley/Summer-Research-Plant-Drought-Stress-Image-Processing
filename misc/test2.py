import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Original, unormalized image
img = cv.imread('0530180000_IR_IMG_0003_front.pgm', -1)
height, width = img.shape
print height, width
print "min: ", img.min()
print "max: ", img.max()
# Normalize img to be 8-bit for displaying
normalizedImg = np.zeros((60, 80))
normalizedImg = cv.normalize(img, normalizedImg, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)
# Apply threshold, normalize for displaying
# Cold
ret,thresh1 = cv.threshold(img,8125,img[0].max(),cv.THRESH_BINARY_INV)
normalizedThreshImg = np.zeros((60, 80))
normalizedThreshImg = cv.normalize(thresh1, normalizedThreshImg, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)

# Calculated calibration equation
Fdegree_img = -0.00000608*np.float_power(img,2) + 0.1715806300*img - 920.665168
print "F degrees min: ", Fdegree_img.min()
print "F degrees max: ", Fdegree_img.max()
print "F degree cold avg: ", cv.mean(Fdegree_img, normalizedThreshImg)
# Display
cv.namedWindow('image',cv.WINDOW_NORMAL)
cv.resizeWindow('image', 600, 600)
cv.namedWindow('image2',cv.WINDOW_NORMAL)
cv.resizeWindow('image2', 600, 600)

cv.imshow('image', normalizedImg)
cv.imshow('image2', normalizedThreshImg)
cv.waitKey(0)
cv.destroyAllWindows()