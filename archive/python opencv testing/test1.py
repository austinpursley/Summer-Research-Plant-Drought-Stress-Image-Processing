import cv2 as cv
from read_pgm import read_pgm
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('IR_IMG_0000.pgm', -1)
ret,thresh1 = cv.threshold(img,8000,img[0].max(),cv.THRESH_BINARY)
normalizedImg = np.zeros((60, 80))
normalizedImg = cv.normalize(thresh1, normalizedImg, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)
height, width = normalizedImg.shape
print height, width
#cv.imshow('image', img)
print img[0].min()
print normalizedImg[0].max()
#cv.namedWindow('image',cv.WINDOW_NORMAL)
#cv.resizeWindow('image', 600, 600)
cv.namedWindow('image2',cv.WINDOW_NORMAL)
cv.resizeWindow('image2', 600, 600)
#cv.imshow('image', normalizedImg)
cv.imshow('image2', normalizedImg)
cv.waitKey(0)
cv.destroyAllWindows()