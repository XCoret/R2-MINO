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


# ROBOT WIN
e1={
    #21
    'maRobot':{ 
            #idFitxa : [ (x,y,amplada,alçada), [ puntsEsquerra/Dalt, puntsDreta/Baix], orientació]
            0 :[(5,5,4,2),[1,1],0],
            1 :[(5,10,4, 2),[4,4],0],
            2 :[(5,15,4, 2),[4,2],0],
            3 :[(5,220,4, 2),[2,3],0]  
    },
    #8
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

# EMPAT
e2={
    #8
    'maRobot':{ 
            #idFitxa : [ (x,y,amplada,alçada), [ puntsEsquerra/Dalt, puntsDreta/Baix], orientació]
            0 :[(5,5,4,2),[0,0],0],
            1 :[(5,10,4, 2),[4,4],0]  
    },
    #8
    'maHuma':{ 
        0 :[(55,40,4,2),[1,2],0],
        1 :[(55,45,4, 2),[5,0],0] 
    },
    'taulell':{ 
        0 :[(25,23,4, 2),[4,3],1],
        1 :[(23,25,4, 2),[6,3],0],
        2 :[(21,25,4, 2),[6,6],1]    
    },
    'pou':{}
}

# HUMAN WIN
e3={
    #8
    'maRobot':{ 
            #idFitxa : [ (x,y,amplada,alçada), [ puntsEsquerra/Dalt, puntsDreta/Baix], orientació]
            0 :[(5,5,4,2),[0,0],0],
            1 :[(5,10,4, 2),[4,4],0]  
    },
    #20
    'maHuma':{ 
        0 :[(55,40,4, 2),[1,2],0],
        1 :[(55,45,4, 2),[5,0],0],
        2 :[(21,25,4, 2),[6,6],1]
    },
    'taulell':{ 
        0 :[(25,23,4, 2),[4,3],1],
        1 :[(23,25,4, 2),[6,3],0],
        2 :[(21,25,4, 2),[6,6],1]    
    },
    'pou':{}
}

print("RETURN: ",getWinner(e1,"h"))
print(" ")
print(" ")
print(" ")
print("RETURN: ",getWinner(e2, "h"))
print(" ")
print(" ")
print(" ")
print("RETURN: ",getWinner(e2, "r"))
print(" ")
print(" ")
print(" ")
print("RETURN: ",getWinner(e3, "r"))
