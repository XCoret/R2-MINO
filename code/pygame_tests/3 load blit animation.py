import pygame,sys
from pygame.locals import *
from random import randint


pygame.init()
pWindow= pygame.display.set_mode((800,800))
pygame.display.set_caption("Hello world!")

img = pygame.image.load("C:/Users/Pipo/Pictures/st.png")
pX= 200 ##randint(10,40)
pY= 100 ##randint(10,50)

vel = 1
white =(255,255,255)
right = True

while True:
    pWindow.fill(white)
    pWindow.blit(img, (pX,pX))
    
    for pEvent in pygame.event.get():
        if pEvent.type == QUIT:
            pygame.quit()
            sys.exit()

    if right == True:
        if pX<400:
            pX+=vel
        else:
            right=False
    else:
        if pX>1:
            pX-=vel
        else:
            right=True
            
    pygame.display.update()
