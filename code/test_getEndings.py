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

b1 = {
    0 :[(25,23,4,2),[4,3],1],
    1 :[(23,25,4, 2),[6,3],0],
    2 :[(21,25,4, 2),[6,6],1]    
}

b2 = {
    0 :[(21,25,4, 2),[6,6],1],
    1 :[(23,25,4, 2),[6,3],0],
    2 :[(25,23,4,2),[4,3],1]   
}

b3 = {
    0:[(40,24,4, 2),[0,4],0],
    1:[(27,30,4, 2),[3,3],1],
    2:[(21,31,4, 2),[0,1],1],
    3:[(37,29,4, 2),[2,6],1],
    4:[(24,30,4, 2),[0,3],0],
    5:[(43,25,4, 2),[4,5],1],
    6:[(30,30,4, 2),[3,6],0],
    7:[(34,30,4, 2),[6,6],0],
    8:[(37,25,4, 2),[0,2],1]
}

getEndings(b3)


