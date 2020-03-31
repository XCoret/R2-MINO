# -*- coding: utf-8 -*-
'''
Computa els canvis registrats en el taulell de joc i ho passa al Mòdul Control.
'''
import cv2
import numpy as np
from matplotlib import pyplot as plt

print('Modul Visio')
def llegirImatge(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



    plt.imshow(gray,'gray')
    plt.show()

