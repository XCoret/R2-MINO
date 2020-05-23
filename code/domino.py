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
import math

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
    print("getWinner")
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

def common_elements(list1, list2):
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return result

def getPossibleTokensToPlay(extrems, hand):
    numbers = []
    for i in extrems.keys():
        numbers.append(extrems[i][3])
    
    possibleTokens =  []
    for i in numbers:
        for j in hand.keys():
            if (hand[j][1][0] == i or hand[j][1][1] == i):
                possibleTokens.append(hand[j])
            
    print("POSSIBLE TOKENS ", possibleTokens)
    return possibleTokens

def getRandomTokenFromWell(well):
    randomTokenIndex = random.randint(0,(len(well)-1))
    return well[randomTokenIndex]

def getEmptySpaceFromHand(robotHand):
    if(len(robotHand) <= 11):
        y = 6.5 + (2.5* (len(robotHand)))
        return [-22.5, y]
    else:
        y = 6.5 + (2.5* (len(robotHand) - 12))
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
        bestOption = possibleTokens[list(doublesIndexes)[0:1][0][0]]
    elif len(repeatedIndexes) > 0:
        #Retorna el repetit mès gran
        bestOption = possibleTokens[repeatedIndexes[0][0]]
    else:
        #Retorna el mès gran
        bestOption = possibleTokens[sortedByValue[0][0]]

    print("BEST OPTION ", bestOption)
    return bestOption

def calculateOrientation(orientationO, extremValue, token):
    isFirst = None
    if (extremValue == token[1][0]):
        isFirst == True
    elif (extremValue == token[1][1]):
        isFirst == False
        
    if (orientationO == "N"):
        if isFirst:
            return "W"
        else:
            return "E"        
    elif (orientationO == "S"):
        if isFirst:
            return "E"
        else:
            return "W" 
    elif (orientationO == "E"):
        if isFirst:
            return "N"
        else:
            return "S" 	
    elif (orientationO == "W"):
        if isFirst:
            return "S"
        else:
            return "N"

def getClosestToken(board, extrem):
    closestToken = None
    closestDist = 5000
    cXP = extrem[0][0]
    cYP = extrem[0][1]

    if len(board) == 1:
        closestToken = board[0]
    else:
        for i in board:
            tX = board[i][0][0]
            tY = board[i][0][1]
            
            dist = math.sqrt((tX - cXP)**2 + (tY - cYP)**2)

            if dist < closestDist and board[i][1] != extrem[1]:
                closestDist = dist
                closestToken = board[i]

    return closestToken

def getDirectionsBlocked(proxima, extrem):
    print("proxima ", proxima)
    print("extrem ", extrem)
    blockedList = []
    if (extrem[0][0] > proxima[0][0]):
        blockedList.append("W")
    else:
        blockedList.append("E")
    if (extrem[0][1] > proxima[0][1]):
        blockedList.append("S")
    else:
        blockedList.append("N")
    return blockedList

def getDistancesFromBoard(cXR, cYR, isExtremDouble, isExtremVertical):
    distDict = {}

    distDict["N"] = abs(cYR - 45)
    distDict["S"] = abs(cYR - 5)
    distDict["E"] = abs(cXR - 20)
    distDict["W"] = abs(cXR + 20)
    
    if isExtremDouble:
        if isExtremVertical:
            distDict["N"] = abs(cYR - 45) - 1
            distDict["S"] = abs(cYR - 5) - 1
        else:
            distDict["E"] = abs(cXR - 20) - 1
            distDict["W"] = abs(cXR + 20) - 1

    #Ordenar de mès gran a mès petit
    distDict = {k: v for k, v in sorted(distDict.items(), key=lambda item: item[1], reverse=True)}
    
    return distDict

def placeToken(board, extrem, extremValue, token):
    isExtremVertical = None
    isExtremDouble = None
    isTokenDouble = None
    isFirstValue = None
    cXR = None
    cYR = None
    cXA = None
    cYA = None
    
    # Trobar peça proxima a extrem
    proxima = getClosestToken(board, extrem)
    
    # Saber tipus de extrem, i token    
    if (extrem[2] == 1):
        isExtremVertical = True
    else:
        isExtremVertical = False
        
    if (extrem[1][0] == extrem[1][1]):
        isExtremDouble = True
    else:
        isExtremDouble = False

    if (token[1][0] == token[1][1]):
        isTokenDouble = True
    else:
        isTokenDouble = False

    #Eliminar direcció que bloqueja la proxima
    dirBlocked = getDirectionsBlocked(proxima, extrem)
    print ("dirBlocked ", dirBlocked)

    #Trobar cooredenades de referéncia
    if isExtremDouble:
        (cXR, cYR) = extrem[0][0:2]
    else:
        if isExtremVertical:
            if (extrem[1][0] == extremValue):
                isFirstValue = True
                cXR = extrem[0][0]
                cYR = extrem[0][1] + 1
                
            elif (extrem[1][1] == extremValue):
                isFirstValue = False
                cXR = extrem[0][0]
                cYR = extrem[0][1] - 1
        else:
            if (extrem[1][0] == extremValue):
                isFirstValue = True
                cXR = extrem[0][0] - 1
                cYR = extrem[0][1]
                
            elif (extrem[1][1] == extremValue):
                isFirstValue = False
                cXR = extrem[0][0] + 1
                cYR = extrem[0][1]

    # Calcular proximitat amb les parets respecte del cooredenades calculades de referéncia per ordre considerant la orientació del doble
    distDict = getDistancesFromBoard(cXR, cYR, isExtremDouble, isExtremVertical)

    # Restar les ja descartades del diccionari de longituds
    for i in dirBlocked:
        distDict.pop(i, None)

    # Si extrem Normal - nou token Doble
    if (not isExtremDouble and isTokenDouble):
        print ("N - D Situation")
        if isExtremVertical:
            if isFirstValue:
                cXA = cXR
                cYA = cYR + 2
            else:
                cXA = cXR
                cYA = cYR - 2
            return [(cXA, cYA), "S"]
        else:
            if isFirstValue:
                cXA = cXR - 2
                cYA = cYR
            else:
                cXA = cXR + 2
                cYA = cYR
            return [(cXA, cYA), "E"]

    # Si extrem Doble - nou token Normal
    elif (isExtremDouble and not isTokenDouble):
        print ("D - N Situation")
        direccio = next(iter(distDict))
        if isExtremVertical:
            if (direccio == "N"):
                cXA = cXR
                cYA = cYR + 4
            elif (direccio == "S"):
                cXA = cXR
                cYA = cYR - 4
            elif (direccio == "E"):
                cXA = cXR + 3
                cYA = cYR 
            elif (direccio == "W"):
                cXA = cXR - 3
                cYA = cYR 
        else:
            if (direccio == "N"):
                cXA = cXR
                cYA = cYR + 3
            elif (direccio == "S"):
                cXA = cXR
                cYA = cYR - 3
            elif (direccio == "E"):
                cXA = cXR + 4
                cYA = cYR 
            elif (direccio == "W"):
                cXA = cXR - 4
                cYA = cYR 
         
        return [(cXA, cYA), calculateOrientation(direccio, extremValue, token)]

    # Si extrem Normal - nou token Normal
    elif (not isExtremDouble and not isTokenDouble):
        print ("N - N Situation ", cXR , " ", cYR)
        direccio = next(iter(distDict))
        print ("direccio ", direccio)

        if (direccio == "N"):
            cXA = cXR
            cYA = cYR + 3
        elif (direccio == "S"):
            cXA = cXR
            cYA = cYR - 3
        elif (direccio == "E"):
            cXA = cXR + 3
            cYA = cYR 
        elif (direccio == "W"):
            cXA = cXR - 3
            cYA = cYR
            
        print ("FINAL COORDINATES ", cXA , " ", cYA)
        return [(cXA, cYA), calculateOrientation(direccio, extremValue, token)]


# return action, coordinatesO, coordinatesD, orientationD
# action "t" -> tirar
# action "a" -> agafar
# action "p" -> passar
def doAction(gameDictionary):
    robotHand = gameDictionary["maRobot"]
    board = gameDictionary["taulell"]
    well = gameDictionary["pou"]
    
    if len(board) == 0:
        ## la partida acaba de començar
        md, ms, indexMaxRobot, indexDoubleRobot = getDoublesAndMax(robotHand)
        if indexDoubleRobot != -1:
            firstToken = robotHand[indexDoubleRobot]
        else:
            firstToken = robotHand[indexMaxRobot]

        coordinatesO = firstToken[0][0:2]
        coordinatesD = (0, 25)
        orientationD = "W"
        
        #TIRAR
        return "t", coordinatesO, coordinatesD, orientationD
        
    elif len(board) >= 1:
        extrems = gameDictionary["extrems"]
        possibleTokens = getPossibleTokensToPlay(extrems, robotHand) 
        
        if len(possibleTokens) == 0:
            if len(well) == 0:
                # PASSAR
                return "p", None, None, None
            else:
                token = getRandomTokenFromWell(well)
                coordinatesD = getEmptySpaceFromHand(robotHand)
                coordinatesO = token[0][0:2]
                # AGAFAR
                return "a", coordinatesO, coordinatesD, "N"
        else:
            extrem = None
            extremValue = None
            
            token = getBestOption(possibleTokens)

            if (token[1][0] == extrems[0][3] or token[1][1] == extrems[0][3]):
                extrem = extrems[0]
                extremValue = extrems[0][3]
            elif (token[1][0] == extrems[1][3] or token[1][1] == extrems[1][3]):
                extrem = extrems[1]
                extremValue = extrems[1][3]

            coordinatesD, orientationD = placeToken(board, extrem, extremValue, token)
            print ("FINAL ORIENTATION: ", orientationD)
            coordinatesO = token[0][0:2]
            # TIRAR
            return "t", coordinatesO, coordinatesD, orientationD


## TESTS ##
##e1={
##    'maRobot':{ 
##            #idFitxa : [ (x,y,amplada,alçada), [ puntsEsquerra/Dalt, puntsDreta/Baix], orientació]
##            0 :[(5,5,4,2),[1,1],0],
##            1 :[(5,10,4, 2),[4,4],0],
##            2 :[(5,15,4, 2),[4,2],0],
##            3 :[(5,20,4, 2),[2,3],0]  
##    },
##    'maHuma':{ 
##        0 :[(55,40,4,2),[1,2],0],
##        1 :[(55,45,4, 2),[5,0],0] 
##    },
##    'taulell':{ 
##        0 :[(26,24,4,2),[4,3],1],
##        1 :[(23,25,4, 2),[6,3],0],
##        2 :[(20,25,4, 2),[6,6],1]    
##    },
##    'pou':{}
##}
##
##doAction(e1)

#TO-DO: Col·locar la nova peça
