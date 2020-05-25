import numpy as np
import math
import cv2 as cv
from matplotlib import pyplot as plt
import os
import visio as a
import time
if __name__ == '__main__':
    v = a.ModulVisio(False)
    files = os.listdir('frames')
    time.sleep(5)
    for f in files:
        print(f)
        frame = cv.imread('frames/{}'.format(f))
        v.updateFrame(frame, False
        cv.imshow('Input', frame)
        try:
            cv.imshow('BG Substaction',v.fitxaFrame)
        except:
            pass
        cv.imshow('Output',v.get_output_frame())        
        cv.waitKey(2000)  
    cv.destroyAllWindows()
