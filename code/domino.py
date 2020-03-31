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
print('Modul Joc Carregat!')
class Fitxa:
    def __init__(self, vA,vB,orientacio):
        self.vA = vA
        self.vB = vB
        self.orientacio = orientacio

def func():
    fitxes=[]
    for a in range(7):
        for b in range(7-a):
            fitxes.append(Fitxa(a,b,1))
        #print(a)
        
    for f in fitxes:
        print(str(f.vA)+' '+str(f.vB))
    print(len(fitxes))
