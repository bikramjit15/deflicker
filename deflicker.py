from PIL import Image
import glob
import cv2
import imutils
import sys
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import os
import cv2
import pandas as pd
from numpy.polynomial.hermite import hermfit, hermval
import time
import progressbar


######################################################Start DEFLICKER###########################################

def brightness(img):
    cols, rows, temp = img.shape
    brightness_value = np.sum(img) / (255 * cols * rows)
    return brightness_value

def adjust_brightness(img, actual, adjusted, beta):
    ratio = adjusted / actual
    return cv2.convertScaleAbs(img, alpha = ratio, beta = beta)
    




ext = input('Input the original file extension: ')
if '.' not in ext.strip():
    ext = '.'+ext.strip()
files = glob.glob('raw/*'+ext)
n_images= len(glob.glob('raw/*'+ext))
print('Sucessfully read %d images'%n_images)
i=0
brightness_array = np.zeros(n_images)
print('Calculating Image Properties')
################crop-dimension#####################
rotate = imp.load_source('rotate', 'rotat.py')
im2 = cv2.imread(files[1]).copy()
print('Use keys r and e to rotate and left-click + drag to crop')
print('Right Click to reset rotate and crop')
print('click c to proceed')
(y,y1,x,x1,angle_r) = rotate.ro(im2)
#print(y,y1,x,x1,angle_r)
print('crop and rotation details fetched!')
################crop-dimension#####################
toolbar_width = n_images

# Converts the images:
i=0
print('Calculating average image properties')
# setup toolbar
with progressbar.ProgressBar(max_value=toolbar_width) as bar:
    for f in files:
        time.sleep(0.1)
        bar.update(i)
        if (i%1 == 0):
            #n_images+=1
            im2 = cv2.imread(f)
            im2 = imutils.rotate(im2, angle=angle_r)
            im = im2[y:y1, x:x1].copy()
            brightness_array[i] = (brightness(im))
            i+=1
        




mean_brightness = np.mean(brightness_array)
print('Computed %lf as mean brigthness'%mean_brightness)
stdev_brightness = np.std(brightness_array)
print('Computed %lf as standard deviation of brightness'%stdev_brightness)
min_brightness = np.min(brightness_array)
print('Computed %lf as min brigthness'%min_brightness)


i=0
print('Cropping, Rotating and deflickering')
# setup toolbar

new_bright_value = mean_brightness
with progressbar.ProgressBar(max_value=toolbar_width) as bar:
    for f in files:
        time.sleep(0.1)
        bar.update(i)
        i+=1
        if (i%1 == 0):
            #n_images+=1
            im2 = cv2.imread(f)
            im2 = imutils.rotate(im2, angle=angle_r)
            im = im2[y:y1, x:x1].copy()
            bright_value = brightness(im)
            #print('Processing image no. %d ' %i )
            beta = 0
            im2 = adjust_brightness(im, bright_value, new_bright_value, beta)
            cv2.imwrite(f"img/img{i:04d}.bmp", im2)