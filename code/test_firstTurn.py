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




# ROBOT WIN per doble [4,4]
e1={
    'maRobot':{ 
            #idFitxa : [ (x,y,amplada,alçada), [ puntsEsquerra/Dalt, puntsDreta/Baix], orientació]
            0 :[(5,5,4,2),[1,1],0],
            1 :[(5,10,4, 2),[4,4],0],
            2 :[(5,15,4, 2),[4,2],0],
            3 :[(5,220,4, 2),[2,3],0]  
    },
    'maHuma':{ 
        0 :[(55,40,4,2),[1,2],0],
        1 :[(55,45,4, 2),[5,0],0] 
    },
    'taulell':{ 
        0 :[(25,23,4,2),[4,3],1],
        1 :[(23,25,4, 2),[6,3],0],
        2 :[(21,25,4, 2),[6,6],1]    
    },
    'pou':{}
}

# ROBOT WIN per doble [1,1]
e2={
    'maRobot':{ 
            #idFitxa : [ (x,y,amplada,alçada), [ puntsEsquerra/Dalt, puntsDreta/Baix], orientació]
            0 :[(5,5,4,2),[1,1],0],
            1 :[(5,10,4, 2),[4,0],0],
            2 :[(5,15,4, 2),[4,2],0],
            3 :[(5,220,4, 2),[2,3],0]  
    },
    'maHuma':{ 
        0 :[(55,40,4,2),[1,2],0],
        1 :[(55,45,4, 2),[0,0],0] 
    },
    'taulell':{ 
        0 :[(25,23,4,2),[4,3],1],
        1 :[(23,25,4, 2),[6,3],0],
        2 :[(21,25,4, 2),[6,6],1]    
    },
    'pou':{}
}

# HUMAN WIN per doble [5,5]
e3={
    'maRobot':{ 
            #idFitxa : [ (x,y,amplada,alçada), [ puntsEsquerra/Dalt, puntsDreta/Baix], orientació]
            0 :[(5,5,4,2),[1,1],0],
            1 :[(5,10,4, 2),[4,4],0],
            2 :[(5,15,4, 2),[4,2],0],
            3 :[(5,220,4, 2),[2,3],0]  
    },
    'maHuma':{ 
        0 :[(55,40,4,2),[1,2],0],
        1 :[(55,45,4, 2),[5,5],0] 
    },
    'taulell':{ 
        0 :[(25,23,4,2),[4,3],1],
        1 :[(23,25,4, 2),[6,3],0],
        2 :[(21,25,4, 2),[6,6],1]    
    },
    'pou':{}
}

# HUMAN WIN per doble [0,0]
e4={
    'maRobot':{ 
            #idFitxa : [ (x,y,amplada,alçada), [ puntsEsquerra/Dalt, puntsDreta/Baix], orientació]
            0 :[(5,5,4,2),[1,5],0],
            1 :[(5,10,4, 2),[4,3],0],
            2 :[(5,15,4, 2),[4,2],0],
            3 :[(5,220,4, 2),[2,3],0]  
    },
    'maHuma':{ 
        0 :[(55,40,4,2),[1,2],0],
        1 :[(55,45,4, 2),[0,0],0] 
    },
    'taulell':{ 
        0 :[(25,23,4,2),[4,3],1],
        1 :[(23,25,4, 2),[6,3],0],
        2 :[(21,25,4, 2),[6,6],1]    
    },
    'pou':{}
}

# ROBOT WIN per max [4,3] = 7
e5={
    'maRobot':{ 
            #idFitxa : [ (x,y,amplada,alçada), [ puntsEsquerra/Dalt, puntsDreta/Baix], orientació]
            0 :[(5,5,4,2),[1,0],0],
            1 :[(5,10,4, 2),[4,3],0],
            2 :[(5,15,4, 2),[4,2],0],
            3 :[(5,220,4, 2),[2,3],0]  
    },
    'maHuma':{ 
        0 :[(55,40,4,2),[1,2],0],
        1 :[(55,45,4, 2),[5,0],0] 
    },
    'taulell':{ 
        0 :[(25,23,4,2),[4,3],1],
        1 :[(23,25,4, 2),[6,3],0],
        2 :[(21,25,4, 2),[6,6],1]    
    },
    'pou':{}
}

# HUMAN WIN per max [6,5] = 11
e6={
    'maRobot':{ 
            #idFitxa : [ (x,y,amplada,alçada), [ puntsEsquerra/Dalt, puntsDreta/Baix], orientació]
            0 :[(5,5,4,2),[1,0],0],
            1 :[(5,10,4, 2),[4,3],0],
            2 :[(5,15,4, 2),[4,2],0],
            3 :[(5,220,4, 2),[2,3],0]  
    },
    'maHuma':{ 
        0 :[(55,40,4,2),[1,2],0],
        1 :[(55,45,4, 2),[6,5],0] 
    },
    'taulell':{ 
        0 :[(25,23,4,2),[4,3],1],
        1 :[(23,25,4, 2),[6,3],0],
        2 :[(21,25,4, 2),[6,6],1]    
    },
    'pou':{}
}

print("RETURN: ",getFirstTurn(e1))
print(" ")
print(" ")
print(" ")
print("RETURN: ",getFirstTurn(e2))
print(" ")
print(" ")
print(" ")
print("RETURN: ",getFirstTurn(e3))
print(" ")
print(" ")
print(" ")
print("RETURN: ",getFirstTurn(e4))
print(" ")
print(" ")
print(" ")
print("RETURN: ",getFirstTurn(e5))
print(" ")
print(" ")
print(" ")
print("RETURN: ",getFirstTurn(e6))

