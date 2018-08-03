# ir_crop.py
# Austin Pursley
# 7/20/2018
# Help with automatically cropping inafred/thermal plant images
# Some images still required manually cropping

import cv2 as cv
import numpy as np
import os
from matplotlib import pyplot as plt

i = 0
# dir = "data/plant_imgs/"
dir = 'data/plant_imgs/'
odir = "output/"
for file in os.listdir(dir):
    file_dir = dir + file
    if file.endswith("top.pgm"):
        # Image processing
        img = cv.imread(file_dir, -1)
        normalizedImg = np.zeros((60, 80)) # Normalize img to be 8-bit for displaying
        normalizedImg = cv.normalize(img, normalizedImg, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)
		y, h, x, w = 5, 50, 10, 50
        crop_img = normalizedImg[y:y + h, x:x + w] # Start small crop
        range = img.max()-img.min()
        lower = int(img.min())
        upper = int(img.max() - 0.80*range)
        ret, th = cv.threshold(crop_img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
        th = cv.bitwise_not(th)
        kernel = np.ones((2, 2), np.uint8)
        morph = cv.morphologyEx(th, cv.MORPH_OPEN, kernel)
        im2, contours, hier = cv.findContours(morph, cv.RETR_EXTERNAL,2, offset=((x-1),(y-1)))
        if contours:
			# Use largest contour for crop ROI
            c = max(contours, key = cv.contourArea)
            x,y,w,h = cv.boundingRect(c)
            masked_img = np.zeros((60, 80))
            cv.drawContours(masked_img, [c], 0, 255, -1)
            roi = normalizedImg[y:y + h, x:x + w]
			# Output
            # print "upper: ", upper
            # print "lower: ", lower
            # print "norm min: ", th.min()
            # print "norm max: ", th.max()
            jpg_img_name = odir + file[:-4] + "_0_orignorm" + ".jpg"
            cv.imwrite(jpg_img_name, normalizedImg)
            mask_img_name = odir + file[:-4] + "_1_mask" + ".jpg"
            cv.imwrite(mask_img_name, masked_img)
            # file_name = odir + file
            # file_name = file_name[:-4] + "_3_cropped.jpg"
            # cv.imwrite(file_name, roi)
        else:
            print file + " RESULTED IN EMPTY CONTOUR"