# -*- coding: utf-8 -*-
'''
Mòdul encarregat d’organitzar l’execució dels demés mòduls 
a partir de la informació que aquests li proporcionin. 
Les seves tasques seran:

-Formar un estat de partida a partir de la informació de la càmera rebuda del mòdul Visió. 
(Processament d’imatges a dades).

-Informar al mòdul jugabilitat de l’estat de la partida perquè aquest respongui amb una jugada.

-Proporcionar al mòdul Moviment les coordenades inicials i finals de la posició de la fitxa a moure.
'''
import domino as d
import visio as v
import moviment as m

if __name__ == '__main__':
    print('Modul Control Excecutant')
    #d.func()
    #v.llegirImatge('src/domino.jpg')
    #print(m.getMovementTo(4,4,4))
    isGame = false
    isSetup = false
    isWon = false
    firstTurn = null
    secondTrun = null

    while(!isWon):
        #Les 28 peces estan al pou
        if(isSetup):
            #Cadascú agafa 7 peces per torns

            #Robot senyala el que té el doble mès gran per començar

            #S'asginen les variables de torns segons qui té el numero més gran 
            firstTurn = d.playerAlgorithm("h") #huma
            secondTrun = d.playerAlgorithm("r") #robot

            #isSetup a false
            #isGame a true

        #Comença la partdia
        while(isGame):
            #Apartr el braç per llegir taulell
            
            token = firstTurn.playTurn()

            if(token != false):
                #col·locarla amb sentit

            #Apartr el braç per llegir taulell si torn humà

            #Esperar final de torn per nova fitxa o pasar

            #Lectura de taulell

            #Li queden fitxes?

            #Comprovar si s'ha acabat, posar isGame i isWon a false i recompte de punts si taulell mort
            
            secondTrun.playTurn()
            
            #Apartr el braç per llegir taulell si torn humà

            #Esperar final de torn per nova fitxa o pasar

            #Lectura de taulell

            #Li queden fitxes?

            #Comprovar si s'ha acabat, posar isGame i isWon a false i recompte de punts si taulell mort
            
        #Rutina de senyalar el guanyador i final

#Mètode que crida visió per iniciar el setup
def setSetup(self, changeSetup):
    isSetup = changeStart
