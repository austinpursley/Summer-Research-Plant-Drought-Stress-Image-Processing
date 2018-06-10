import cv2 as cv
from read_pgm import read_pgm
import numpy as np
from matplotlib import pyplot as plt

# Original, unormalized image
img = cv.imread('0607141501_IR_IMG_0004.pgm', -1)
height, width = img.shape
print height, width
print "min: ", img.min()
print "max: ", img.max()
# Normalize img to be 8-bit for displaying
normalizedImg = np.zeros((60, 80))
normalizedImg = cv.normalize(img, normalizedImg, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)
# Apply threshold, normalize for displaying
# Cold
ret,thresh1 = cv.threshold(img,7625,img[0].max(),cv.THRESH_BINARY_INV)
normalizedThreshImg = np.zeros((60, 80))
normalizedThreshImg = cv.normalize(thresh1, normalizedThreshImg, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)
# Hot
ret,thresh2 = cv.threshold(img,9000,img[0].max(),cv.THRESH_BINARY)
normalizedThreshImg2 = np.zeros((60, 80))
normalizedThreshImg2 = cv.normalize(thresh2, normalizedThreshImg2, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)
#Background
bg_not = cv.bitwise_or(normalizedThreshImg, normalizedThreshImg2)
bg = cv.bitwise_not(bg_not)
normalizedBgImg = np.zeros((60, 80))
normalizedBgImg = cv.normalize(bg, normalizedBgImg, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)

# Caluculate the average of thresolded area
#print "thresh avg: ", cv.mean(img, normalizedThreshImg)
#print "thresh avg: ", cv.mean(img, normalizedThreshImg2)
print "bg average: ", cv.mean(img, normalizedBgImg)

# Calculated calibration equation
Fdegree_img = -0.00000608*np.float_power(img,2) + 0.1715806300*img - 920.665168
print "F degrees min: ", Fdegree_img.min()
print "F degrees max: ", Fdegree_img.max()
print "F degree cold avg: ", cv.mean(Fdegree_img, normalizedThreshImg)
print "F degree hot avg 2: ", cv.mean(Fdegree_img, normalizedThreshImg2)
print "F degree background: ", cv.mean(Fdegree_img, normalizedBgImg)
# Display
cv.namedWindow('image',cv.WINDOW_NORMAL)
cv.resizeWindow('image', 600, 600)
cv.namedWindow('image2',cv.WINDOW_NORMAL)
cv.resizeWindow('image2', 600, 600)
cv.namedWindow('image3',cv.WINDOW_NORMAL)
cv.resizeWindow('image3', 600, 600)
cv.namedWindow('image4',cv.WINDOW_NORMAL)
cv.resizeWindow('image4', 600, 600)
cv.imshow('image', normalizedImg)
cv.imshow('image2', normalizedThreshImg)
cv.imshow('image3', normalizedThreshImg2)
cv.imshow('image4', normalizedBgImg)
cv.waitKey(0)
cv.destroyAllWindows()