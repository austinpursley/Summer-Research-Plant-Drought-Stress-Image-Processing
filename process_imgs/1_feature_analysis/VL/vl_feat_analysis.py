# vl_feat_analysis.py
# Austin Pursley
# 8/3/2018
# Finding hue of plants and seeing how that feature changes over time.
# Looking at hue mean and hue variance

import cv2 as cv
import numpy as np
import os
from datetime import datetime
from matplotlib import pyplot as plt
from numpy import array

i = 0
dir = "C:/Users/Austin Pursley/Projects/Summer-Research-Plant-Drought-Stress-Computer-Vision/process_imgs/0_data/crop_plant_imgs/cropped/VL/top/"
odir = "output/"
avg_hue = [[],[],[],[],[],[]]
var_hue = [[],[],[],[],[],[]]
dates = [[],[],[],[],[],[]]
hours = [[],[],[],[],[],[]]
then = datetime(year=2018, month=5, day=30)
for file in os.listdir(dir):
    if file.endswith(".jpg"):
        # Get the date the image was taken
        str_date = "18" + file[:10]
        date = datetime.strptime(str_date, "%y%m%d%H%M%S")
        p = int(file[-9]) - 1
        dates[p].append(date)
        delta = date-then
        hours[p].append(int(delta.total_seconds()/3600))
        # Read image
        file_dir = dir + file
        img = cv.imread(file_dir, -1)
        # blur pre-processing to reduce noise
        blur = cv.bilateralFilter(img, 5, 75, 75)
        # convert to HSV color space
        hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(hsv)
        # apply low and high threshold (inRange) for green plant
        lower_green = np.array([30, 20, 23])
        upper_green = np.array([50, 255, 150])
        mask = cv.inRange(hsv, lower_green, upper_green)
        # Morphology, to adjust mask
        kernel = np.ones((7,7),np.uint8)
        opening = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
        kernel = np.ones((3, 3), np.uint8)
        morph = cv.morphologyEx(opening, cv.MORPH_ERODE, kernel)
        # Use mask to get average and variance hue of plant
        mean, std = cv.meanStdDev(h,mask=morph)
        var = (std[0][0])**2
        avg_hue[p].append(mean[0][0])
        var_hue[p].append(var)
        # file_name = odir + os.path.splitext(file)[0] + "_mask.jpg"
        # cv.imwrite(file_name, mask)

feat_type1 = ['Mean', 'Variance']
feat_type2 = ['mean', 'vari']
p_cond = ""
p_type = ""
for t in range(0,2):
    for p in range(0,6):
        # Set x and y axes
        x = array(hours[p])
        if t == 0:
            y = array(avg_hue[p])
        if t == 1:
            y = array(var_hue[p])
        z = np.polyfit(x, y, 1)
        # Plant condition
        if (p==0) | (p==1) | (p==2):
            p_cond = "Watered"
        elif (p==3) | (p==4) | (p==5):
            p_cond = "Drought-stressed"
        # Plant type / species
        if (p==0) | (p==4):
            p_type = "type 1"
        elif (p==2) | (p==5):
            p_type = "type 2"
        elif (p==2) | (p==5):
            p_type = "type 3"
        # Calculate the r correlation coefficient
        r_mat = np.corrcoef(x, y)
        r = r_mat[0][1]
        r_text = "r = %.4f" % r
        # Plot
        plt.plot(x, y, marker='o', linestyle='None')
        plt.plot(x, z[1]+z[0]*x, linestyle='dashed')
        plt.title("VL Hue " + feat_type1[t] + ", Plant " + p_type + ", " + p_cond + "\n" + r_text)
        plt.xlabel("Time (Hours)")
        plt.ylabel("Hue " + feat_type1[t])
        plt.savefig("VL_hue_" + feat_type2[t] + "_plant" + p_type + "_" + p_cond + ".png")
        # # Print equation onto plot
        # eq = "y=%.4fx+%.4f" %(z[0], z[1])
        # poly_z = np.poly1d(z)
        # x_text = np.amin(x) - (np.amax(x) - np.amin(x))*0.01
        # y_text = poly_z(25) + - (np.amax(y) - np.amin(y))*0.10
        # plt.annotate(eq, xy = (35,poly_z(35)), xytext=(x_text,y_text),  arrowprops=dict(facecolor='black', shrink=0.025), bbox={'facecolor':'white'})
        print("Plant " + str(p + 1) + " " + feat_type1[t] + " Correlation: " + str(r)) + p_cond
        plt.close()