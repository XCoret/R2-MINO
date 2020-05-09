# -*- coding: utf-8 -*-
'''
S’encarrega de definir la jugada a realitzar a partir de l’estat de la 
partida que rep del mòdul Control i també del nivell de dificultat seleccionat.
'''

'''
Classe fitxa:
    va : valor extrem A
    vb : valor extrem B
    orientacio : (0:horitzontal, 1:vertical)
'''
print('Modul Joc Carregat!')

def getFirstTurn(gameDictionary):
    humanHand = gameDictionary["maHuma"]
    robotHand = gameDictionary["maRobot"]
    maxDoubleHuman = -1
    maxDoubleRobot = -1

    maxSumHuman = 0
    maxSumRobot = 0
    
    maxFirstRobot = -1
    maxSecondRobot = -1
    
    maxFirstHuman = -1
    maxSecondHuman = -1
     
    for key in robotHand:
        token = robotHand[key]
        numbers = token[1]
        first = numbers[0]
        second = numbers[1]
        sumNumbers = first + second
        #Buscar fitxa mès alta
        if sumNumbers > maxSumRobot:
            maxSumRobot = sumNumbers
            maxFirstRobot = first
            maxSecondRobot = second
        #Buscar per dobles
        if(first == second and first > maxDoubleRobot):
            maxDoubleRobot = first

    for key in humanHand:
        token = humanHand[key]
        numbers = token[1]
        first = numbers[0]
        second = numbers[1]
        sumNumbers = first + second
        #Buscar fitxa mès alta
        if sumNumbers > maxSumHuman:
            maxSumHuman = sumNumbers
            maxFirstHuman = first
            maxSecondHuman = second
        #Buscar per dobles
        if(first == second and first > maxDoubleHuman):
            maxDoubleHuman = first

    print("-----------------------------------------------------------------------")
    print("maxDoubleRobot: ", maxDoubleRobot, " maxDoubleHuman: ", maxDoubleHuman)
    print("maxSumRobot: ", maxSumRobot, " maxSumHuman: ", maxSumHuman)
    print("-----------------------------------------------------------------------")
    
    if maxDoubleHuman < maxDoubleRobot:
        print("Winner ROBOT with DOUBLE: [", maxDoubleRobot, ",", maxDoubleRobot, "]")
        return "r"
    elif maxDoubleHuman > maxDoubleRobot:
        print("Winner HUMAN with DOUBLE: [", maxDoubleHuman, ",", maxDoubleHuman, "]")
        return "h"
    else:
        print("NOBODY HAS DOUBLES!")
        if maxSumRobot > maxSumHuman:
            print("Winner ROBOT with: [", maxFirstRobot, ",", maxSecondRobot, "] TOTAL:", maxSumRobot)
            return "r"
        elif maxSumRobot < maxSumHuman:
            print("Winner HUMAN with: [", maxFirstHuman, ",", maxSecondHuman, "] TOTAL:", maxSumHuman)
            return "h" 

def getWinner(gameDictionary, firstTurn):
    humanHand = gameDictionary["maHuma"]
    robotHand = gameDictionary["maRobot"]

    pointsHuman = 0
    pointsRobot = 0

    #Comptar les fitxes de cada mà
    for key in robotHand:
        token = robotHand[key]
        numbers = token[1]
        first = numbers[0]
        second = numbers[1]
        sumNumbers = first + second
        pointsRobot += sumNumbers

    for key in humanHand:
        token = humanHand[key]
        numbers = token[1]
        first = numbers[0]
        second = numbers[1]
        sumNumbers = first + second
        pointsHuman += sumNumbers

    print("ROBOT:", pointsRobot, "  HUMAN:", pointsHuman)
    if pointsRobot > pointsHuman:
        print("Winner ROBOT")
        return "r"
    elif pointsRobot < pointsHuman:
        print("Winner HUMAN")
        return "h"
    elif pointsRobot == pointsHuman:
        print("EMPAT, guanya qui té el torn")
        return firstTurn

#return "t" -> tirar
#return "a" -> agafar
#return "p" -> passar
def doAction(gameDictionary):
    robotHand = gameDictionary["maRobot"]
    board = gameDictionary["taulell"]
    well = gameDictionary["pou"]

    #intenta tirar segons regles del domino

    #Si no es pot tirar return

