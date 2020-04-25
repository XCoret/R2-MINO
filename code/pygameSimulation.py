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
orange = (255,153,0)

## WINDOW ##
heightW = 800
widthW = 1600
widthColumn = 600
heightRow = heightW/2

## BASE
baseX= 900
baseY= 400
baseRadius = 37 ## mm

## Arm A
lenghtA = 280/2 ## mm
widthA = 25 ## mm
AposX = baseX+lenghtA
AposY = 400
degreeA = 0

## Arm B
lenghtB = 360/2 ## mm
widthB = 25 ## mm
BposX = AposX+lenghtB
BposY = 400
degreeB = 0

## Arm C
lengthC = 152 ##mm

pygame.init()
pWindow= pygame.display.set_mode((widthW,heightW), pygame.RESIZABLE)
pygame.display.set_caption("R2-MINO")


def getNewPosition(lenght, degree, centerX, centerY):
    newX = lenght* math.cos(math.radians(degree)) + centerX
    newY = lenght* math.sin(math.radians(degree)) + centerY
  
    return newX, newY


def printGrid():
    pWindow.fill(white)
    pygame.draw.line(pWindow, black, (widthColumn,0), (widthColumn, heightW))
    pygame.draw.line(pWindow, black, (0,heightRow), (widthColumn, heightRow))


def printFirstCell():
    pygame.draw.line(pWindow, blue, (0, 100),(400-(lenghtB*2),100), widthB)
    pygame.draw.line(pWindow, green, (400-(lenghtB*2),100), (400,100), widthB)

def printSecondCell():
    pygame.draw.line(pWindow, blue, (0, heightRow+(heightRow/2)),(400-(lenghtB*2),heightRow+(heightRow/2)), widthB)
    pygame.draw.line(pWindow, green, (400-(lenghtB*2),heightRow+(heightRow/2)), (400,heightRow+(heightRow/2)), widthB)


while True:
    printGrid()
    pygame.draw.circle(pWindow, red, (baseX,baseY), baseRadius)
    
    (AposX,AposY) = getNewPosition(lenghtA, degreeA, baseX, baseY)
    pygame.draw.line(pWindow, blue, (baseX,baseY), (round(AposX),round(AposY)), widthA)

    (BposX,BposY) = getNewPosition(lenghtB, degreeB, AposX, AposY)
    pygame.draw.line(pWindow, green, (round(AposX),round(AposY)), (round(BposX),round(BposY)), widthB)

    printFirstCell()
    pygame.draw.line(pWindow, orange, (350,50), (350,50+lengthC), widthB)

    printSecondCell()

    
    for pEvent in pygame.event.get():
        if pEvent.type == QUIT:
            pygame.quit()
            sys.exit()
        ## KEY controls
        elif pEvent.type == pygame.KEYDOWN:
            if pEvent.key == K_LEFT:
                degreeA+=1
            elif pEvent.key == K_RIGHT:
                degreeA-=1
            if pEvent.key == K_UP:
                degreeB+=1
            elif pEvent.key == K_DOWN:
                degreeB-=1
        ## END KEY controls
    
    pygame.display.update()









