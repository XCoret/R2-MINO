# -*- coding: utf-8 -*-
"""
@author: XCoret
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('domino.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blurred = cv2.pyrMeanShiftFiltering(img,21,51)

ret,threshold = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
contours,hierarchy = cv2.findContours(threshold,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

print(len(contours))

plt.imshow(gray,'gray')
plt.show()