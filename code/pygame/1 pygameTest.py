import pygame,sys
from pygame.locals import *

windowColor = pygame.Color(70,80,150)

pygame.init()
pWindow= pygame.display.set_mode((400,300))
pWindow.fill(windowColor)  
pygame.display.set_caption("Hello world!")
lC = pygame.Color(0,0,250)
pygame.draw.line(pWindow, lC , (60,80), (160,100))

while True:
     
    for pEvent in pygame.event.get():
        if pEvent.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
