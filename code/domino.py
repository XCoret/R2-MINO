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
class Fitxa:
    def __init__(self, vA,vB,orientacio):
        self.vA = vA
        self.vB = vB
        self.orientacio = orientacio

def func():
    for i in range(6):
        print(i)
    print('Domino!')