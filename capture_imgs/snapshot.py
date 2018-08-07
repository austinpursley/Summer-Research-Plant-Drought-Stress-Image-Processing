# capture_imgs.py
# Austin Pursley
# 6/6/2018
# This script was used for imaging plants for a summer research project.
# Takes a single image and ends

import os
import time
import datetime
from time import sleep
from picamera import PiCamera
from subprocess import call

import cv2 as cv
import numpy as np

time = datetime.datetime.now().strftime("%m%d%H%M%S")

print "Time: " , time

# Capture the visible light image
camera = PiCamera()
camera.resolution = (1024, 768)
# Flip because camera is upside down (won't have to flip images later)
camera.vflip = True
camera.hflip = True
# Preview if you have a monitor
camera.start_preview()
# Camera warm-up time
sleep(2)
i = 0
while os.path.exists("IR_IMG_%04d.pgm" % i):
	i += 1
vl_img_name = "VL_IMG_" + str(i).zfill(4) + "_" + time + ".jpg"
camera.capture(vl_img_name)
camera.close()

# Capture the thermal image (check C code for details)
call(["sudo", "./raspi_capture_ir_raw/raspi_capture_ir_raw"])

# For visualization, create normalized thermal image
ir_img_name = "IR_IMG_%04d.pgm" % i
ir_img = cv.imread(ir_img_name, -1)
vl_img = cv.imread(vl_img_name, -1)
normalized_ir = np.zeros((60, 80))
normalized_ir = cv.normalize(ir_img, normalized_ir, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)
# Show both images

cv.namedWindow('vl_image',cv.WINDOW_NORMAL)
cv.resizeWindow('vl_image', 600, 600)
cv.imshow('vl_image', vl_img)

cv.namedWindow('ir_image',cv.WINDOW_NORMAL)
cv.resizeWindow('ir_image', 600, 600)
cv.moveWindow('ir_image', 900, 300)
cv.imshow('ir_image', normalized_ir)
cv.waitKey(0)

resize = cv.resize(normalized_ir, (0,0), fx=10, fy=10, interpolation = cv.INTER_NEAREST)
ir_img_name2 = "visualize_ir/IR_IMG_%04d.jpg" % i
cv.imwrite(ir_img_name2, resize)