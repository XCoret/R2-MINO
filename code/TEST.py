##def aux():
##    global isGame
##    isGame = True
##    
##if __name__ == '__main__':
##    isGame = False
##    print (isGame)
##    aux()
##    print (isGame)

##possibleTokens = [[(5,5,4,2),[1,1],0],[(5,5,4,2),[2,3],0],[(5,5,4,2),[4,4],0],[(5,5,4,2),[6,1],0]]
possibleTokens = [[(5,5,4,2),[4,1],0],[(5,5,4,2),[3,4],0],[(5,5,4,2),[3,5],0],[(5,5,4,2),[1,1],0]]

def getDoublesIndex(possibleTokens):
    doubles = {}
    iteration = 0
    for check in possibleTokens:
        if check[1][0] == check[1][1]:
            doubles[iteration] = check[1][0]
        iteration += 1
    return sorted(doubles.items(), key=lambda x: x[1], reverse=True)

##doubles = getDoublesIndex(possibleTokens)
##
##print(doubles)
##
##print(list(doubles)[0:1][0][0]) 

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
    return repeaters

##repeaters = getrepeatedIndex(possibleTokens)
##
##print(repeaters)
##
##print(sorted(repeaters, key = lambda x: int(x[2]), reverse=True))
##
##print(sorted(repeaters, key = lambda x: int(x[2]), reverse=True)[0][0])

def getsortedByValueIndex(possibleTokens):
    sortedByValue = {}
    iteration = 0
    for check in possibleTokens:
        sortedByValue[iteration] = check[1][0] + check[1][1]
        iteration += 1
        print("Entro")
    
    return sorted(sortedByValue.items(), key=lambda x: x[1], reverse=True)

sortede = getsortedByValueIndex(possibleTokens)

print(sortede)

print(sortede[0][0])
