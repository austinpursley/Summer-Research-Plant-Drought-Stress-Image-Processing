# -*- coding: utf-8 -*-
import cv2 as cv
import numpy as np
import os
import matplotlib as plt
from matplotlib import pyplot as plt

# Original, unormalized image

fig = plt.figure(figsize=(12,4))
i = 1
row = 2
column = 4
dir = 'set1'
for f in os.listdir(dir):
    if os.path.splitext(f)[1] == ".pgm":
        f_dir = dir + '/' + f
        img = cv.imread(f_dir, -1)
        img = np.float32(img)
        fig.add_subplot(row, column, i)
        Fdegree_img = -0.00000608*np.float_power(img,2) + 0.1715806300*img - 920.665168
        print "max: ", Fdegree_img.max()
        print "min: ", Fdegree_img.min()
        date = f[:10]
        date = date[:2] + '.' + date[2:4] + '.' + date[4:8]
        plt.title(date)
        im = plt.imshow(Fdegree_img, vmin=68, vmax=85.1)
        im.set_cmap('ocean')
        cv.namedWindow('image',cv.WINDOW_NORMAL)
        cv.resizeWindow('image', 600, 600)
        i = i + 1

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.825, 0.55, 0.022, 0.30])
cbar = plt.colorbar(im, cax=cbar_ax)
cbar.set_label("F$^\circ$")

for f in os.listdir(dir):
    if os.path.splitext(f)[1] == ".jpg":
        f_dir = dir + '/' + f
        img = cv.imread(f_dir, -1)
        fig.add_subplot(row, column, i)
        #date = f[:10]
        #date = date[:2] + '.' + date[2:4] + '.' + date[4:8]
        #plt.title(date)
        im = plt.imshow(img)
        im.set_cmap('ocean')
        i = i + 1

plt.show()