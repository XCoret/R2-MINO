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
pWindow= pygame.display.set_mode((1600,800))
pygame.display.set_caption("R2-MINO")

baseX= 800
baseY= 400
baseRadius = 37 ## mm

lenghtA = 280 ## mm
widthA = 25 ## mm
AposX = baseX+lenghtA
AposY = 400
degreeA = 0

lenghtB = 280 ## mm
widthB = 25 ## mm
BposX = AposX+lenghtB
BposY = 400
degreeB = 0


def getNewPosition(lenght, degree, centerX, centerY):
    newX = lenght* math.cos(math.radians(degree)) + centerX
    newY = lenght* math.sin(math.radians(degree)) + centerY
  
    return newX, newY




while True:
    pWindow.fill(white)
    pygame.draw.circle(pWindow, red, (baseX,baseY), baseRadius)
    
    (AposX,AposY) = getNewPosition(lenghtA, degreeA, baseX, baseY)
    pygame.draw.line(pWindow, blue, (baseX,baseY), (round(AposX),round(AposY)), widthA)

    (BposX,BposY) = getNewPosition(lenghtB, degreeB, AposX, AposY)
    pygame.draw.line(pWindow, green, (round(AposX),round(AposY)), (round(BposX),round(BposY)), widthA)
    
    for pEvent in pygame.event.get():
        if pEvent.type == QUIT:
            pygame.quit()
            sys.exit()

    if degreeA == 360:
        degreeA = 0
        
    degreeA +=1
    pygame.display.update()









