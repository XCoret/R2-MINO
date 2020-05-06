##def aux():
##    global isGame
##    isGame = True
##    
##if __name__ == '__main__':
##    isGame = False
##    print (isGame)
##    aux()
##    print (isGame)


class test:
    isGame2 = None

    def __init__(self):
        print ("Constructor")
        self.isGame2 = True

    def aux2(self):
        self.isGame2 = False

    if __name__ == '__main__':
        print (isGame2)
        aux2(self)
        print (isGame2)

test()
    
