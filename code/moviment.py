# -*- coding: utf-8 -*-
'''
A partir de les coordenades inicials i finals de posició de la fitxa a moure, 
rebuda del mòdul Control, calcular el moviment del braç i executar-lo.
'''
print('Modul Moviment Carregat!')
import math

class C:
    PI = 3.14159
    ARM_1 = 27.5
    ARM_2 = 27.5
    OPEN_DEGREES = 0
    CLOSE_DEGREES = 45
    IDLE_X = 180
    IDLE_Y = 90
    LIFT_VALUE= 360
    IDLE_TOOL = 180    

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
        print ("ANGULO 1: " + str(round(angulo1,2)))
        print ("ANGULO 2: " + str(round(angulo2,2)))
        return [round(angulo1,2), round(angulo2,2)]

    ''' Actual funcitons that would had moved the servos instead of returning values for the demo '''
    def operateToolOpen(self, isOpen):
        if(isOpen):
            return self.OPEN_DEGREES
        else:
            return self.CLOSE_DEGREES

    def operateToolRotate(self, direction, angulo1, angulo2, angulo3):
        baseX = self.ARM_1 * math.cos(math.radians(angulo1))
        baseY = self.ARM_1 * math.sin(math.radians(angulo2+180))

        toolX = self.ARM_2 * math.cos(math.radians(angulo1 + angulo2 + 180))  + baseX
        toolY = self.ARM_2 * math.sin(math.radians(angulo1 + angulo2 + 360)) + baseY

        x = round(toolX) - round(baseX)
        y = round(toolY) - round(baseY)
        degree =  math.degrees(math.atan2(y, x))

        if (direction == "N"):
            return (90 - angulo1 - angulo2 +180 +180) %360
        elif (direction == "S"):
            return 270 - angulo1 - angulo2
        elif (direction == "E"):
            return 0 - angulo1 - angulo2
        elif (direction == "W"):
            return 180 - angulo1 - angulo2
            
    def operateToolLift(self, isLift):
        if(isLift):
            return self.LIFT_VALUE
        else:
            return 0

    def idlePosition(self):
        return (self.IDLE_X, self.IDLE_Y)

    def moveTo(self, x_pos, y_pos):
        return calculate_movement(x_pos, y_pos)
        
    def signalPlayer(self, player):
        if (player == "h"):
            return (25, 25)
        elif (player == "r"):
            return (-25, 25)
        
''' test that will be on calcul module '''
#c = C()
#c.calculate_movement(20, 45)
