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
import random

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
    
    if maxDoubleHuman < maxDoubleRobot:
        return "r"
    elif maxDoubleHuman > maxDoubleRobot:
        return "h"
    else:
        if maxSumRobot > maxSumHuman:
            return "r"
        elif maxSumRobot < maxSumHuman:
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

    if pointsRobot < pointsHuman:
        return "r"
    elif pointsRobot > pointsHuman:
        return "h"
    elif pointsRobot == pointsHuman:
        # EMPAT, guanya qui té el torn
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

    return ending1, ending2, contiguous1, contiguous2

def setNewPosition(token, x, y, o):
    newToken = token.copy()
    newToken[0] = (x,y,4,2)
    newToken[2] = o
    return newToken

def common_elements(list1, list2):
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return result

def getPossibleTokensToPlay(numbers, hand):
    possibleTokens =  {}
    for key in hand:
        token = hand[key]
        tokenValues = token[1]
        commons = common_elements(tokenValues, numbers)
        for i in commons:
            possibleTokens[i] = key
    return possibleTokens

def getRandomTokenFromWell(well):
    randomTokenIndex = random.randint(0,len(well))
    return well[randomTokenIndex]

def getEmptySpaceFromHand(robotHand):
    if(len(robotHand) <= 11):
        y = 6 + (2.5* (len(robotHand) - 1))
        return [-22.5, y]
    else:
        y = 6 + (2.5* (len(robotHand) - 12))
        return [-27, y]

def getDoublesIndex(possibleTokens):
    doubles = {}
    iteration = 0
    for check in possibleTokens:
        if check[1][0] == check[1][1]:
            doubles[iteration] = check[1][0]
        iteration += 1
    return sorted(doubles.items(), key=lambda x: x[1], reverse=True)

def getrepeatedIndex(possibleTokens):
    repeaters = []
    iteration = 0
    for check in possibleTokens:
        iteration2 = 0
        for compare in possibleTokens:
            if iteration != iteration2:
                if check[1][0] == compare[1][0] or check[1][0] == compare[1][1]:
                    repeaters.append([iteration, check[1][0], (check[1][0] + check[1][1])])
                elif check[1][1] == compare[1][0] or check[1][1] == compare[1][1]:
                    repeaters.append([iteration, check[1][1],(check[1][0] + check[1][1])])
            iteration2 += 1
        iteration += 1
    return sorted(repeaters, key = lambda x: int(x[2]), reverse=True)

def getsortedByValueIndex(possibleTokens):
    sortedByValue = {}
    iteration = 0
    for check in possibleTokens:
        sortedByValue[iteration] = check[1][0] + check[1][1]
        iteration += 1
    
    return sorted(sortedByValue.items(), key=lambda x: x[1], reverse=True)

def getBestOption(possibleTokens):
    # Dobles
    doublesIndexes = getDoublesIndex(possibleTokens)
    # Numeros Repetits
    repeatedIndexes = getrepeatedIndex(possibleTokens)
    # Mes grans
    sortedByValue = getsortedByValueIndex(possibleTokens)

    if len(doublesIndexes) > 0:
        #Retorna el doble mès gran
        return possibleTokens[list(doublesIndexes)[0:1][0][0]]
    elif len(repeatedIndexes) > 0:
        #Retorna el repetit mès gran
        return possibleTokens[repeatedIndexes[0][0]]
    else:
        #Retorna el mès gran
        return possibleTokens[sortedByValue[0][0]]
        

# return action, cToken0, cToken1
# action "t" -> tirar
# action "a" -> agafar
# action "p" -> passar
# firstToken: token a moure
# secondToken: token resultant de moure cToken0
def doAction(gameDictionary):
    robotHand = gameDictionary["maRobot"]
    board = gameDictionary["taulell"]
    well = gameDictionary["pou"]

    firstToken = None
    secondToken = None
    tokensInBoard = len(board)
    
    if len(board) == 0:
        ## la partida acaba de començar
        md, ms, indexMaxRobot, indexDoubleRobot = getDoublesAndMax(robotHand)
        if indexDoubleRobot != -1:
            firstToken = robotHand[indexDoubleRobot]
        else:
            firstToken = robotHand[indexMaxRobot]

        # center table
        x = 30
        y = 30
        o = 1
        secondToken = setNewPosition(firstToken, x, y, o)
        #TIRAR
        return "t", firstToken, secondToken
        
    elif len(board) == 1:
        tokenBoard = board[0]
        possibleNumbers = tokenBoard[1]
        possibleTokens = getPossibleTokensToPlay(possibleNumbers, robotHand)
        if len(possibleTokens) == 0:
            if len(well) == 0:
                # PASSAR
                return "p", None, None
            else:
                firstToken = getRandomTokenFromWell(well)
                handPlaceCoordinates = getEmptySpaceFromHand(robotHand)
                # AGAFAR
                return "a", firstToken, handPlaceCoordinates
        else:
            # choose best token from possibleTokens
            bestOption = getBestOption(possibleTokens)
            # secondToken = calculateNewPosition(firstToken, tokenBoard) #Equip Visio
            # TIRAR
            return "t", firstToken, secondToken
        
    elif len(board) > 1:
        ending1, ending2, contiguous1, contiguous2 = getEndings(board)
        #possibleNumbers = getPossibleNumbers(ending1, ending2, contiguous1, contiguous2) #Marian
        possibleNumbers = [] #AUXILIAR
        possibleTokens = getPossibleTokensToPlay(possibleNumbers, robotHand)
        if len(possibleTokens) == 0:
            if len(well) == 0:
                # PASSAR
                return "p", None, None
            else:
                firstToken = getRandomTokenFromWell(well)
                handPlaceCoordinates = getEmptySpaceFromHand(robotHand)
                # AGAFAR
                return "a", firstToken, handPlaceCoordinates
        else:
            # choose best token from possibleTokens
            firstToken = getBestOption(possibleTokens)
            # boardCoordinates = calculateNewPosition(firstToken, endingUsed)
            return "t", firstToken, boardCoordinates


## TESTS ##
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

#TO-DO: Col·locar la nova peça
