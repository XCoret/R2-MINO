# -*- coding: utf-8 -*-
'''
Mòdul encarregat d’organitzar l’execució dels demés mòduls 
a partir de la informació que aquests li proporcionin. 
Les seves tasques seran:

-Formar un estat de partida a partir de la informació de la càmera rebuda del mòdul Visió. 
(Processament d’imatges a dades).

-Informar al mòdul jugabilitat de l’estat de la partida perquè aquest respongui amb una jugada.

-Proporcionar al mòdul Moviment les coordenades inicials i finals de la posició de la fitxa a moure.
'''
import domino as d
# import visio as v #COMENTAT PER TEST
#v = v() #COMENTAT PER TEST
from moviment import C
m = C()
import time

import pygame,sys
import math
import time
from pygame.locals import *
import random

from classeFitxa import Fitxa

## ----- PYGAME ----- ##

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
laterals = 100 ##mm

## BASE
baseX= 1100
baseY= 600
baseRadius = 50 ## mm

## Arm A
lenghtA = 275 ## mm
widthA = 25 ## mm
AposX = baseX + lenghtA
AposY = 400
degreeA = 180
maxDegreeA = 360

## Arm B
lenghtB = 275 ## mm
widthB = 25 ## mm
BposX = AposX + lenghtB
BposY = 400
degreeB = 90
maxDegreeB = 360 ## 

## Arm C
lengthC = 200 ##mm
maxHeight = 60
minHeight = 140
actualHeight = maxHeight
isDown = False

## Tool
minOpening = 20
maxOpening = 40
actualOpening = maxOpening
degreeTool = 180
nextDegreeTool = degreeTool
maxDegreeTool = 360
toolCompensation = 0


## INIT ##
pygame.init()
m = C()
pWindow= pygame.display.set_mode((widthW,heightW), pygame.RESIZABLE)
pygame.display.set_caption("R2-MINO")
#degreeA, degreeB = m.idlePosition()
next_degreeA = degreeA
next_degreeB = degreeB
next_toolCompensation = toolCompensation
armAReady = False
armBReady = False
compensationReady = False

hasStartedCatch = False
hasStartedDrop = False

count_test1 = 0
count_test2 = 0
count_test3 = 0
count_test4 = 0
setIdle = False

fitxes = pygame.sprite.Group()


## CALCULATE FUNCTIONS ##
def calculateFirstArm():
    x = lenghtA * math.cos(math.radians(degreeA)) + baseX
    y = lenghtA * math.sin(math.radians(degreeA+180)) + baseY
    return x,y

def calculateSecondArm():
    x = lenghtB * math.cos(math.radians(degreeA + degreeB + 180))  + AposX
    y = lenghtB * math.sin(math.radians(degreeA + degreeB + 360)) + AposY
    return x,y

def calculateSlide(degA, degB):
    x = math.cos(math.radians(degA))* math.sin(math.radians(degB)) + math.sin(math.radians(degA))* math.cos(math.radians(degB))
    y = math.sin(math.radians(degA))* math.sin(math.radians(degB)) - math.cos(math.radians(degA))* math.cos(math.radians(degB))
    deg = math.degrees(math.atan2(y, x))
    print(deg)

def calculateSecondArmAngle():
    x = round(BposX) - round(AposX)
    y = round(BposY) - round(AposY)
    degree =  math.degrees(math.atan2(y, x))
    return degree

def calculateToolAngleForPrint():
    return degreeTool + calculateSecondArmAngle()

def calculateIdleDegreeTool():
    x = round(BposX) - round(AposX)
    y = round(BposY) - round(AposY)
    degree = math.degrees(math.atan2(y, x))
    return degree + degreeTool

def coordinates2Pixels(cX, cY, scale):
    x = baseX + cX*10*scale # cm to mm
    y = baseY - cY*10*scale # cm to mm
    return x, y
    

## PRINT FUNCTIONS ##
PURPLE = (83, 33, 158)

def drawEllipse(x, y):
    pygame.draw.ellipse(pWindow, PURPLE, [x, y-100, tableSide, 200])
    

def drawTable():
    drawEllipse(baseX-round(tableSide/2), baseY-(tableSide + baseRadius))
    pygame.draw.rect(pWindow,greenTable,(baseX-round(tableSide/2),baseY-(tableSide + baseRadius), tableSide, tableSide))
    pygame.draw.rect(pWindow,orange,(baseX-round(tableSide/2)-laterals,baseY-(tableSide +baseRadius), laterals,tableSide))
    pygame.draw.rect(pWindow,orange,(baseX+round(tableSide/2),baseY-(tableSide +baseRadius), laterals,tableSide))


def printGrid():
    pWindow.fill(white)
    pygame.draw.line(pWindow, black, (widthColumn,0), (widthColumn, heightW))
    pygame.draw.line(pWindow, black, (0,heightRow), (widthColumn, heightRow))

def printFirstCell():
    pygame.draw.line(pWindow, green, (0,round(heightRow/2)), (375,round(heightRow/2)), widthB)

def printSecondCell():
    pygame.draw.line(pWindow, green, (widthColumn/2,heightW), (widthColumn/2,heightRow+round(heightRow/2)), widthB)

def printLiftTool(actualHeight):
    pygame.draw.line(pWindow, orange, (350,actualHeight+20), (350,actualHeight+lengthC), widthB)

def printTool(actualHeight, actualOpening):
    pygame.draw.line(pWindow, red, (350,actualHeight+lengthC), (350+actualOpening,actualHeight+lengthC+50), 15)
    pygame.draw.line(pWindow, blue, (350,actualHeight+lengthC), (350-actualOpening,actualHeight+lengthC+50), 15)

def printToolCell2(degree):
    centerX = widthColumn/2
    centerY = round(heightRow+(heightRow/2))
    lenghtTool = 50
    blueX = lenghtTool * math.cos(math.radians(degree+180)) + centerX
    blueY = lenghtTool * math.sin(math.radians(degree+180)) + lengthC + heightRow
    redX = lenghtTool * math.cos(math.radians(degree)) + centerX
    redY =  lenghtTool * math.sin(math.radians(degree)) + lengthC + heightRow
    pygame.draw.line(pWindow, blue, (round(blueX),round(blueY)), (centerX,centerY), 15)
    pygame.draw.line(pWindow, red, (round(redX),round(redY)), (centerX,centerY), 15)

def printRutine():
    global AposX, AposY, BposX, BposY, fitxes
    printGrid()
    drawTable()
    pygame.draw.circle(pWindow, red, (baseX,baseY), baseRadius)

    fitxes.update()
    fitxes.draw(pWindow)
    
    (AposX,AposY) = calculateFirstArm()
    pygame.draw.line(pWindow, blue, (baseX,baseY), (round(AposX),round(AposY)), widthA)

    (BposX,BposY) = calculateSecondArm()
    pygame.draw.line(pWindow, green, (round(AposX),round(AposY)), (round(BposX),round(BposY)), widthB)

    #printToolPrincipal(calculateIdleDegreeTool())

    printFirstCell()
    printLiftTool(actualHeight)
    printTool(actualHeight, actualOpening)
    
    printSecondCell()
    printToolCell2(degreeTool)
    calculateSecondArmAngle()
    
 
## MOVEMENT FUNCTIONS ##
def goTo(goX, goY, isDegree):
    global next_degreeA
    global next_degreeB
    global degreeA
    global degreeB

    armAReady = False
    armBReady = False

    if isDegree:
        next_degreeA, next_degreeB = goX, goY
    else: 
        next_degreeA, next_degreeB = m.calculate_movement(goX, goY)

    while (not armAReady or not armBReady):
        printRutine()

        ## Gradual increment of degreeA
        if round(degreeA,2) != next_degreeA:
            if(degreeA < next_degreeA):
                degreeA +=0.01

            else:
                degreeA -=0.01
        else:
            armAReady = True

        ## Gradual increment of degreeB
        if round(degreeB,2) != next_degreeB:
            if(degreeB < next_degreeB):
                degreeB +=0.01
            else:
                degreeB -=0.01
        else:
            armBReady = True
        
        pygame.display.update()

def openTool(): 
    global actualOpening
    
    while True:
        printRutine()
        if(actualOpening < m.operateToolOpen(True)):
            actualOpening +=0.05
        else:
            pygame.display.update()
            break
        pygame.display.update()
        
def closeTool(): 
    global actualOpening

    while True:
        printRutine()
        if(actualOpening > m.operateToolOpen(False)):
            actualOpening -=0.05
        else:
            pygame.display.update()
            break
        pygame.display.update()

def upTool():
    global actualHeight

    while True:
        printRutine()
        if(actualHeight > m.operateToolLift(True)):
            actualHeight -=0.05
        else:
            pygame.display.update()
            break
        pygame.display.update()

def downTool():
    global actualHeight

    while True:
        printRutine()
        if(actualHeight < m.operateToolLift(False)):
            actualHeight +=0.05
        else:
            pygame.display.update()
            break
        pygame.display.update()

def rotateTool(orientation):
    global degreeTool
    next_degreeTool = m.operateToolRotate(orientation)
    
    while True:
        printRutine()
        if round(degreeTool,2) != round(next_degreeTool,2):
            if(degreeTool < next_degreeTool):
                degreeTool +=0.05
            else:
                degreeTool -=0.05
        else:
            pygame.display.update()
            break   
        pygame.display.update()
        
def goIdle():
    x, y = m.idlePosition()
    goTo(x, y, True)

def goSignalPlayer(player):
    x, y = m.signalPlayer(player)
    goTo(x, y, True)
    closeTool()
    openTool()
    closeTool()
    openTool()    
    
def goCatch(pX, pY, orientation):
    goTo(pX, pY, False)
    rotateTool(orientation)
    downTool()
    closeTool()
    upTool()

def goDrop(pX, pY, orientation):
    goTo(pX, pY, False)
    rotateTool(orientation)
    downTool()
    openTool()
    upTool()

def goDance():
    goTo(0, 20, False)
    goTo(5, 25, False)
    goTo(0, 30, False)
    closeTool()
    openTool()
    goTo(-5, 25, False)
    goTo(0, 20, False)
    closeTool()
    openTool()
    closeTool()
    openTool()
    goTo(-5, 25, False)
    goTo(0, 30, False)
    closeTool()
    openTool()
    goTo(5, 25, False)
    goTo(0, 20, False)
    closeTool()
    openTool()
    closeTool()
    openTool()

def goSignalPass():
    goIdle()
    rotateTool('N')
    rotateTool('S')
    rotateTool('N')
    rotateTool('S')

## SIMULATION FUNCTIONS ##

def simCreateGame():
    print("SIMP!")
    global fitxes
    
    #Instantiate 28 Tokens
    for x in range(1, 29): 
        fitxes.add(Fitxa(str(x),0,0,(20,40)))

    fitxesAux = pygame.sprite.Group()
    fitxesAux = fitxes

    llistaIndex = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
    indexR = []
    indexH = []
    indexP = []

    for i in range(7):
        newIndex = random.choice(llistaIndex)
        indexR.append(newIndex)
        llistaIndex.remove(newIndex)
        
    for i in range(7):
        newIndex = random.choice(llistaIndex)
        indexH.append(newIndex)
        llistaIndex.remove(newIndex)

    for i in range(14):
        newIndex = random.choice(llistaIndex)
        indexP.append(newIndex)
        llistaIndex.remove(newIndex)

    for i in range(7):
        x, y = coordinates2Pixels(-22.5, (6.5 + 2.5 * i), 1)
        print(x, y)
        fitxes.sprites()[indexR[i]].moveTo(x,y)

    for i in range(7):
        x, y = coordinates2Pixels(22.5, (6.5 + 2.5 * i), 1)
        fitxes.sprites()[indexH[i]].moveTo(x,y)

    for i in range(14):
        fitxes.sprites()[indexP[i]].directRotate(0)
        fitxes.sprites()[indexP[i]].setBack(True)
        x, y = coordinates2Pixels((-16.25 + 2.5 * i), 47.5, 1)
        fitxes.sprites()[indexP[i]].moveTo(x,y)

    printRutine()
    pygame.display.update()


    #Put upsidedown de rest on the well

printRutine()
pygame.display.update()
## ----- PYGAME ----- ##

## ----- CONTROL LOGIC ----- ##

if __name__ == '__main__':
    print('Modul Control Excecutant')
    
    #Control variables
    isGame = False
    isEnd = False
    isWon = False
    firstTurn = None
    secondTrun = None
    dictionary = None
    toggleTurn = True
    skipButton = False
    skipRobot = False
    winner = None

    gameStatusTEST ={
    'maRobot':{ 
            #idFitxa : [ (x,y,amplada,alçada), [ puntsEsquerra/Dalt, puntsDreta/Baix], orientació]
            0 :[(5,5,4,2),[6,6],0],
            1 :[(5,10,4, 2),[1,2],0],
            2 :[(5,15,4, 2),[3,4],0]
    },
    'maHuma':{ 
        0 :[(55,40,4,2),[3,0],0],
        1 :[(55,45,4, 2),[5,5],0],
        2 :[(5,15,4, 2),[4,1],0]
    },
    'taulell':{},
    'pou':{}
    } #TEST TOKEN MOVEMENT

    #7 peçes repartides a cada jugador (MANUAL)
    #14 peçes restants, al pou (girades) (MANUAL)
    
    simCreateGame()
    
    #IDLE
    goIdle()

    #Read hands for game setup
    #gameStatus = v.getGameStatus() #AFEGIR QUAN VISIÓ 100% IMPLEMENTADA #COMENTAT PER TEST

    firstTurn = d.getFirstTurn(gameStatusTEST) 

    if (firstTurn == "h"):
        secondTrun = "r"
    elif (firstTurn == "r"):
        secondTrun = "h"

    print(firstTurn)
    time.sleep(5)

    
    
    #Signal who starts
    goSignalPlayer(firstTurn)

    #IDLE
    goIdle()
    
    time.sleep(5)
    
    #isGame = True #COMENTAT PER TEST

    while(not isEnd):
        while(isGame):
            
            if(toggleTurn and not skipButton):
                playTurn(firstTurn)
                toggleTurn = False
            elif (not skiprobot):
                playTurn(secondTurn)
                toggleTurn = True

            if(skipButton and skipRobot):
                isGame = False
                isWon = True          
                
        while(isWon):
            if winner != None:
                m.signalPlayer(winner)
                isWon = False
                isEnd = True
            else:
                gameStatus = v.getGameStatus() 
                winner = d.getWinner(gameStatus, firstTurn)
                
    #m.dance() #COMENTAT PER TEST

def setSkipButton(changeskipButton):
    global skipButton
    skipButton = changeskipButton

#Mètode d'I/O del botó de passar torn

def playTurn(player):
    global isGame
    global isWon
    global winner
    playing = True

    #IDLE
    m.idleposition()
    
    if(player == "h"):
        global skipButton
        while playing:
            
            newToken = v.getIfNewTokenOnBoard() #COMENATR PER FER

            #CDETECTAR POU BUIT PER PASSAR

            humanHand = v.getHumanHand()

            if (len(humanHand) == 0): #Assegurar que es pot saber el tamany aixi
                playing = False
                isGame = False
                isWon = True
                winner = "h"
            elif (newToken or skipButton):
                playing = False
                
            time.sleep(1)
    elif(player == "r"):
        global skipRobot

        #IDLE
        m.idlePosition()
        
        while playing:
            #Demanar diccionary estat
            gameStatus = v.getGameStatus()

            #Demanar accio
            action, cToken0, rTokenO, coordinatesD, rotationD = d.doAction(gameStatus) 

            if(action == "t"):
                
                m.moveTo(coordinatesH[0], coordinatesH[1]) #Arreglar al moviment (bloqeuix fins que acaba)
                m.action("c", orientationH) #Arreglar al moviment (bloqeuix fins que acaba)

                m.moveTo(coordinatesB[0], coordinatesB[1])
                m.action("d", orientationB)

                if (len(robotHand) == 1):
                    playing = False
                    isGame = False
                    isWon = True
                    winner = "r"
                    
                playing = False
                
            elif(action == "a"):

                m.moveTo(coordinatesNewToken[0], coordinatesNewToken[1]) #FER Quan simulació
                m.action("c", orientationNT) 

                m.moveTo(coordinatesnewTokenHand[0], coordinatesnewTokenHand[1])

                #IDLE
                m.idlePosition()

            elif(action == "p"):
                skipRobot = True
                m.signalPass()
                
            time.sleep(1)