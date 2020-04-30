import pygame,sys
import math
import time
from pygame.locals import *
from random import randint
from moviment import C

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
maxDegreeA = 360

## Arm B
lenghtB = 250 ## mm
widthB = 25 ## mm
BposX = AposX+lenghtB
BposY = 400
degreeB = 0
maxDegreeB = 360 ## 

## Arm C
lengthC = 200 ##mm
maxDegreeC = 180
radiusC = 20 ##mm

autoRun = True

count_test = 0
setIdle = False

## INIT ##

pygame.init()
mov = C()
pWindow= pygame.display.set_mode((widthW,heightW), pygame.RESIZABLE)
pygame.display.set_caption("R2-MINO")
degreeA, degreeB = mov.idlePosition()
next_degreeA = degreeA
next_degreeB = degreeB



## FUNCTIONS ##

def resetDegrees():
    return mov.idlePosition()

def test1(count_test):
    positions = [[0, 5], [25, 5], [25, 25], [25, 45], [0, 45], [-20, 45], [-20, 25], [-20, 5]]
    (x, y) = mov.calculate_movement(positions[count_test][0], positions[count_test][1])
    return x, y

def test2(count_test, setIdle):
    positions = [[10, 15], [10, 35], [-10, 35], [-10, 15], [0, 25]]

    if setIdle == True:
        (x, y) = resetDegrees()
    else:
        (x, y) = mov.calculate_movement(positions[count_test][0], positions[count_test][1])
    
    return x, y
    

def drawTable():
    pygame.draw.rect(pWindow,greenTable,(baseX-round(tableSide/2),baseY-(tableSide + baseRadius), tableSide, tableSide))
    pygame.draw.rect(pWindow,orange,(baseX-round(tableSide/2)-laterals,baseY-(tableSide +baseRadius), laterals,tableSide))
    pygame.draw.rect(pWindow,orange,(baseX+round(tableSide/2),baseY-(tableSide +baseRadius), laterals,tableSide))

def calculateFirstArm():
    x = lenghtA * math.cos(math.radians(degreeA)) + baseX
    y = lenghtA * math.sin(math.radians(degreeA+180)) + baseY
    return x,y

def calculateSecondArm():
    x = lenghtB * math.cos(math.radians(degreeA + degreeB + 180))  + AposX
    y = lenghtB * math.sin(math.radians(degreeA + degreeB + 360)) + AposY
    return x,y

def printGrid():
    pWindow.fill(white)
    pygame.draw.line(pWindow, black, (widthColumn,0), (widthColumn, heightW))
    pygame.draw.line(pWindow, black, (0,heightRow), (widthColumn, heightRow))

def printFirstCell():
    pygame.draw.line(pWindow, green, (400-(lenghtB*2),heightRow/2), (400,heightRow/2), widthB)

def printSecondCell():
    pygame.draw.line(pWindow, green, (400-(lenghtB*2),heightRow+(heightRow/2)), (400,heightRow+(heightRow/2)), widthB)

def printClosedTool():
    pygame.draw.line(pWindow, blue, (350,140+lengthC), (350+20,140+lengthC+50), 15)
    pygame.draw.line(pWindow, blue, (350,140+lengthC), (350-20,140+lengthC+50), 15)

def printOpenedTool():
    pygame.draw.line(pWindow, blue, (350,140+lengthC), (350+40,140+lengthC+50), 15)
    pygame.draw.line(pWindow, blue, (350,140+lengthC), (350-40,140+lengthC+50), 15)

def printLiftTool(isLift):
    if isLift:
        pygame.draw.line(pWindow, orange, (350,80), (350,60+lengthC), widthB)
    else:
        pygame.draw.line(pWindow, orange, (350,160), (350,140+lengthC), widthB)
    


## MAIN ##

while True:
    printGrid()
    drawTable()
    pygame.draw.circle(pWindow, red, (baseX,baseY), baseRadius)
    
    (AposX,AposY) = calculateFirstArm()
    pygame.draw.line(pWindow, blue, (baseX,baseY), (round(AposX),round(AposY)), widthA)

    (BposX,BposY) = calculateSecondArm()
    pygame.draw.line(pWindow, green, (round(AposX),round(AposY)), (round(BposX),round(BposY)), widthB)

    printFirstCell()

    printLiftTool(True)
    printClosedTool()  

    printSecondCell()
    
    for pEvent in pygame.event.get():
        if pEvent.type == QUIT:
            pygame.quit()
            sys.exit()
        ## KEY controls
        elif pEvent.type == pygame.KEYDOWN:
            if pEvent.key == K_LEFT:
                next_degreeA, next_degreeB = test2(count_test, setIdle)
                if setIdle:
                    setIdle = False
                else:
                    count_test +=1
                    setIdle = True
            elif pEvent.key == K_RIGHT:
                degreeA, degreeB = test1(count_test)
                count_test +=1
            if pEvent.key == K_UP:
                if degreeB<maxDegreeB:
                    degreeB+=1
            elif pEvent.key == K_DOWN:
                if degreeB>0:
                    degreeB-=1
        ## END KEY controls


    if degreeA != next_degreeA:
        if(degreeA < next_degreeA):
            degreeA +=0.01
        else:
            degreeA -=0.01
    if degreeB != next_degreeB:
        if(degreeB < next_degreeB):
            degreeB +=0.01
        else:
            degreeB -=0.01

    pygame.display.update()
    #time.sleep(0.1)

##    if(autoRun == True):
##        degreeB+=1
##        if degreeB > maxDegreeB:
##            degreeB = 0
##            degreeA += 1
##            if degreeA > maxDegreeA:
##                degreeA = 0
        
    
