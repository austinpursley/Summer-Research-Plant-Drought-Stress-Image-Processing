import os
import time
import datetime
import os
from time import sleep
from picamera import PiCamera
from subprocess import call

import cv2 as cv
import numpy as np

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

#get timestamp
timestamp = datetime.datetime.now().strftime("%m%d%H%M%S")
print "Time: " , timestamp
# Caputre VL images
i = 0
while os.path.exists("IR_IMG_%04d.pgm" % i):
    i += 1
vl_img_name = timestamp + "_VL_IMG_" + str(i).zfill(4) + ".jpg"
camera.capture(vl_img_name)
camera.close()
# Capture the thermal image (check C code for details)
call(["sudo", "./raspi_capture_ir_raw/raspi_capture_ir_raw"])
ir_img_name = "IR_IMG_%04d.pgm" % i
new_ir_img_name  = timestamp + "_IR_IMG_%04d.pgm" % i
os.rename(ir_img_name, new_ir_img_name)

# For visualization, create normalized thermal image
ir_img = cv.imread(ir_img_name, -1)
vl_img = cv.imread(vl_img_name, -1)
normalized_ir = np.zeros((60, 80))
normalized_ir = cv.normalize(ir_img, normalized_ir, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)
# Show both images

cv.namedWindow('ir_image',cv.WINDOW_NORMAL)
cv.resizeWindow('ir_image', 600, 600)
cv.namedWindow('vl_image',cv.WINDOW_NORMAL)
cv.resizeWindow('vl_image', 600, 600)
cv.imshow('vl_image', vl_img)
cv.imshow('ir_image', normalized_ir)
cv.waitKey(0)
cv.destroyAllWindows()

resize = cv.resize(normalized_ir, (0,0), fx=10, fy=10, interpolation = cv.INTER_NEAREST)
ir_img_name2 = "visualize_ir/IR_IMG_%04d.jpg" % i
cv.imwrite(ir_img_name2, resize)