import numpy as np
import math
import cv2 as cv
from matplotlib import pyplot as plt

class ModulVisio():
    ###############################################################################################
    def __init__(self, debug = False):
        self.debug = debug
        
        # mides en cm del taulell #
        self.midaTaulell =[60.0,55.0]
        self.midaMin = 10.0
        self.midaMax = 40.0      
        self.margeRobot = 5.0
        ###########################
        
        self.empty = True
        self.originalBackground = None
        self.fitxaFrame = None
        self.frame = None
        self.grayFrame = None
        self.rotatedFrame = None
        
        self.patroH = None
        self.patroV = None
        
        self.midaFitxa = [0,0]
        self.rotacioDefecte = 0.0
        
        self.estatPartida = None
        
        self.extrems=[]
    ###############################################################################################
    
    def updateFrame(self,frame,debug=None):
        if debug is not None:
            self.debug = debug
        self.frame = frame
        self.grayFrame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        if self.originalBackground is None:
            self.originalBackground = self.grayFrame
        else:
            self.fitxaFrame = cv.absdiff(self.grayFrame,self.originalBackground)
            self.fitxaFrame[self.fitxaFrame<127]=0
            self.fitxaFrame[self.fitxaFrame!=0]=255
            if self.empty:
                self.getFirstFeatures()
            self.rotatedFrame = self.rotate_frame(self.fitxaFrame)
            
            self.getTableData()
        
        if self.debug:
            print('[Visio: updateFrame()]')
            fig, ax = plt.subplots(nrows=3, ncols=3);
            ax[0,0].remove()
            ax[0,1].imshow(self.frame)
            ax[0,1].set_title('Original frame')
            ax[0,2].remove()
            ax[1,0].imshow(self.grayFrame,'gray')
            ax[1,0].set_title('grayFrame')
            ax[1,1].imshow(self.originalBackground,'gray')
            ax[1,1].set_title('background')
            ax[1,2].imshow(self.fitxaFrame,'gray')
            ax[1,2].set_title('fitxaFrame')
            ax[2,0].remove()
            ax[2,1].imshow(self.rotatedFrame,'gray')
            ax[2,1].set_title('rotatedFrame')
            ax[2,2].remove()
            plt.show()     
            
    ###############################################################################################
    def contarPou(self):
        fitxaFrame = cv.absdiff(self.grayFrame,self.originalBackground)
        midaMin = int((self.midaMin*self.frame.shape[1])/self.midaTaulell[0])
        midaMax = int((self.midaMax*self.frame.shape[0])/self.midaTaulell[1])
        
        pou = fitxaFrame[0:midaMin,midaMin:midaMin+midaMax]
        threshold = cv.GaussianBlur(pou,(5,5),0)
        contours,hierarchy = cv.findContours(threshold,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)   
        zona='pou'
        orientacio = 0
        for i,c in enumerate(contours):
            if hierarchy[0][i,3]==-1:
                rect = cv.minAreaRect(contours[i])
                
                x,y = self.robot_coords(rect[0])
                w = (rect[1][1]*self.frame.shape[1])/self.midaTaulell[0]
                h = (rect[1][0]*self.frame.shape[1])/self.midaTaulell[0]
                
                
                if w>h:
                    orientacio = 0
                else:
                    orientacio = 1
                
                self.estatPartida[zona][len(self.estatPartida[zona])]=[(x,y,w,h),[0,0],orientacio]
                
      
                    
    ###############################################################################################
    
    def getFirstFeatures(self):
        threshold = cv.GaussianBlur(self.fitxaFrame,(5,5),0)
        contours,hierarchy = cv.findContours(threshold,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)   
        
        max_w = 0
        max_h = 0
        
        for i,c in enumerate(contours):
            if hierarchy[0][i,3]==-1:
                rect = cv.minAreaRect(contours[i])
                if(rect[1][0]>=max_w and rect[1][1]>=max_h):
                    max_w = rect[1][0]
                    max_h = rect[1][1]
                    
                    posicio = rect[0]
                    midaFitxa = rect[1]
                    rotacio = rect[2]

            self.empty = False
                
        if not self.empty:
            rows,cols,_ = self.frame.shape
            
            x = int(posicio[0])
            y = int(posicio[1])
            
            width = int(midaFitxa[0])
            height = int(midaFitxa[1])
            
            centerX = int(cols/2)
            centerY = int(rows/2)
            
            h_gap = centerX - x
            v_gap = centerY - y
            
            # Traslacio
            dst = self.fitxaFrame.copy()
            M = np.float32([[1,0,h_gap],[0,1,v_gap]])
            dst = cv.warpAffine(dst,M,(cols,rows))
            
            # Rotacio
            if width > height: # Horitzontal
                rotacio +=90
            else:
                width, height = height,width
            
            M = cv.getRotationMatrix2D((cols/2,rows/2),rotacio,1.0)
            dst = cv.warpAffine(dst,M,(cols,rows))
            
            self.rotatedFrame = dst
            
            # Definicio patron    
            templateHeight = height * 0.2
            templateWidth = width * 0.5
            
            self.patroH = dst[centerY-int(templateHeight*0.5):centerY+int(templateHeight*0.5), centerX-int(templateWidth*0.5):centerX+int(templateWidth*0.5)]
            self.patroV = self.patroH.transpose()
            self.midaFitxa = [min(width, height),max(width, height)]
            self.rotacioDefecte = rotacio                
        
        if self.debug:
            print('[Visio: getFirstFeatures()]')
            print('Empty:{}; Posicio:{}; mida:{}; rotacio:{};'.format(self.empty,posicio, self.midaFitxa,self.rotacioDefecte))
            fig, ax = plt.subplots(nrows=2, ncols=3);
            ax[0,0].remove()
            ax[0,1].imshow(self.frame)
            ax[0,1].set_title('Original frame')
            ax[0,2].remove()
            ax[1,0].imshow(self.rotatedFrame,'gray')
            ax[1,0].set_title('rotatedFrame')
            ax[1,1].imshow(self.patroH,'gray')
            ax[1,1].set_title('patroH')
            ax[1,2].imshow(self.patroV,'gray')
            ax[1,2].set_title('patroV')
            plt.show()
            
    ###############################################################################################
    def rotate_frame(self, frame):
        if self.rotacioDefecte != 0.0:
            (h,w) = frame.shape[:2]
            (cX,cY) = (w//2,h//2)

            M = cv.getRotationMatrix2D((cX,cY),self.rotacioDefecte,1.0)
            cos = np.abs(M[0,0])
            sin = np.abs(M[0,1])

            nW = int((h*sin)+(w*cos))
            nH = int((h*cos)+(w*sin))

            M[0,2] += (nW/2)-cX
            M[1,2] += (nH/2)-cY

            res = cv.warpAffine(frame,M,(nW,nH))
        else:
            res = frame
        return res
    
    ###############################################################################################
    
    def contarPunts(self,roi):
        roi = cv.GaussianBlur(roi,(5,5),0)
        _,threshold = cv.threshold(roi,127,255,cv.THRESH_BINARY)
        contours, hierarchy = cv.findContours(threshold,cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        punts = 0
        for i,c in enumerate(contours):
            pare = hierarchy[0][i,3]
            if pare != -1:
                punts+=1
        
        if self.debug:
            threshold = np.zeros((threshold.shape[0],threshold.shape[1],3),dtype=np.uint8)
            threshold = cv.drawContours(threshold,contours,-1,(255,127,0),1)
            contoursRoi = np.zeros((roi.shape[0],roi.shape[1],3),dtype=np.uint8)
            contoursRoi[:,:,0] = roi
            contoursRoi[:,:,1] = roi
            contoursRoi[:,:,2] = roi
            contoursRoi = cv.drawContours(contoursRoi,contours,-1,(255,127,0),1)
            print('[Visio: contarPunts()]')
            fig, ax = plt.subplots(nrows=2, ncols=3);
            ax[0][0].imshow(self.patroV,'gray')
            ax[0][0].set_title('patroV')  
            ax[0][1].remove()
            
            ax[0][2].imshow(self.patroH,'gray')
            ax[0][2].set_title('patroH')  
            
            ax[1][0].imshow(roi,'gray')
            ax[1][0].set_title('ROI Original') 
            
            ax[1][1].imshow(contoursRoi,'gray')
            ax[1][1].set_title('Contorns ROI')            
            ax[1][2].imshow(threshold,'gray')
            ax[1][2].set_title('Contorns') 
                       
            plt.show()
        
        return punts
    
    ###############################################################################################
    def getZone(self,pt):
        #self.estatPartida = {'maRobot':{},'maHuma':{},'taulell':{},'pou':{}}
        zona = 'taulell'
        
        midaMin = (self.midaMin*self.frame.shape[1])/self.midaTaulell[0]
        midaMax = (self.midaMax*self.frame.shape[0])/self.midaTaulell[1]

        x,y = pt
    
        if x in np.arange(0,midaMin) and y in np.arange(midaMin,midaMin+midaMax):    
            zona = 'maHuma'
            
        elif x in np.arange(self.frame.shape[1]-midaMin, self.frame.shape[1]) and y in np.arange(midaMin,self.frame.shape[1]):            
            zona = 'maRobot'
#         elif x in np.arange(midaMin,self.frame.shape[1]-midaMin) and y in np.arange(0,midaMin):            
#             zona = 'pou'      
            
        elif x in np.arange(midaMin,midaMin+midaMax) and y in np.arange(midaMin,midaMin+midaMax):            
            zona = 'taulell'     
            
        return zona    
    ###############################################################################################
    
    def getTableData(self):
        arrayPatrons = [self.patroH, self.patroV]
        zonaMatch = int(min(self.patroV.shape))
        self.estatPartida = {'maRobot':{},'maHuma':{},'taulell':{},'pou':{}}
        diccionariPunts={}
        found = []
        for patro in arrayPatrons:
            w,h = patro.shape[::-1]
            # Template Matching
            res = cv.matchTemplate(self.rotatedFrame,patro,cv.TM_CCOEFF_NORMED)
            thr = 0.8
            loc = np.where(res >= thr)
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
                    diccionariPunts[len(diccionariPunts)]=[(center[0],center[1],amplada,alcada),[0,0],orientacio] 
                    #self.estatPartida['taulell'][len(self.estatPartida['taulell'])] = [(center[0],center[1],amplada,alcada),[0,0],orientacio] 
                    
        for dic in diccionariPunts:
            #print(estatPartida['taulell'][dic])
            x,y,w,h = diccionariPunts[dic][0]
            puntsA=0
            puntsB=0
            orientacio = diccionariPunts[dic][2]
            if w>h:
                oritentacio = 0
            else:
                oritentacio = 1
            if diccionariPunts[dic][2]: # Vertical
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

                
                
            diccionariPunts[dic][1]=[puntsA,puntsB]
            rotatedCenter = self.rotate_point((diccionariPunts[dic][0][0],diccionariPunts[dic][0][1]))
            x,y = self.robot_coords(rotatedCenter)
            # id: [[x,y,w,h],[puntsA,puntsB],orientacio]
            zona = self.getZone(rotatedCenter)
            w = (w*self.frame.shape[1])/self.midaTaulell[0]
            h = (h*self.frame.shape[1])/self.midaTaulell[0]
            self.estatPartida[zona][len(self.estatPartida[zona])]=[(x,y,w,h),[puntsA,puntsB],orientacio]
            
            
        self.contarPou()
        if self.debug:
            print('[Visio: getTableData()]')
            for d in self.estatPartida:
                print('{}: {}'.format(d,self.estatPartida[d]))
            
    ###############################################################################################                    
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
    ###############################################################################################
    def robot_coords(self,pt):
        # TODO 
        # midaTaulell 
        max_x=self.midaTaulell[0]
        max_y=self.midaTaulell[1]
        pt0 = pt[0]-self.grayFrame.shape[1]/2
        pt1 = (pt[1]-self.grayFrame.shape[0])
        
        x = ((pt0*max_x)/self.grayFrame.shape[1])
        y = -((pt1*max_y)/self.grayFrame.shape[0])
        return(x,y)
    
    ###############################################################################################
        

