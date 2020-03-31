# R2-MINO

![alt text](https://raw.githubusercontent.com/XCoret/R2-MINO/master/docs/icona.png)


Adaptació d’un robot Scara per a jugar partides
de dòmino de forma intel·ligent contra
oponents humans.

## Components del grup
Xavi Coret - 1423586
Marian Cabrera - 1392634
Martí Tuneu - 1425069
Marc Callado - 1392623

## Descripció del projecte

L’objectiu del projecte és construir un robot de tipus SCARA amb la implementació
de la funcionalitat per jugar partides de domino contra oponents humans. El robot
disposarà d’una càmera enfocada cap al taulell on es juga la partida i anirà
enregistrant i processant tots els moviments que es vagin produint. Quan sigui el
torn del robot, amb les normes del dòmino i l’estat actual de la partida obtingut a
partir de la càmera, aquest seleccionarà la següent jugada a fer i farà el càlcul de les
cinemàtiques per dur-la a terme.

## Arquitectura del Software

**Control:** Mòdul encarregat d’organitzar l’execució dels demés mòduls a partir de la informació que aquests li proporcionin. Les seves tasques seran:    
    - Formar un estat de partida a partir de la informació de la càmera rebuda del mòdul Visió. (Processament d’imatges a dades).
    - Informar al mòdul jugabilitat de l’estat de la partida perquè aquest respongui amb una jugada.
    - Proporcionar al mòdul Moviment les coordenades inicials i finals de la posició de la fitxa a moure.
**Jugabilitat:** S’encarrega de definir la jugada a realitzar a partir de l’estat de la partida que rep del mòdul Control i també del nivell de dificultat seleccionat.
**Visió:** Computa els canvis registrats en el taulell de joc i ho passa al Mòdul Control
**Moviment:** A partir de les coordenades inicials i finals de posició de la fitxa a moure, rebuda del mòdul Control, calcular el moviment del braç i executar-lo.
