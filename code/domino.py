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

def getDoublesAndMax(hand):
    maxDouble = -1
    maxSum = 0

    maxFirst = -1
    maxSecond = -1

    indexMax = -1
    indexDouble = -1
    
    for key in hand:
        token = hand[key]
        numbers = token[1]
        first = numbers[0]
        second = numbers[1]
        sumNumbers = first + second
        #Buscar fitxa mès alta
        if sumNumbers > maxSum:
            maxSum = sumNumbers
            maxFirst = first
            maxSecond = second
            indexMax = key
        #Buscar per dobles
        if(first == second and first > maxDouble):
            maxDouble = first
            indexDouble = key

    return maxDouble, maxSum, indexMax, indexDouble

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
     
    maxDoubleRobot, maxSumRobot, indexMaxRobot, indexDoubleRobot = getDoublesAndMax(robotHand)
    maxDoubleHuman, maxSumHuman, indexMaxHuman, indexDoubleHuman = getDoublesAndMax(humanHand)

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
    if pointsRobot < pointsHuman:
        print("Winner ROBOT")
        return "r"
    elif pointsRobot > pointsHuman:
        print("Winner HUMAN")
        return "h"
    elif pointsRobot == pointsHuman:
        print("EMPAT, guanya qui té el torn")
        return firstTurn

def getEndings(board):
    contiguous = {}
    valuesFrom = {}
    for key in board: 
        token = board[key]
        tokenPos = token[0]
        tokenX = tokenPos[0]
        tokenY = tokenPos[1]
        nearest = []

        for near in board:
            if key != near:
                ntoken = board[near]
                ntokenPos = ntoken[0]
                ntokenX = ntokenPos[0]
                ntokenY = ntokenPos[1]
                diffX = tokenX-ntokenX
                diffY = tokenY-ntokenY
                if diffX <= 4 and diffX >=-4 and diffY <= 4 and diffY >=-4:
                    nearest.append(near)
        contiguous[key] = nearest
        print(key, ": ",contiguous[key])

        ending1 = None
        ending2 = None
        contiguous1 = None
        contiguous2 = None
        for j in contiguous:
            if len(contiguous[j]) < 2:
                if ending1 == None:
                    ending1 = j
                    contiguous1 = contiguous[j][0]
                else:
                    ending2 = j
                    contiguous2 = contiguous[j][0]

    print("ENDINGS: ", ending1, ", ", ending2)
    print("CONT: ", contiguous1, ", ", contiguous2)
    return ending1, ending2, contiguous1, contiguous2

# return action, cToken0, cToken1
# action "t" -> tirar
# action "a" -> agafar
# action "p" -> passar
# cToken0: token a moure
# cToken1: token resultant de moure cToken0
def doAction(gameDictionary):
    robotHand = gameDictionary["maRobot"]
    board = gameDictionary["taulell"]
    well = gameDictionary["pou"]

    tokensInBoard = len(board)
    
    ending1, ending2, contiguous1, contiguous2 = getEndings(board)


    #if tokensInBoard == 0:
        ## tirar el doble mes alt, o la fitxa mes alta
    

    #intenta tirar segons regles del domino

    #Si no es pot tirar return


e1={
    'maRobot':{ 
            #idFitxa : [ (x,y,amplada,alçada), [ puntsEsquerra/Dalt, puntsDreta/Baix], orientació]
            0 :[(5,5,4,2),[1,1],0],
            1 :[(5,10,4, 2),[4,4],0],
            2 :[(5,15,4, 2),[4,2],0],
            3 :[(5,20,4, 2),[2,3],0]  
    },
    'maHuma':{ 
        0 :[(55,40,4,2),[1,2],0],
        1 :[(55,45,4, 2),[5,0],0] 
    },
    'taulell':{ 
        0 :[(26,24,4,2),[4,3],1],
        1 :[(23,25,4, 2),[6,3],0],
        2 :[(20,25,4, 2),[6,6],1]    
    },
    'pou':{}
}

doAction(e1)
