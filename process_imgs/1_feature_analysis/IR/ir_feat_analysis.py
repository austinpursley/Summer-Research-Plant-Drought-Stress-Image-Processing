# ir_feat_analysis.py
# Austin Pursley
# 8/3/2018
# Finding thermal intensity of plants and seeing how that feature changes over time.
# Looking at thermal intensity mean and variance

import cv2 as cv
import numpy as np
import os
from datetime import datetime
from matplotlib import pyplot as plt
from numpy import array

i = 0
dir = "C:/Users/Austin Pursley/Projects/Summer-Research-Plant-Drought-Stress-Computer-Vision/process_imgs/0_data/raw_plant_imgs/"
crop_dir = "C:/Users/Austin Pursley/Projects/Summer-Research-Plant-Drought-Stress-Computer-Vision/process_imgs/0_data/crop_plant_imgs/cropped/IR/"
odir = "output/"
avg = [[],[],[],[],[],[]]
var = [[],[],[],[],[],[]]
dif = [[],[],[],[],[],[]]
dates = [[],[],[],[],[],[]]
hours = [[],[],[],[],[],[]]
then = datetime(year=2018, month=5, day=30)

for file in os.listdir(dir):
    if file.endswith("top.pgm"):
        # Get the date the image was taken
        str_date = "18" + file[:10]
        date = datetime.strptime(str_date, "%y%m%d%H%M%S")
        p = int(file[-9]) - 1
        dates[p].append(date)
        delta = date - then
        hours[p].append(int(delta.total_seconds() / 3600))
        # Read images
        img_dir = dir + file
        mask_dir = crop_dir + os.path.splitext(file)[0] + "_1_mask.jpg"
        img = cv.imread(img_dir, -1)
        mask = cv.imread(mask_dir, 0)
        # Calibrate thermal image and find features
        Fdegree_img = -0.00000608 * np.float_power(img, 2) + 0.1715806300 * img - 920.665168
        not_mask = cv.bitwise_not(mask)
        mean, std = cv.meanStdDev(Fdegree_img, mask=mask)
        variance = (std[0][0]) ** 2
        back_mean = cv.mean(Fdegree_img, not_mask)
        mean_diff = back_mean - mean[0][0]
        avg[p].append(mean[0][0])
        var[p].append(variance)
        dif[p].append(mean_diff[0])
        # Output images for illustration of plant ROI
        normalizedImg = np.zeros((60, 80))
        normalizedImg = cv.normalize(img, normalizedImg, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)
        file_name = odir + os.path.splitext(file)[0] + ".jpg"
        cv.imwrite(file_name, normalizedImg)
        file_name = odir + os.path.splitext(file)[0] + "_mask.jpg"
        cv.imwrite(file_name, mask)

feat_type1 = ['Mean', 'Variance', 'Mean Difference']
feat_type2 = ['mean', 'vari', 'diffmean']
p_type = ""
p_cond = ""
for t in range(0,3):
    for p in range(0,6):
        # Set x and y axes
        x = array(hours[p])
        if t == 0:
            y = array(avg[p])
        if t == 1:
            y = array(var[p])
        if t == 2:
            y = array(dif[p])
        z = np.polyfit(x, y, 1)
        # Plant condition
        if (p == 0) | (p == 1) | (p == 2):
            p_cond = "Watered"
        elif (p == 3) | (p == 4) | (p == 5):
            p_cond = "Drought-stressed"
        # Plant type / species
        if (p == 0) | (p == 4):
            p_type = "type 1"
        elif (p == 2) | (p == 5):
            p_type = "type 2"
        elif (p == 2) | (p == 5):
            p_type = "type 3"
        # Calculate the r correlation coefficient
        r_mat = np.corrcoef(x, y)
        r = r_mat[0][1]
        r_text = "r = %.4f" % r
        # Plot
        plt.plot(x, y, marker='o', linestyle='None')
        plt.plot(x, z[1]+z[0]*x, linestyle='dashed')
        plt.title("IR Hue " + feat_type1[t] + ", Plant " + p_type + ", " + p_cond + "\n" + r_text)
        plt.xlabel("Time (Hours)")
        plt.ylabel("Thermal " + feat_type1[t])
        plt.savefig("VL_hue_" + feat_type2[t] + "_plant" + p_type + "_" + p_cond + ".png")
        print("Plant " + str(p + 1) + " " + feat_type1[t] + " Correlation: " + str(r)) + p_type
        plt.close()