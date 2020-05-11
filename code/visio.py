# -*- coding: utf-8 -*-
'''
Computa els canvis registrats en el taulell de joc i ho passa al Mòdul Control.
'''
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import time
import math

class Visio():    
    def __init__(self):
        self.originalBackground = None
        self.background = None        
        self.frame = None
        self.grayFrame = None
        self.rotatedFrame = None
        
        self.patroH = None
        self.patroV = None
        self.midaFitxa = [0,0] # p.e.: Fitxa Vertical [amplada, alcada]
        self.rotacioDefecte = 0.0
        
        self.empty = True
        
        self.estatPartida = None
        
    ###################################################################
    def rotate_frame(self):
        (h,w) = self.grayFrame.shape[:2]
        (cX,cY) = (w//2,h//2)
        
        M = cv.getRotationMatrix2D((cX,cY),self.rotacioDefecte,1.0)
        cos = np.abs(M[0,0])
        sin = np.abs(M[0,1])
        
        nW = int((h*sin)+(w*cos))
        nH = int((h*cos)+(w*sin))
        
        M[0,2] += (nW/2)-cX
        M[1,2] += (nH/2)-cY
        
        return cv.warpAffine(self.grayFrame,M,(nW,nH))
    ###################################################################
    def rotate_point(self,pt):
        angle = (self.rotacioDefecte*math.pi)/180
        ox = self.rotatedFrame.shape[1]/2
        oy = self.rotatedFrame.shape[0]/2
        px, py = pt
        x = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        y = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)   
        x = int(x-((self.rotatedFrame.shape[1]-self.grayFrame.shape[1])/2))
        y = int(y-((self.rotatedFrame.shape[0]-self.grayFrame.shape[0])/2))
        
        return (x,y)
    ###################################################################
    def updateFrame(self,frame):
        self.frame = frame
        self.grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        self.backgroundSubstraction()
        if self.empty:
            self.getFirstFeatures()
        if self.rotacioDefecte == 0.0:
            self.rotatedFrame = self.grayFrame
        else:
            self.rotatedFrame = self.rotate_frame()
        
    
    ##### backgroundSubstraction #####
    def backgroundSubstraction(self, debug=False):
        if self.originalBackground is None:
            self.originalBackground = self.grayFrame
            self.background = self.grayFrame
        else:
            self.background = cv.absdiff(self.grayFrame,self.originalBackground)
            
        if debug:
            cv.imshow("Debug visio: backgroundSubstraction",self.background)
    
    ###################################################################
    def mostrarResultat(self, debug = False):
        im = self.frame
        for d in self.estatPartida:
            if debug:
                print(d,':',self.estatPartida[d])
            punts = self.estatPartida[d][1]
            x,y,w,h = self.estatPartida[d][0]
            orientacio = self.estatPartida[d][2]
            margin=20
            if orientacio == 0:
                x1=x-margin
                y1=y+int(h/2)
                x2=x+w
                y2=y+int(h/2)
                im =cv.putText(im,str(punts[0]),(x1,y1), cv.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv.LINE_AA)
                im =cv.putText(im,str(punts[1]),(x2,y2), cv.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv.LINE_AA)
            else:
                x1=x+int(w/2)
                y1=y
                x2=x+int(w/2)
                y2=y+h+margin
                im =cv.putText(im,str(punts[0]),(x1,y1), cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)
                im =cv.putText(im,str(punts[1]),(x2,y2), cv.FONT_HERSHEY_SIMPLEX, 1,(255,0,0),2,cv.LINE_AA)            
            if debug:
                im =cv.putText(im,str(d),(x+int(w/2),(y+int(h/2))), cv.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv.LINE_AA)
        im.astype('uint8')
        return im
        
        
    ##### processarFrame #####
    def processarFrame(self, debug=False):
        # Aplicar threshold
        #_,threshold = cv.threshold(self.grayFrame,127,255,cv.THRESH_BINARY)
        _,threshold = cv.threshold(self.frame,127,255,cv.THRESH_BINARY)
        # Aplicar filtre Gaussia
        threshold = cv.GaussianBlur(threshold,(5,5),0)
        
        # Creem imatge 2D per trobar contorns
        contorns = threshold[:,:,0]
        #Trobem els contorns presents en la imatge
        contours, hierarchy = cv.findContours(contorns,cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        dictContorns = {}
        
        '''
        contarPunts(hierarchy)
        '''
        # Per cada contorn c
        for i,c in enumerate(contours):
            pare = hierarchy[0][i,3]
            # Si el contorn actual esta dins d'algun altre (es un punt)
            if pare != -1:
                # registrem les dades de la fitxa a la que pertany el punt a la variable cos
                # cos -> (x,y,width,height)
                cos = cv.boundingRect(contours[pare])
                # registrem les dades del punt actual
                x,y,w,h = cv.boundingRect(contours[i])
                punts=[0,0]
                orientacio=0
                #Comprovem l'orientacio de la fitxa i assignem el punt a un dels costats
                if cos[2] > cos[3]:
                    # Horitzontal
                    orientacio=0
                    if x < cos[0]+int(cos[2]/2):
                        punts=[1,0] # Esquerra
                    else:
                        punts=[0,1] # Dreta
                elif cos[2] < cos[3]:
                    # Vertical
                    orientacio=1
                    if y < cos[1]+int(cos[3]/2):
                        punts=[1,0] # Superior
                    else:
                        punts=[0,1] # Inferior
                else:
                    print('Error!')
                    pass          

                # Si la fitxa no existeix en el diccionari, la afegim amb totes les dades que hem recollit
                if not str(pare) in dictContorns:
                    dictContorns[str(pare)]=[cos,punts,orientacio]
                # Si la fitxa si existeix, modifiquem el camp punts afegint el punt trobat al canto corresponent
                else:               
                    dictContorns[str(pare)][1][0]+=punts[0]
                    dictContorns[str(pare)][1][1]+=punts[1]           
    
        if debug:
            cv.imshow("Debug visio: processarFrame",self.background)
        self.estatPartida = dictContorns
        return dictContorns
    
    
    
    def getFirstFeatures(self, debug = False):
        
        im = self.frame.copy()
        _, threshold = cv.threshold(self.frame,127,255,cv.THRESH_BINARY)
        threshold = cv.GaussianBlur(threshold,(5,5),0)
        
        contorns = threshold[:,:,0]
        contours, hierarchy = cv.findContours(contorns,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        
        
        posicio = (0,0)
        rotacio = 0.0
        midaFitxa = (0,0) #w,h
        for i,c in enumerate(contours):  
            if hierarchy[0][i,3]==-1:
                # Calculem els vertex maxim i minim i la rotacio del contorn            
                rect = cv.minAreaRect(contours[i])  
                # rect -> (center (x,y), (width, height), angle of rotation )
                # Definim la posicio de la fitxa
                posicio = rect[0]
                # Definim la mida de la fitxa
                midaFitxa = rect[1]
                self.midaFitxa = midaFitxa
                # Definim la rotacio alpha de la fitxa
                rotacio = rect[2]
                self.empty = False
                break
                
        if not self.empty:
            #self.estatPartida={'maRobot':{},'maHuma':{},'taulell':{},'pou':{}}
            self.patroH = None
            # Trobar una plantilla del centre de una fitxa per trobar les demes
            rows,cols,_ = im.shape

            x = int(posicio[0])
            y = int(posicio[1])


            width = int(midaFitxa[0])
            height = int(midaFitxa[1])

            centerX = int(cols/2)
            centerY = int(rows/2)

            h_gap = centerX - x
            v_gap = centerY - y
            dst = self.grayFrame.copy()
            # Traslacio al centre
            M = np.float32([[1,0,h_gap],[0,1,v_gap]])
            dst = cv.warpAffine(dst,M,(cols,rows))
            
            # Rotacio
            if width > height: # Horitzontal
                rotacioOrigen = 90+rotacio
            else: # Vertical
                rotacioOrigen= rotacio
                temp = width
                width = height
                height = temp
            self.midaFitxa = [min(width, height),max(width, height)]
            self.rotacioDefecte = rotacioOrigen
            M = cv.getRotationMatrix2D((cols/2,rows/2),rotacioOrigen,1)
            dst = cv.warpAffine(dst,M,(cols,rows))

            # ROI
            templateHeight = height*0.2
            templateWidth = width*0.5
            self.patroH  = dst[ centerY-int(templateHeight*0.5):centerY+int(templateHeight*0.5) , centerX-int(templateWidth*0.5) : centerX+int(templateWidth*0.5)]
            self.patroV = self.patroH.transpose()
            if debug :
                plt.figure()
                plt.imshow(self.patroH)
                print('Amplada: {}, Alcada: {}, Rotacio: {}'.format(midaFitxa[0],midaFitxa[1],rotacio))
                
        return (posicio,self.midaFitxa,self.rotacioDefecte),self.patroH  
    
    
    
    def contarPunts(self,roi):
        dst = np.zeros((roi.shape[0],roi.shape[1],3),dtype=np.uint8)
        dst[:,:,0] = roi[:,:]
        dst[:,:,1] = roi[:,:]
        dst[:,:,2] = roi[:,:]
        dst = cv.GaussianBlur(dst,(5,5),0)
        _,threshold = cv.threshold(dst,127,255,cv.THRESH_BINARY)    
        contours, hierarchy = cv.findContours(threshold[:,:,0],cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        punts = 0

        dst = cv.drawContours(dst,contours,-1,(255,127,0),1)
        #plt.figure()
        #plt.imshow(dst,'gray')
        for i,c in enumerate(contours):
            pare = hierarchy[0][i,3]
            if pare != -1:
                punts+=1
        return punts
    
    def getTableData(self):
        if not self.empty:
            if self.patroH is None:
                self.getFirstFeatures()
                        
            # Template matching
            arrayPatrons = [self.patroV,self.patroH]
            zonaMatch = int(min(self.patroV.shape))
            self.estatPartida={'maRobot':{},'maHuma':{},'taulell':{},'pou':{}}
            # TODO: ROI per cada zona d'interes
            found=[]
            for patro in arrayPatrons:
                w,h = patro.shape[::-1]
                # Template Matching
                res = cv.matchTemplate(self.rotatedFrame,patro,cv.TM_CCOEFF_NORMED)
                thr = 0.8
                loc = np.where(res>=thr)

                for pt in zip(*loc[::-1]):
                    # Trobar coordenades sense rotar

                    if len(found)==0:
                        same=False
                    else:
                        same=False
                        for f in found:
                            if pt[0] in (np.arange(f[0]-zonaMatch, f[0]+zonaMatch)):
                                if pt[1] in (np.arange(f[1]-zonaMatch, f[1]+zonaMatch)):
                                    same=True
                                    break
                    if not same:
                        found.append(pt)
                        top_left = pt
                        bottom_right = (pt[0] + w, pt[1] + h)                
                        top_right = (bottom_right[0],top_left[1])
                        bottom_left = (top_left[0],bottom_right[1])

                        center = (int(top_left[0]+(round((top_right[0]-top_left[0])/2))) ,int(top_left[1]+(round((bottom_left[1]-top_left[1])/2))))


                        orientacio = 1 #h
                        alcada = self.midaFitxa[1]
                        amplada = self.midaFitxa[0]
                        if top_right[0]-top_left[0] < bottom_left[1]-top_left[1]:
                            orientacio=0
                            alcada = self.midaFitxa[0]
                            amplada = self.midaFitxa[1]
                        self.estatPartida['taulell'][len(self.estatPartida['taulell'])] = [(center[0],center[1],amplada,alcada),[0,0],orientacio] 
                        
            for dic in self.estatPartida['taulell']:
                #print(estatPartida['taulell'][dic])
                x,y,w,h = self.estatPartida['taulell'][dic][0]
                puntsA=0
                puntsB=0
                if self.estatPartida['taulell'][dic][2]: # Vertical
                    # ROI
                    roi = self.rotatedFrame[y-round(h/2) : y,x-round(w/2) : x+round(w/2)] # Superior
                    puntsA=self.contarPunts(roi)
                    roi = self.rotatedFrame[y : y+round(h/2),x-round(w/2) : x+round(w/2)] # Inferior
                    puntsB=self.contarPunts(roi)

                else: # Horitzontal
                    # ROI
                    roi = self.rotatedFrame[y-round(h/2) : y+round(h/2),x-round(w/2) : x] # Esquerra
                    puntsA=self.contarPunts(roi)

                    roi = self.rotatedFrame[y-round(h/2) : y+round(h/2),x : x+round(w/2)] # Dreta
                    puntsB=self.contarPunts(roi)

                self.estatPartida['taulell'][dic][1]=[puntsA,puntsB]
                rotatedCenter = self.rotate_point((self.estatPartida['taulell'][dic][0][0],self.estatPartida['taulell'][dic][0][1]))
                self.estatPartida['taulell'][dic][0]=(rotatedCenter[0],rotatedCenter[1],self.estatPartida['taulell'][dic][0][2],self.estatPartida['taulell'][dic][0][3])
                
        else:
            self.estatPartida = None
        return self.estatPartida