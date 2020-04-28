import pygame,sys
import math
from pygame.locals import *
from random import randint

## COLORS ##
white =(255,255,255)
black=(0,0,0)
red = (255,0,0)
green = (0,255,0)
greenTable=(17,119,17)
blue = (0,0,255)
orange = (255,153,0)

## WINDOW ##
heightW = 800
widthW = 1600
widthColumn = 600
heightRow = heightW/2

## TABLE ##
tableSide = 400 ## mm
laterals = 50 ##mm
areaList = []

## BASE
baseX= 1100
baseY= 600
baseHeight = 100 ##mm TODO ajustar
baseRadius = 50 ## mm

## Arm A
lenghtA = 250 ## mm
widthA = 25 ## mm
AposX = baseX+lenghtA
AposY = 400
degreeA = 0
maxDegreeA = 180

## Arm B
lenghtB = 250 ## mm
widthB = 25 ## mm
BposX = AposX+lenghtB
BposY = 400
degreeB = 90
maxDegreeB = 360 ## TODO ajustar

## Arm C
lengthC = 152 ##mm
maxDegreeC = 180
radiusC = 20 ##mm

autoRun = True



## FUNCTIONS ##

def drawTable():
    pygame.draw.rect(pWindow,greenTable,(baseX-round(tableSide/2),baseY-(tableSide + baseRadius), tableSide, tableSide))
    pygame.draw.rect(pWindow,orange,(baseX-round(tableSide/2)-laterals,baseY-(tableSide +baseRadius), laterals,tableSide))
    pygame.draw.rect(pWindow,orange,(baseX+round(tableSide/2),baseY-(tableSide +baseRadius), laterals,tableSide))

def calculateFirstArm():
    x = lenghtA * math.cos(math.radians(degreeA)) + baseX
    y = lenghtA * math.sin(math.radians(degreeA+180)) + baseY
    return x,y

def calculateSecondArm():
    x = lenghtB * math.cos(math.radians(degreeA - degreeB + 180))  + AposX
    y = lenghtB * math.sin(math.radians(degreeA - degreeB + 360)) + AposY
    return x,y

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

## MAIN ##

pygame.init()
pWindow= pygame.display.set_mode((widthW,heightW), pygame.RESIZABLE)
pygame.display.set_caption("R2-MINO")



while True:
    printGrid()
    drawTable()
    pygame.draw.circle(pWindow, red, (baseX,baseY), baseRadius)
    
    (AposX,AposY) = calculateFirstArm()
    pygame.draw.line(pWindow, blue, (baseX,baseY), (round(AposX),round(AposY)), widthA)

    (BposX,BposY) = calculateSecondArm()
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
                if degreeA<maxDegreeA:
                    degreeA+=1
            elif pEvent.key == K_RIGHT:
                if degreeA>0:
                   degreeA-=1
            if pEvent.key == K_UP:
                if degreeB<maxDegreeB:
                    degreeB+=1
            elif pEvent.key == K_DOWN:
                if degreeB>0:
                    degreeB-=1
        ## END KEY controls

    if(autoRun == True):
        degreeB+=1
        if degreeB > maxDegreeB:
            degreeB = 0
            degreeA += 1
            if degreeA > maxDegreeA:
                degreeA = 0
        
    pygame.display.update()
