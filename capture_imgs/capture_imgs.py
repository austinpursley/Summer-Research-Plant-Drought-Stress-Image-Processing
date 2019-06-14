# capture_imgs.py
# Austin Pursley
# 6/6/2018
# This script was used for imaging plants for a summer research project.

# This script runs on a Raspberry Pi and is used to quickly capture images from
# both a visible light (VL) camera and an infared (IR) camera. In the physical
# setup, the cameras are right next to each other and I was taking pictures of
# some plants, one by one, to gather data for a computer vision research
# project. I using MobaXterm to establish an SSH into the Pi to run this program.
# The thermal camera used is a FLIR Lepton, v.1.5, 50 degree, shutterless version

import os
import time
import datetime
import os
from time import sleep
from picamera import PiCamera
from subprocess import call

import cv2 as cv
import numpy as np

#Verify the time is updated / correct
print "Time is ", datetime.datetime.now()
# Show both images
camera = PiCamera()
camera.resolution = (1024, 768)
# Flip because camera is upside down (won't have to flip images later)
camera.vflip = True
camera.hflip = True
# Preview if you have a monitor
camera.start_preview()
# Camera warm-up time
sleep(2)
program_run = True
while(program_run):
  print "Capturing images..."
  # Capture the visible light image
  timestamp = datetime.datetime.now().strftime("%m%d%H%M%S")
  i = -1
  for f in os.listdir('.'):
    if os.path.splitext(f)[1] == ".pgm":
      pic_num = (os.path.splitext(f)[0])[-4:]
      if int(pic_num) > i:
        i = int(pic_num)

  vl_img_name = timestamp + "_VL_IMG_" + str(i+1).zfill(4) + ".jpg"
  camera.capture(vl_img_name)
  # Capture the thermal image (check C code for details)
  call(["sudo", "./raspi_capture_ir_raw/raspi_capture_ir_raw"])
  ir_img_name = "IR_IMG_0000.pgm"
  new_ir_img_name  = timestamp + "_IR_IMG_%04d.pgm" % (i+1)
  os.rename(ir_img_name, new_ir_img_name)
  ir_img_name = new_ir_img_name
  ir_img = cv.imread(ir_img_name, -1)
  vl_img = cv.imread(vl_img_name, -1)
  # For visualization, create normalized, larger thermal image
  norm_ir = np.zeros((60, 80))
  norm_ir = cv.normalize(ir_img, norm_ir, 255, 0, cv.NORM_MINMAX, dtype=cv.CV_8U)
  norm_ir_resize = cv.resize(norm_ir, (0,0), fx=10, fy=10, interpolation = cv.INTER_NEAREST)
  vis_ir_dir = "visualize_ir/" + os.path.splitext(ir_img_name)[0] + ".jpg"
  cv.imwrite(vis_ir_dir, norm_ir_resize)
  # This window is called to make sure two images windows are activated.
  cv.namedWindow("GetFocus", cv.WINDOW_NORMAL)
  img = np.zeros((60, 80))
  cv.imshow("GetFocus", img)
  cv.setWindowProperty("GetFocus", cv.WND_PROP_FULLSCREEN, 1)
  cv.waitKey(1)
  cv.setWindowProperty("GetFocus", cv.WND_PROP_FULLSCREEN, cv.WINDOW_NORMAL)
  cv.destroyWindow("GetFocus")
  # Two windows for images
  cv.namedWindow('vl_win',cv.WINDOW_NORMAL)
  cv.resizeWindow('vl_win', 400, 400)
  cv.moveWindow('vl_win', 50, 100)
  cv.imshow('vl_win', vl_img)
  cv.namedWindow('ir_win',cv.WINDOW_NORMAL)
  cv.resizeWindow('ir_win', 400, 400)
  cv.moveWindow('ir_win', 450, 100)
  cv.imshow('ir_win', norm_ir)
  # Removing windows. Calling waitKey in succession removes an issue where
  # windows would not close
  cv.waitKey(0)
  cv.destroyAllWindows()
  cv.waitKey(1)
  cv.waitKey(1)
  cv.waitKey(1)
  cv.waitKey(1)
  cv.waitKey(1)
  # Capture will take another set of images
  # Discard will delete previous images and take another set
  # Quit will exit the program
  print "Capture: c Discard: d Quit: q"
  print "ENTER: "
  while True:
      k = raw_input()
      if (k == 'y') | (k == 'c'):
        print "Capturing more images..."
        break
      elif((k == 'n') | (k == 'd')):
          print "Deleting images, capturing more..."
          os.remove(vl_img_name)
          os.remove(ir_img_name)
          os.remove(vis_ir_dir)
          break
      elif k == 'q':
            program_run = False
            break
camera.close()
print "ending program..."