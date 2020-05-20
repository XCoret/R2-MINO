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
import moviment as m
import time

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
    } 
    
    #m = m() #COMENTAT PER TEST
    #v = v() #COMENTAT PER TEST

    #7 peçes repartides a cada jugador (MANUAL)
    #14 peçes restants, al pou (girades) (MANUAL)
    
    #IDLE
    #m.idlePosition() #COMENTAT PER TEST

    #Read hands for game setup
    #gameStatus = v.getGameStatus() #AFEGIR QUAN VISIÓ 100% IMPLEMENTADA #COMENTAT PER TEST

    firstTurn = d.getFirstTurn(gameStatusTEST) 

    if (firstTurn == "h"):
        secondTrun = "r"
    elif (firstTurn == "r"):
        secondTrun = "h"

    print(firstTurn)
    #Signal who starts
    #m.signalPlayer(firstTurn) #COMENTAT PER TEST

    #IDLE
    #m.idlePosition() #COMENTAT PER TEST
            
    #time.sleep(5) #COMENTAT PER TEST
    
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

            #Demanar accio ARREGLAR
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
