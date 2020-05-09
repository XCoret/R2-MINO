import pygame,sys
from pygame.locals import *

## COLORS ##
white =(255,255,255)
black=(0,0,0)

## WINDOW ##
heightW = 800
widthW = 800

pygame.init()
pWindow= pygame.display.set_mode((widthW,heightW), pygame.RESIZABLE)
pygame.display.set_caption("R2-MINO")

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

def do(gameDictionary):
    robotHand = gameDictionary["maRobot"]
    board = gameDictionary["taulell"]
    well = gameDictionary["pou"]

    tokensInBoard = len(board)

    for key in board:
        token = board[key]
        tokenPosition = token[0]
        tokenX = tokenPosition[0]
        tokenY = tokenPosition[1]
        pygame.draw.circle(pWindow, black, (tokenX, tokenY), 1)








pWindow.fill(white)
do(e1)
pygame.display.update()
