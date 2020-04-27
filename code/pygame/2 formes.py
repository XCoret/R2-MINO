import pygame,sys
from pygame.locals import *

pygame.init()
pWindow= pygame.display.set_mode((400,300)) 
pygame.display.set_caption("Hello world!")

pygame.draw.line(pWindow, lC , (60,80), (160,100))
pygame.draw.circle(pWindow, (8,70,120),(80,90), 20)
pygame.draw.rect(pWindow,(130,70,70),(10,10, 100,50))
pygame.draw.polygon(pWindow, (90,180,70), ((140,0),(290,106),(40,80)))

while True:
     
    for pEvent in pygame.event.get():
        if pEvent.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
