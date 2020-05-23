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
from moviment import C
import time
import pygame,sys
import math
import time
from pygame.locals import *
import random

from classeFitxa import Fitxa

m = C()
#v = v() #COMENTAT PER TEST

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
primerClick = False
game_rotation= None
simulationRunning = True
tokenMoving = None


pygame.display.update()
initGame = True
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

def getTokenByCoordinates(cX, cY):
    cXP, cYP = coordinates2Pixels(cX, cY, 1)
    global fitxes
    closestToken = None
    closestDist = 5000
    
    for i in fitxes.sprites():
        tX, tY = i.getPosition()
        
        dist = math.sqrt((tX - cXP)**2 + (tY - cYP)**2)

        if dist < closestDist:
            closestDist = dist
            closestToken = i

    return closestToken

def getTokenByPixels(cXP, cYP):
    global fitxes
    closestToken = None
    closestDist = 5000
    
    for i in fitxes.sprites():
        tX, tY = i.getPosition()
        
        dist = math.sqrt((tX - cXP)**2 + (tY - cYP)**2)

        if dist < closestDist:
            closestDist = dist
            closestToken = i

    return closestToken
        

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
def goTo(goX, goY, isDegree, token):
    global next_degreeA
    global next_degreeB
    global degreeA
    global degreeB
    global BposX
    global BposY

    armAReady = False
    armBReady = False

    if isDegree:
        next_degreeA, next_degreeB = goX, goY
    else: 
        next_degreeA, next_degreeB = m.calculate_movement(goX, goY)

    while (not armAReady or not armBReady):
        printRutine()
        if eventQuitFuncion():
            pygame.quit()

        ## Gradual increment of degreeA
        if round(degreeA,1) != round(next_degreeA,1):
            if(degreeA < next_degreeA):
                degreeA +=0.10

            else:
                degreeA -=0.10
        else:
            armAReady = True

        ## Gradual increment of degreeB
        if round(degreeB,1) != round(next_degreeB,1):
            if(degreeB < next_degreeB):
                degreeB +=0.1
            else:
                degreeB -=0.1
        else:
            armBReady = True

        if token != None:
            token.moveTo(BposX, BposY)
        
        pygame.display.update()

def openTool(): 
    global actualOpening
    
    while True:
        printRutine()
        if eventQuitFuncion():
            pygame.quit()
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
        if eventQuitFuncion():
            pygame.quit()
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
        if eventQuitFuncion():
            pygame.quit()
        if(actualHeight > m.operateToolLift(True)):
            actualHeight -=0.1
        else:
            pygame.display.update()
            break
        pygame.display.update()

def downTool():
    global actualHeight

    while True:
        printRutine()
        if eventQuitFuncion():
            pygame.quit()
        if(actualHeight < m.operateToolLift(False)):
            actualHeight +=0.1
        else:
            pygame.display.update()
            break
        pygame.display.update()

def rotateTool(orientation):
    global degreeTool
    next_degreeTool = m.operateToolRotate(orientation)
    
    while True:
        printRutine()
        if eventQuitFuncion():
            pygame.quit()
        if round(degreeTool,2) != round(next_degreeTool,2):
            if(degreeTool < next_degreeTool):
                degreeTool +=0.1
            else:
                degreeTool -=0.1
        else:
            pygame.display.update()
            break   
        pygame.display.update()
        
def goIdle():
    x, y = m.idlePosition()
    goTo(x, y, True, None)

def goSignalPlayer(player):
    x, y = m.signalPlayer(player)
    goTo(x, y, True, None)
    closeTool()
    openTool()
    closeTool()
    openTool()    
    
def goCatch(pX, pY, orientation):
    goTo(pX, pY, False, None)
    rotateTool(orientation)
    downTool()
    closeTool()
    upTool()

def goDrop(pX, pY, orientation, token):
    goTo(pX, pY, False, token)
    rotateTool(orientation)
    downTool()
    openTool()
    token.directRotate(m.operateToolRotate(orientation))
    upTool()

def goDance():
    goTo(0, 20, False, None)
    goTo(5, 25, False, None)
    goTo(0, 30, False, None)
    closeTool()
    openTool()
    goTo(-5, 25, False, None)
    goTo(0, 20, False, None)
    closeTool()
    openTool()
    closeTool()
    openTool()
    goTo(-5, 25, False, None)
    goTo(0, 30, False, None)
    closeTool()
    openTool()
    goTo(5, 25, False, None)
    goTo(0, 20, False, None)
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
    fitxes.update()
    pygame.display.update()


def printTokensFromDictionary(robotTokens, humanTokens, boardTokens, nWell):
    global fitxes

    for i in range len(robotTokens):
        x, y = coordinates2Pixels(-22.5, (6.5 + 2.5 * i), 1)
        fitxes.add(Fitxa(str(robotTokens[i]),x,y,(20,40)))

    for i in range len(humanTokens):
        x, y = coordinates2Pixels(22.5, (6.5 + 2.5 * i), 1)
        fitxes.add(Fitxa(str(humanTokens[i]),x,y,(20,40)))

    for i in range len(boardTokens):
        x, y = coordinates2Pixels(22.5, (6.5 + 2.5 * i), 1)
        newToken = Fitxa(str(boardTokens[i][0]),x,y,(20,40))
        newToken.directRotate() #falta
        fitxes.add(newToken)

    
    for i in range(nWell):
        x, y = coordinates2Pixels((-16.25 + 2.5 * i), 47.5, 1)
        newToken = Fitxa(str(0),x,y,(20,40))
        newToken.directRotate(0)
        newToken.setBack(True)
        fitxes.add(newToken)

    

# ----- DEMO TESTS FOR VIDEO ----- #

# Robot responds to human first turn on a D - N situation. Robot prioratize bigger token with repeated values
def testScenario1():
    print ("test 1")

    # Status
    gameDictionary = {}
    humanTokens = []
    robotTokens = []
    boardTokens = {0: [,]}
    nWell = 0

    # Variables

# ----- DEMO TESTS FOR VIDEO ----- #

def eventQuitFuncion():
    global simulationRunning
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simulationRunning=False
            return True
    return False

def eventMoveTokenFunction():
    global primerClick, game_rotation, tokenMoving
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
        if event.type == MOUSEMOTION:
            mx,my = pygame.mouse.get_pos()
            if tokenMoving != None:
                print("MOVING")
                print()
                tokenMoving.moveTo(mx,my)
                tokenMoving.setBack(False)
                printRutine()
                fitxes.update()
                fitxes.draw(pWindow)
                pygame.display.update()
                
        if event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                mx,my = pygame.mouse.get_pos()
                token = getTokenByPixels(mx, my)
                if token != None:
                    print("CLICK")
                    print()
                    tokenMoving = token
                        
            if pygame.mouse.get_pressed()[2]:
                mx,my = pygame.mouse.get_pos()
                token = getTokenByPixels(mx, my)
                if token != None:
                    print("ROTATION")
                    print()
                    token.rotate(90)
                    printRutine()
                    fitxes.update()
                    fitxes.draw(pWindow)
                    pygame.display.update()

        if event.type == MOUSEBUTTONUP:
            tokenMoving = None


def playTurn(player):
    global isGame
    global isWon
    global winner
    global skipButton
    global skipRobot
    playing = True

    #IDLE
    goIdle()
    #gameStatusStart = v.getGameStatus() ##COMENTAT PER TEST
    
    player = "h" ##TODO treure, es nomes per test 
    
    if(player == "h" and not skipButton):
        skipButton = True
        while playing:
            eventMoveTokenFunction()
            #gameStatus = v.getGameStatus() ##COMENTAT PER TEST
            
            #Ha tirat
##            if len(gameStatus["taulell"]) > len(gameStatusStart["taulell"]):
##                #Ha guanyat
##                if (len(gameStatus["maHuma"]) == 0):
##                    playing = False
##                    isGame = False
##                    isWon = True
##                    winner = "h"
##                else:
##                    playing = False
##
##            elif len(gameStatus["pou"]) == 0:
##                #Ha passat
##                skipButton = True
##                playing = False
                
            time.sleep(1)
            
    elif(player == "r" and not skipRobot):
        skipRobot = True
        while playing:
            #Demanar diccionary estat
            gameStatus = v.getGameStatus()

            #Demanar accio
            action, cToken0, coordinatesD, rotationD = d.doAction(gameStatus) 

            if(action == "t"):
                
                goCatch(cToken0[0], cToken0[1], "N")
                token = getTokenByCoordinates(cToken0[0], cToken0[1])
                goDrop(coordinatesD[0], coordinatesD[1], rotationD, token)

                if (len(robotHand) == 1):
                    playing = False
                    isGame = False
                    isWon = True
                    winner = "r"
                    
                playing = False
                
            elif(action == "a"):

                goCatch(cToken0[0], cToken0[1], "W")
                token = getTokenByCoordinates(cToken0[0], cToken0[1])
                goDrop(coordinatesD[0], coordinatesD[1], rotationD, token)
                token.setBack(False)

                #IDLE
                m.idlePosition()

            elif(action == "p"):
                skipRobot = True
                playing = False
                m.signalPass()
                
            time.sleep(1)



def mainControlFunction():
    global isEnd, isGame, toggleTurn, isWon, gameStatus, winner, initGame
    
    ## TEST MOVIMENT DE FITXA ##

    ##time.sleep(1)
    ##goCatch(20, 47.5, "N")
    ##token = getTokenByCoordinates(20, 47.5)
    ##goDrop(0, 25, "W", token)
    ##token.setBack(False)

    ## TEST MOVIMENT DE FITXA ##
    gameStatusTEST ={
    'maRobot':{ 
            #idFitxa : [ (x,y,amplada,alçada), [ puntsEsquerra/Dalt, puntsDreta/Baix], orientació]
            0 :[(5,5,4,2),[3,0],0],
            1 :[(5,10,4, 2),[1,2],0],
            2 :[(5,15,4, 2),[3,4],0]
    },
    'maHuma':{ 
        0 :[(55,40,4,2),[6,6],0],
        1 :[(55,45,4, 2),[5,5],0],
        2 :[(5,15,4, 2),[4,1],0]
    },
    'taulell':{},
    'pou':{}
    } #TEST TOKEN MOVEMENT

    if initGame:
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
    
        time.sleep(1)

        #Signal who starts
        goSignalPlayer(firstTurn)

        #IDLE
        goIdle()
    
        time.sleep(1)
    
        isGame = True
        initGame = False

    if not isEnd:
        print("This is not the END")
        if isGame:
            print("IS GAME")
            if(toggleTurn):
                playTurn(firstTurn)
                toggleTurn = False
            else:
                playTurn(secondTurn)
                toggleTurn = True

            if(skipButton and skipRobot):
                isGame = False
                isWon = True
        if isWon:
            if winner != None:
                m.signalPlayer(winner)
                isWon = False
                isEnd = True
            else:
                gameStatus = v.getGameStatus() 
                winner = d.getWinner(gameStatus, firstTurn)
                
    #m.dance() #COMENTAT PER TEST


       
#--------------------------------------------------------------------------------------#
#   SIMULATION                                                                         #
#--------------------------------------------------------------------------------------#
printRutine()
simCreateGame()
while(simulationRunning):
    eventQuitFuncion()
    mainControlFunction()
    pygame.display.update()

pygame.quit()
