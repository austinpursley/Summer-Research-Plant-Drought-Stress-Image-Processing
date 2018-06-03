import os
import time
import datetime
import os
from time import sleep
#from picamera import PiCamera
from subprocess import call

import cv2 as cv
import numpy as np

camera = PiCamera()
camera.resolution = (1024, 768)
# Flip because camera is upside down (won't have to flip images later)
camera.vflip = True
camera.hflip = True
# Preview if you have a monitor
camera.start_preview()
# Camera warm-up time
sleep(2)

this_condition = True
while this_condition:
    print "taking images..."
    # Capture the visible light image
    ################################################################
    timestamp = datetime.datetime.now().strftime("%m%d%H%M%S")
    i = 0
    while os.path.exists("IR_IMG_%04d.pgm" % i):
        i += 1
    vl_img_name = timestamp + "_VL_IMG_" + str(i).zfill(4) + ".jpg"
    camera.capture(vl_img_name)
    # Capture the thermal image (check C code for details)
    call(["sudo", "./raspi_capture_ir_raw/raspi_capture_ir_raw"])
    ir_img_name = "IR_IMG_%04d.pgm" % i
    new_ir_img_name  = timestamp + "_IR_IMG_%04d.pgm" % i
    os.rename(ir_img_name, new_ir_img_name)
    ##################################################################
    ir_img = cv.imread(ir_img_name, -1)
    vl_img = cv.imread(vl_img_name, -1)
    # For visualization, create normalized, resized thermal image
    norm_ir = np.zeros((60, 80))
    norm_ir = cv.normalize(ir_img, norm_ir, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)
    norm_ir_resize = cv.resize(norm_ir, (0,0), fx=10, fy=10, interpolation = cv.INTER_NEAREST)
    vis_ir_dir = "visualize_ir/" + ir_img_name
    cv.imwrite(vis_ir_dir, norm_ir_resize)
    # Show both images
    cv.namedWindow('ir_image',cv.WINDOW_NORMAL)
    cv.resizeWindow('ir_image', 600, 600)
    cv.namedWindow('vl_image',cv.WINDOW_NORMAL)
    cv.resizeWindow('vl_image', 600, 600)
    cv.imshow('vl_image', vl_img)
    cv.imshow('ir_image', norm_ir)
    ##################################################################
    print("use images?")
    input = cv.waitKey(0)
    #cv.destroyAllWindows()
    #input = raw_input("Use images? ")
    if (input == ord('y')):
        input = raw_input("Take another photo? ")
        if (input == "y"):
            print "taking images..."
        elif (input == "n"):
            print "ending program..."
            camera.close()
            this_condition = False
    elif(input == ord('y')):
        print "deleting images, taking more"
        os.remove(vl_img_name)
        os.remove(new_ir_img_name)