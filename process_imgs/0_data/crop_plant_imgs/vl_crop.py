# vl_crop.py
# Austin Pursley
# 7/20/2018
# Help with automatically cropping visible light plant images.
# Some images still required manually cropping

import cv2 as cv
import numpy as np
import os
from matplotlib import pyplot as plt

idir = "uncropped"
odir = "cropped/"
redo_file_list = open("redo_crop.txt", "w")
# i = 0
for file in os.listdir(idir):
    file_dir = idir + file
    if file.endswith(".jpg"):
        # Image processing
        img = cv.imread(file_dir, -1)
        blur = cv.bilateralFilter(img, 5, 75, 75) #blur reduces noise
        hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
		lower_green = np.array([30, 20, 23]) #thresh values found experimentally
        upper_green = np.array([50, 255, 150])
        mask = cv.inRange(hsv, lower_green, upper_green)
        kernel = np.ones((15,15),np.uint8) #morphology adjusts mask
        opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        kernel = np.ones((100,100),np.uint8)
        dilate = cv.morphologyEx(opening, cv.MORPH_DILATE, kernel)
        kernel = np.ones((50, 50), np.uint8)
        dilate = cv.morphologyEx(dilate, cv.MORPH_ERODE, kernel)
        res =cv.bitwise_and(img, img, mask= mask)
        im2, contours, hier = cv.findContours(dilate, cv.RETR_EXTERNAL,2)
        if contours:
			# Use biggest contour to get crop ROI
            c = max(contours, key = cv.contourArea)
            x,y,w,h = cv.boundingRect(c)
            roi = img[y:y+h, x:x+w]
            cv.rectangle(res,(x,y),(x+w,y+h),(0,255,0),2)
			# Output Results
            file_name = odir + "_0_orig" + file
            cv.imwrite(file_name, img)
            file_name = odir + "_1_mask" + file
            cv.imwrite(file_name, mask)
            file_name = odir + file
            cv.imwrite(file_name, roi)

            # Display
            # cv.namedWindow('img',cv.WINDOW_NORMAL)
            # cv.resizeWindow('img', 1024, 768)
            # cv.imshow('img', img)
            # cv.namedWindow('mask',cv.WINDOW_NORMAL)
            # cv.resizeWindow('mask', 1024, 768)
            # cv.imshow('mask', mask)
            # cv.namedWindow('open',cv.WINDOW_NORMAL)
            # cv.resizeWindow('open', 1024, 768)
            # cv.imshow('open', roi)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
			
			# Reject and Accept Images when program is running
			# (didn't quite get this part right)
            # fb = -1
            # while (fb != 1) & (fb != 0):
            #     try:
            #         fb = int(raw_input("Accpet: 1, Reject: 0: "))
            #     # not an integer
            #     except ValueError:
            #         print("not an int")
            #     if fb == 1:
            #         odir = "output/"
            #         file_name = odir + str(i) + "_0_.jpg"
            #         cv.imwrite(file_name, img)
            #         # file_name = odir + str(i) + "_1_mask.jpg"
            #         # cv.imwrite(file_name, mask)
            #         # file_name = odir + "roi_" + file
            #         # cv.imwrite(file_name, roi)
            #         i += 1
            #     elif fb == 0:
            #         redo_file_list.write(file_dir + "\n")
        else:
            print file + " RESULTED IN EMPTY CONTOUR"
redo_file_list.close()