import pygame,sys
import math
from pygame.locals import *
from random import randint

## COLORS ##
white =(255,255,255)
black=(0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
##END COLORS ##

pygame.init()
pWindow= pygame.display.set_mode((800,800))
pygame.display.set_caption("R2-MINO")

baseX= 400
baseY= 400

lenghtA = 280 ## mm
widthA = 50 ## mm
baseRadius = 37 ## mm

AposX = baseX-lenghtA
AposY = 400

degreeA = 0
vel = 1

##BposX=0
##BposY=0


def getNewPosition(lenght, degree, centerX, centerY):
    newX = lenght* math.cos(math.radians(degree)) + centerX
    newY = lenght* math.sin(math.radians(degree)) + centerY
  
    return newX, newY




while True:
    pWindow.fill(white)
    pygame.draw.circle(pWindow, red, (baseX,baseY), baseRadius)
    
    (AposX,AposY) = getNewPosition(lenghtA, degreeA, baseX, baseY)
    pygame.draw.line(pWindow, blue, (baseX,baseY), (round(AposX),round(AposY)), widthA)
    
    for pEvent in pygame.event.get():
        if pEvent.type == QUIT:
            pygame.quit()
            sys.exit()

    if degreeA == 360:
        degreeA = 0
        
    degreeA +=1
    pygame.display.update()









