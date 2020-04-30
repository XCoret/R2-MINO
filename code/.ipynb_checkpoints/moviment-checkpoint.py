# -*- coding: utf-8 -*-
'''
A partir de les coordenades inicials i finals de posició de la fitxa a moure, 
rebuda del mòdul Control, calcular el moviment del braç i executar-lo.
'''
print('Modul Moviment Carregat!')
import math

class C:
    PI = 3.14159
    ARM_1 = 4;
    ARM_2 = 2

    pos = 0

    def __init__(self):
        print ("Constructor")

    def distance(self, x_pos, y_pos):
        return math.sqrt(x_pos*x_pos + y_pos*y_pos)

    def cos_law(self, A, B, C): 
      div = (A*A + B*B - C*C) / (2*A*B)
      if (div < -1.0):
          div = -1.0
      if(div > 1.0):
          div = 1.0
      return math.acos(div)

    def rad_2_grad(self, rad):
        return rad * 180.0 / self.PI

        
    def calculate_movement(self, x_pos, y_pos):
        dist = self.distance(x_pos, y_pos)
        D1 = math.atan2(y_pos, x_pos)
        D2 = self.cos_law(dist, self.ARM_1, self.ARM_2)
        a1Radianes = D1 + D2
        a2Radianes = self.cos_law(self.ARM_1, self.ARM_2, dist)
        angulo1 = self.rad_2_grad(a1Radianes)
        angulo2 = self.rad_2_grad(a2Radianes)
        print ("ANGULO 1: " + str(angulo1))
        print ("ANGULO 2: " + str(angulo2))

c = C()
c.calculate_movement(3, 4)