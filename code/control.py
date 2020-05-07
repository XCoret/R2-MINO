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
import visio as v
import moviment as m
import time

if __name__ == '__main__':
    print('Modul Control Excecutant')
    #d.func()
    #v.llegirImatge('src/domino.jpg')
    #print(m.getMovementTo(4,4,4))
    isGame = False
    isSetup = True
    isEnd = False
    isWon = False
    firstTurn = None
    secondTrun = None
    dictionary = None
    toggleTurn = True
    skipButton = False
    skipRobot = False
    winner = None
    m = m()

    while (!isEnd):
        #7 peçes repartides a cada jugador (MANUAL)
        #14 peçes restants, al pou (girades) (MANUAL)
        #IDLE
        m.idlePosition()
        
        if (isSetup):
            #Llegir mans
            humanHand = v.getHumanHand() #COMENATR PER FER
            robotHand = v.getRobotHand() #COMENATR PER FER

            firstTurn = d.getFirstTurn(humanHand, robotHand) #FER A DOMINO

            if (firstTurn == "h"):
                secondTrun = "r"
            elif (firstTurn == "r"):
                secondTrun = "h"
            
            #Robot senyala el que té el doble mès gran per començar
            m.signalPlayer(firstTurn) #FER A MOVIMENT (ull a bloquejar-se fins acabar, posar en IDLE)

            #IDLE
            m.idlePosition()
            
            time.sleep(5)
            
            isSetup = False
            isGame = True

        while(isGame):
            
            if(toggleTurn and not skipButton):
                playTurn(firstTurn)
                toggleTurn = False
            elif:
                if(skiprobot):
                    m.signalPass()
                else:
                    playTurn(secondTurn)
                    toggleTurn = True

            if(skipButton and skipRobot):
                isGame = False
                isWon = True
                
                
        if(isWon):
            global winner
            if winner != None:
                m.signalPlayer(winner)
                #Play music
                isWon = False
                isEnd = True
            else:
                humanHand = v.getHumanHand() 
                robotHand = v.getRobotHand()

                winner = d.getWinner(humanHand, robotHand) #FER A DOMINO
                
    m.dance() #FER A MOVIMENT

#Mètode que crida visió per iniciar el setup
def setSetup(changeSetup):
    global isSetup
    isSetup = changeStart

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

            humanHand = v.getHumanHand()

            if (humanHand.size() == 0): #Assegurar que es pot saber el tamany aixi
                playing = False
                isGame = False
                isWon = True
                winner = "h"
            elif (newToken or skipButton):
                playing = False
                
            time.sleep(1)
    elif(player == "r"):
        global skipRobot
        
        while playing:
            #Demanar diccionary estat
            dictionary = v.getBoardState() #COMENATR PER FER
            robotHand = v.getRobotHand()
            well = v.getWellState() #COMENATR PER FER

            #Demanar accio
            action, tokenH, tokenB = d.doAction(dictionary, robotHand, well) #FER A DOMINO, arreglar amb tipus de dades

            if(action == "t"):
                #demanar coordenades d'origen i destí del Token en questió
                coordinatesH, orientationH = v.getTokenCoordinates(tokenH) #COMENATR PER FER
                coordinatesB, orientationB = v.getTokenCoordinates(tokenB)
                
                m.moveTo(coordinatesH[0], coordinatesH[1]) #Arreglar al moviment (bloqeuix fins que acaba)
                m.action("c", orientationH) #Arreglar al moviment (bloqeuix fins que acaba)

                m.moveTo(coordinatesB[0], coordinatesB[1])
                m.action("d", orientationB)

                if (robotHand.size() == 1): #Assegurar que es pot saber el tamany aixi
                    playing = False
                    isGame = False
                    isWon = True
                    winner = "r"
                    
                playing = False
                
            elif(action == "a"):
                coordinatesNewToken, orientationNT = v.getRandomWellToken() #COMENATR PER FER
                coordinatesnewTokenHand, orientationNTH = v.getEmptyHandSpace() #COMENATR PER FER

                m.moveTo(coordinatesNewToken[0], coordinatesNewToken[1]) #Arreglar al moviment (bloqeuix fins que acaba)
                m.action("c", orientationNT) #Arreglar al moviment (bloqeuix fins que acaba)

                m.moveTo(coordinatesnewTokenHand[0], coordinatesnewTokenHand[1])
                m.action("d", orientationNTH) #ARREGLAT

                #IDLE
                m.idlePosition()

            elif(action == "p"):
                skipRobot = True
                m.signalPass() #FER a MOVIEMTN
                
            time.sleep(1)
        




def pygmageIdle
