import cv2 as cv
from read_pgm import read_pgm
import numpy as np
from matplotlib import pyplot as plt
# Original, un-normalized image
img_name = '0607135153_IR_IMG_0006_top.pgm'
print img_name
img = cv.imread(img_name, -1)
height, width = img.shape
print "min: ", img.min()
print "max: ", img.max()
# Normalize img to be 8-bit for displaying
normalizedImg = np.zeros((60, 80))
normalizedImg = cv.normalize(img, normalizedImg, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)
# Apply threshold in lower and upper bounds.
p = cv.inRange(img, 8162, 8180)
normalizedP = np.zeros((60, 80))
normalizedP = cv.normalize(p, normalizedP, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)
# Caluculate the average of thresolded area
print "plant averge: ", cv.mean(img, normalizedP)
# Calculated calibration equation
Fdegree_img = -0.00000608*np.float_power(img,2) + 0.1715806300*img - 920.665168
print "min (F degree): ", Fdegree_img.min()
print "max (F degree): ", Fdegree_img.max()
print "Plant (F degree): ", cv.mean(Fdegree_img, normalizedP)
# Display
cv.namedWindow('image',cv.WINDOW_NORMAL)
cv.resizeWindow('image', 600, 600)
cv.namedWindow('image4',cv.WINDOW_NORMAL)
cv.resizeWindow('image4', 600, 600)
cv.imshow('image', normalizedImg)
cv.imshow('image4', p)
cv.waitKey(0)
cv.destroyAllWindows()