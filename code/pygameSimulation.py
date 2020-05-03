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
heightRow = round(heightW/2)

## TABLE ##
tableSide = 400 ## mm
laterals = 50 ##mm

## BASE
baseX= 1100
baseY= 600
baseRadius = 50 ## mm

## Arm A
lenghtA = 275 ## mm
widthA = 25 ## mm
AposX = baseX + lenghtA
AposY = 400
degreeA = 0
maxDegreeA = 360

## Arm B
lenghtB = 275 ## mm
widthB = 25 ## mm
BposX = AposX + lenghtB
BposY = 400
degreeB = 0
maxDegreeB = 360 ## 

## Arm C
lengthC = 200 ##mm
maxHeight = 60
minHeight =140
actualHeight = maxHeight
isDown = False

## Tool
minOpening = 20
maxOpening = 40
actualOpening = maxOpening


## INIT ##

pygame.init()
mov = C()
pWindow= pygame.display.set_mode((widthW,heightW), pygame.RESIZABLE)
pygame.display.set_caption("R2-MINO")
degreeA, degreeB = mov.idlePosition()
next_degreeA = degreeA
next_degreeB = degreeB
armAReady = False
armBReady = False

hasStartedCatch = False
hasStartedDrop = False

count_test1 = 0
count_test2 = 0
count_test3 = 0
setIdle = False


## PRINT FUNCTIONS ##

def drawTable(): 
    pygame.draw.rect(pWindow,greenTable,(baseX-round(tableSide/2),baseY-(tableSide + baseRadius), tableSide, tableSide))
    pygame.draw.rect(pWindow,orange,(baseX-round(tableSide/2)-laterals,baseY-(tableSide +baseRadius), laterals,tableSide))
    pygame.draw.rect(pWindow,orange,(baseX+round(tableSide/2),baseY-(tableSide +baseRadius), laterals,tableSide))

def printGrid():
    pWindow.fill(white)
    pygame.draw.line(pWindow, black, (widthColumn,0), (widthColumn, heightW))
    pygame.draw.line(pWindow, black, (0,heightRow), (widthColumn, heightRow))

def printFirstCell():
    pygame.draw.line(pWindow, green, (0,heightRow/2), (375,heightRow/2), widthB)

def printSecondCell():
    pygame.draw.line(pWindow, green, (0,heightRow+(heightRow/2)), (375,heightRow+(heightRow/2)), widthB)

def printLiftTool(actualHeight):
    pygame.draw.line(pWindow, orange, (350,actualHeight+20), (350,actualHeight+lengthC), widthB)

def printTool(actualHeight, actualOpening):
    pygame.draw.line(pWindow, red, (350,actualHeight+lengthC), (350+actualOpening,actualHeight+lengthC+50), 15)
    pygame.draw.line(pWindow, blue, (350,actualHeight+lengthC), (350-actualOpening,actualHeight+lengthC+50), 15)

def printToolCell2(degree):
    centerX = 350
    centerY = heightRow+(heightRow/2)
    lenghtTool = 50
    blueX = lenghtTool * math.cos(math.radians(degree+90)) + 350
    blueY = lenghtTool * math.sin(math.radians(degree+90)) + lengthC + heightRow
    redX = lenghtTool * math.cos(math.radians(degree-90)) + 350
    redY =  lenghtTool * math.sin(math.radians(degree-90)) + lengthC + heightRow
    pygame.draw.line(pWindow, blue, (blueX,blueY), (centerX,centerY), 15)
    pygame.draw.line(pWindow, red, (redX,redY), (centerX,centerY), 15)

## CALCULATE FUNCTIONS ##

def resetDegrees():
    return mov.idlePosition()

def calculateFirstArm():
    x = lenghtA * math.cos(math.radians(degreeA)) + baseX
    y = lenghtA * math.sin(math.radians(degreeA+180)) + baseY
    return x,y

def calculateSecondArm():
    x = lenghtB * math.cos(math.radians(degreeA + degreeB + 180))  + AposX
    y = lenghtB * math.sin(math.radians(degreeA + degreeB + 360)) + AposY
    return x,y

def calculateDegreeTool(x, y):
    degTool = math.degrees(math.atan2(y, x))
    print(degTool)
    return degTool

## MOVEMENT FUNCTIONS ##

def goTo(goX, goY, isIdle):
    global next_degreeA
    global next_degreeB
    if isIdle:
        next_degreeA, next_degreeB = resetDegrees()
    else:
        next_degreeA, next_degreeB = mov.calculate_movement(goX, goY)


def upTool():
    global actualHeight
    global isDown
    if(actualHeight > maxHeight and isDown):
        actualHeight -=0.05
        return True
    else:
        isDown = False
        return False

def downTool():
    global actualHeight
    global isDown
    if(actualHeight < minHeight and not isDown):
        actualHeight +=0.05
        return True
    else:
        isDown = True
        return False
    
def openTool(): 
    global actualOpening
    if(actualOpening < maxOpening):
        actualOpening +=0.05
        return True
    else:
        return False

def closeTool(): 
    global actualOpening
    if(actualOpening > minOpening):
        actualOpening -=0.05
        return True
    else:
        return False

def rotateTool():
    return False
    
def catch():
    global hasStartedCatch
    
    if downTool():
        return True
    elif closeTool():
        return True
    elif upTool():
        return True
    else:
        hasStartedCatch = False
        return False
    
def drop():
    global hasStartedDrop
    if downTool():
        return True
    elif openTool():
        return True
    elif upTool():
        return True
    else:
        hasStartedDrop = False
        return False

## TESTS ##
def test1():
    positions = [[0, 5], [25, 5], [25, 25], [25, 45], [0, 45], [-20, 45], [-20, 25], [-20, 5]]
    (x, y) = mov.calculate_movement(positions[count_test1][0], positions[count_test1][1])
    #calculateDegreeTool(positions[count_test1][0], positions[count_test1][1])
    return x, y

def test2(setIdle):
    positions = [[10, 15], [10, 35], [-10, 35], [-10, 15], [0, 25]]
    if setIdle == True:
        (x, y) = resetDegrees()
    else:
        (x, y) = mov.calculate_movement(positions[count_test2][0], positions[count_test2][1])
    
    return x, y

def test3 ():
    global hasStartedCatch
    global hasStartedDrop
    if(count_test3 == 0):
        goTo(-22,44, False)
        hasStartedCatch = True
    elif(count_test3 == 1):
        goTo(10,35, False)
        hasStartedDrop = True
    elif(count_test3 == 2):
        goTo(10,35, True)


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
    printLiftTool(actualHeight)
    printTool(actualHeight, actualOpening)
    
    printSecondCell()
    printToolCell2(0)
    
    for pEvent in pygame.event.get():
        if pEvent.type == QUIT:
            pygame.quit()
            sys.exit()
        ## KEY controls
        elif pEvent.type == pygame.KEYDOWN:

            # Test 2: movement + idle
            if pEvent.key == K_LEFT:
                next_degreeA, next_degreeB = test2(setIdle)
                hasStartedCatch = False
                hasStartedDrop = False
                if setIdle:
                    setIdle = False
                else:
                    count_test2 +=1
                    setIdle = True 
                if count_test2>4:
                    count_test2 = 0
                    
            # Test 1: movement
            elif pEvent.key == K_RIGHT:
                next_degreeA, next_degreeB = test1()
                count_test1 +=1
                if count_test1>7:
                    count_test1 = 0

            # Test 3: catch + drop        
            if pEvent.key == K_UP:
                test3()
                count_test3 +=1
                if count_test3>2:
                    count_test3 = 0
            
            elif pEvent.key == K_DOWN:
                if degreeB>0:
                    degreeB-=1
        ## END KEY controls


    ## Gradual increment of degreeA
    if round(degreeA,2) != next_degreeA:
        armAReady = False
        if(degreeA < next_degreeA):
            degreeA +=0.01
        else:
            degreeA -=0.01
    else:
        armAReady = True

     ## Gradual increment of degreeB
    if round(degreeB,2) != next_degreeB:
        armBReady = False
        if(degreeB < next_degreeB):
            degreeB +=0.01
        else:
            degreeB -=0.01
    else:
        armBReady = True

    ## Flow control
    if armAReady and armBReady and hasStartedCatch:
        catch()
    if armAReady and armBReady and hasStartedDrop:
        drop()

    ## Window update
    pygame.display.update()

    
