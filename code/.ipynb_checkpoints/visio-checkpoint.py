import numpy as np
import math
import cv2 as cv
from matplotlib import pyplot as plt

class ModulVisio():
    ###############################################################################################
    def __init__(self, debug = False):
        self.debug = debug
        
        # mides del taulell en cm
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
        
        #diciconari per guardar les fitxes de la partida
        self.estatPartida = {'maRobot':{},'maHuma':{},'taulell':{},'pou':{},'extrems':[]}
        self.tempEstatPartida = None
        
        
        self.output_frame = None
        
        self.extrems=[]
        self.fitxesEnTaulell = 0
        self.eix_X=[None,None] #[minim, maxim]
        self.eix_Y=[None,None]
    ###############################################################################################
    '''
        getGameStatus() : Retorna el diccionari amb les fitxes que ha processat i la seva informacio
    '''
    def getGameStatus(self):
        return self.estatPartida
    ###############################################################################################
    '''
        updateFrame(frame) : Realitza les accions basiques de background substraction, 
                                    i crida a les funcions per processar el frame rebut
    '''    
    def updateFrame(self,frame,debug=None):
        if debug is not None:
            self.debug = debug
        self.frame = frame
        self.grayFrame = cv.cvtColor(self.frame,cv.COLOR_BGR2GRAY)
        # Guardem el fons original en cas que no en tinguem cap (taulell buit)
        if self.originalBackground is None:
            self.originalBackground = self.grayFrame
        else:
            # Realitzem un background substraction per extreure les fitxes que hi ha
            self.fitxaFrame = cv.absdiff(self.grayFrame,self.originalBackground)
            self.fitxaFrame[self.fitxaFrame<127]=0
            self.fitxaFrame[self.fitxaFrame!=0]=255
            
            # Busquem el patro del mig de una fitxa així com la rotacio (en cas que n'hi hagi)
            if self.empty:
                self.getFirstFeatures()
            # Rotem el frame amb la rotacio trobada
            self.rotatedFrame = self.rotate_frame(self.fitxaFrame)
            
            # Si ja tenim un patro enregistrat procedim a contar les fitxes
            if not self.empty:
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
    '''
        contarPou() : Realitza un recompte de les fitxes que hi ha en la zona del pou i en registra la seva informacio
                      (coordenades robot, mida en cm, punt a 0 i orientacio
                      defini els punts a [0,0] per seguir amb el mateix format de fitxa de les altre zones
    '''
    def contarPou(self):
        fitxaFrame = cv.absdiff(self.grayFrame,self.originalBackground)
        
        midaMin = int((self.midaMin*self.frame.shape[1])/self.midaTaulell[0])
        midaMax = int((self.midaMax*self.frame.shape[0])/self.midaTaulell[1])
        pou = fitxaFrame[0:midaMin,midaMin:midaMin+midaMax]
        ret,threshold = cv.threshold(pou,10,255,cv.THRESH_TOZERO)
        kernel = np.ones((5,5),np.uint8)
        opening = cv.morphologyEx(threshold, cv.MORPH_OPEN, kernel)   
        
        contours, hierarchy = cv.findContours(opening, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        
        for i,c in enumerate(contours):
            if hierarchy[0][i,3]==-1:
                rect = cv.minAreaRect(contours[i])
                x,y = self.robot_coords(rect[0])

                alcadaPixels = int((self.midaTaulell[1]*self.frame.shape[0])/self.midaTaulell[1]-5)
                w = round((rect[1][0]*self.midaTaulell[0])/self.frame.shape[1],2)
                h = round((rect[1][1]*self.midaTaulell[1])/(alcadaPixels),2)

                if h>w:
                    orientacio = 1
                else:
                    orientacio = 0

                self.estatPartida['pou'][len(self.estatPartida['pou'])]=[(round(x,3),round(y,3),w,h),[0,0],1]
           
    ###############################################################################################
    '''
        getFirstFeatures() : Busquem per el frame qualsevol contorn de fita i a partir d'aquest extraiem un patro 
                             a partir del seu centre
                             
                             
    '''
    def getFirstFeatures(self):
        
        midaMin = int((self.midaMin*self.frame.shape[1])/self.midaTaulell[0])    
        
        threshold = cv.GaussianBlur(self.fitxaFrame,(5,5),0)
        contours,hierarchy = cv.findContours(threshold,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)   
        
        max_w = 0
        max_h = 0

        for i,c in enumerate(contours):
            if hierarchy[0][i,3]==-1:
                rect = cv.minAreaRect(contours[i])
                if rect[0][1]>=midaMin and (rect[1][0]>=max_w and rect[1][1]>=max_h):     
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
            
            # Traslacio del frame per centrar la fitxa
            dst = self.fitxaFrame.copy()
            M = np.float32([[1,0,h_gap],[0,1,v_gap]])
            dst = cv.warpAffine(dst,M,(cols,rows))
            
            # Rotacio del frame per deixar la fitxa en vertical
            if width > height: # Horitzontal
                rotacio +=90
            else:
                width, height = height,width
            
            M = cv.getRotationMatrix2D((cols/2,rows/2),rotacio,1.0)
            dst = cv.warpAffine(dst,M,(cols,rows))
            
            self.rotatedFrame = dst
            
            # Definicio patro  
            
            templateHeight = height * 0.25
            templateWidth = width * 0.5
            # Retall del frame per extreure el patro
            self.patroH = dst[centerY-int(templateHeight*0.4):centerY+int(templateHeight*0.5), centerX-int(templateWidth*0.5):centerX+int(templateWidth*0.5)]
            
            # Desem el patro Vertical com a la transposicio del patro Horitzontal trobat 
            self.patroV = self.patroH.transpose()
            self.midaFitxa = [min(width, height),max(width, height)]
            # Definim la rotació per defecte que tindran les demés fitxes del taulell
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
    '''
        rotate_frame() : Donat un frame, retorna el frame rotat amb la rotació per defecte detectada                               
    '''
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
    '''
        contarPunts() : Donada una regió d'interes (mitja fitxa) conta els punts que detecta
    '''    
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
    '''
        getZone() : Donades unes coordenades retorna el nom de la zona a la que pertanyen
    '''      
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
    '''
        getTableData() : Per cada patro registrat busquem coincidencies en el frame (template matching)
                         Per cada coincidencia (fitxa) trobada, cridem a la funcio contar punts definint com a 
                         regions d'interes ROI les dues parts de cada fitxa i registrem els punts segon la zona on
                         s'hagi produit la coincidencia.
                         
                         A mes, per cada fitxa nova que es detecta, actualitzem els valors dels extrems de la partida
    '''      
    def getTableData(self):
        arrayPatrons = [self.patroH, self.patroV,np.flip(self.patroH,axis=0),np.flip(self.patroV,axis=1)]
        zonaMatch = int(min(self.patroV.shape))
        self.estatPartida = {'maRobot':{},'maHuma':{},'taulell':{},'pou':{},'extrems':[]}
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
                    

        
        for dic in diccionariPunts:
            #print(estatPartida['taulell'][dic])
            x,y,w,h = diccionariPunts[dic][0]
            puntsA=0
            puntsB=0
            orientacio = diccionariPunts[dic][2]
            if w>h:
                orientacio = 1
            else:
                orientacio = 0
            if diccionariPunts[dic][2]: # Vertical
                # ROI
                roi = self.rotatedFrame[y-round(h/2) : y,x-round(w/2) : x+round(w/2)] # Superior
                puntsB=self.contarPunts(roi)
                roi = self.rotatedFrame[y : y+round(h/2),x-round(w/2) : x+round(w/2)] # Inferior
                puntsA=self.contarPunts(roi)

            else: # Horitzontal
                # ROI
                roi = self.rotatedFrame[y-round(h/2) : y+round(h/2),x-round(w/2) : x] # Esquerra
                puntsA=self.contarPunts(roi)

                roi = self.rotatedFrame[y-round(h/2) : y+round(h/2),x : x+round(w/2)] # Dreta
                puntsB=self.contarPunts(roi)
                
                
            diccionariPunts[dic][1]=[puntsA,puntsB]
            rotatedCenter = self.rotate_point((diccionariPunts[dic][0][0],diccionariPunts[dic][0][1]))
            
            zona = self.getZone(rotatedCenter)
                
            x,y = self.robot_coords(rotatedCenter)           
           
            
            alcadaPixels = int((self.midaTaulell[1]*self.frame.shape[0])/self.midaTaulell[1]-5)
            
            w = round((w*self.midaTaulell[0])/self.frame.shape[1],2)
            h = round((h*self.midaTaulell[1])/(alcadaPixels),2)
            
            self.estatPartida[zona][len(self.estatPartida[zona])]=[(x,y,w,h),[puntsA,puntsB],orientacio]
            self.estatPartida['extrems']=None
            if zona=='taulell':
                if len(self.extrems) ==0:
                    
                    #Quan hi ha una fitxa, mirar els seus dos punts
                    puntsExtrem = puntsA
                    self.extrems.append([(x,y,w,h),[puntsA,puntsB],orientacio,puntsExtrem])
                elif len(self.extrems)==1:
                    
                    puntsExtrem = 55
                    ultimaFitxa = self.extrems[0]
                    xi = ultimaFitxa[0][0]-x
                    yi = ultimaFitxa[0][1]-y
                    dist = math.sqrt((xi)**2 + (yi)**2)                  
                   
                    if ultimaFitxa[2] == 1: #vertical
                        if x <= ultimaFitxa[0][0]-(ultimaFitxa[1][0]/2):
                            if orientacio == 0:
                                puntsExtrem = puntsA
                            else:
                                if y <= ultimaFitxa[0][1]-(ultimaFitxa[1][1]/2):
                                    puntsExtrem = puntsA
                                else:
                                    puntsExtrem = puntsB
                        else:
                            if orientacio == 0:
                                puntsExtrem = puntsB
                            else:
                                if y <= ultimaFitxa[0][1]-(ultimaFitxa[1][1]/2):
                                    puntsExtrem = puntsB
                                else:
                                    puntsExtrem = puntsA
                    else:
                        if y <= ultimaFitxa[0][1] - (ultimaFitxa[1][1]/2):
                            if orientacio == 1:
                                puntsExtrem = puntsA
                            else:
                                if x <= ultimaFitxa[0][0] - (ultimaFitxa[1][0]):
                                    puntsExtrem = puntsA
                                else:
                                    puntsExtrem = puntsB
                        else:
                            if x <= ultimaFitxa[0][0] - (ultimaFitxa[1][0]):
                                puntsExtrem = puntsA
                            else:
                                puntsExtrem = puntsB
        
                    
                    self.extrems.append([(x,y,w,h),[puntsA,puntsB],orientacio,puntsExtrem])
                    
                else:
                    trobada = False
                    for f in self.tempEstatPartida[zona]:
                        fitxa = self.tempEstatPartida[zona][f]                        
                        if puntsA == fitxa[1][0] and puntsB == fitxa[1][1]:
                            trobada = True
                            break
                            
                    if not trobada:

                        
                        f1 = self.extrems[0]
                        f2 = self.extrems[1]
                        
                        xi = f1[0][0]-x
                        yi = f1[0][1]-y
                        
                        xj = f2[0][0]-x
                        yj = f2[0][1]-y
                        
                        dist1 = math.sqrt( (xi)**2 + (yi)**2 )
                        dist2 = math.sqrt( (xj)**2 + (yj)**2 )
                        
                        indexFitxa = 0
                        puntsExtrem = 0
                        ultimaFitxa = None
                        distancia =0.0
                        
                       
                        if(dist1<=dist2):
                            indexFitxa = 0
                            ultimaFitxa = self.extrems[0]
                            distancia = dist1
                            
                        elif(dist1>dist2):
                            indexFitxa = 1
                            ultimaFitxa = self.extrems[1]
                            distancia = dist2
                        
                        
                        if ultimaFitxa[2] == 1: #vertical
                            if x <= ultimaFitxa[0][0]-(ultimaFitxa[1][0]/2):
                                if orientacio == 0:
                                    puntsExtrem = puntsA
                                else:
                                    if y <= ultimaFitxa[0][1]-(ultimaFitxa[1][1]/2):
                                        puntsExtrem = puntsA
                                    else:
                                        puntsExtrem = puntsB
                            else:
                                if orientacio == 0:
                                    puntsExtrem = puntsB
                                else:
                                    if y <= ultimaFitxa[0][1]-(ultimaFitxa[1][1]/2):
                                        puntsExtrem = puntsA
                                    else:
                                        puntsExtrem = puntsB
                        else:
                            if x <= ultimaFitxa[0][0]-(ultimaFitxa[1][0]/2):
                                if orientacio == 0:
                                    puntsExtrem = puntsA
                                else:
                                    if y <= ultimaFitxa[0][1]-(ultimaFitxa[1][1]/2):
                                        puntsExtrem = puntsA
                                    else:
                                        puntsExtrem = puntsB
                            else:
                                if orientacio == 0:
                                    puntsExtrem = puntsB
                                else:
                                    if y <= ultimaFitxa[0][1]-(ultimaFitxa[1][1]/2):
                                        puntsExtrem = puntsB
                                    else:
                                        puntsExtrem = puntsA
                                
   
                        self.extrems[indexFitxa]=[(x,y,w,h),[puntsA,puntsB],orientacio,puntsExtrem]
        
        self.tempEstatPartida = self.estatPartida.copy()  
        self.estatPartida['extrems']=self.extrems
        self.contarPou()
        if self.debug:
            print('[Visio: getTableData()]')
            for d in self.estatPartida:
                print('{}: {}'.format(d,self.estatPartida[d]))
            
    ###############################################################################################    
    '''
        rotate_point(pt) : Donada una coordenada, retorna la seva correspondencia amb la rotacio registrada
    '''
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
    '''
        robot_coords(pt) : Donada una coordenada, retorna la seva correspondencia en coordenades robot, on l'origen 
                           esta desplaçat al centre inferior del frame. Retorna les coordenades en centimetres
    '''
    def robot_coords(self,pt):
        max_x=self.midaTaulell[0]
        max_y=self.midaTaulell[1]
        pt0 = pt[0]-self.grayFrame.shape[1]/2
        pt1 = (pt[1]-self.grayFrame.shape[0])
        
        x = ((pt0*max_x)/self.grayFrame.shape[1])
        y = -((pt1*max_y)/self.grayFrame.shape[0])
        return(x,y)
    
    ###############################################################################################
    '''
        centered_coords(pt) : Donada una coordenada robot, retorna la seva correspondencia amb l'origen al centre del frame.
    '''    
    def centered_coords(self,pt):
        x,y = pt
        x = int((x*self.frame.shape[1])/self.midaTaulell[0]) +(self.grayFrame.shape[1]/2)
        y = -int((y*self.frame.shape[0])/self.midaTaulell[1]) +(self.grayFrame.shape[0])
        
        return(int(x),int(y))

    
    ###############################################################################################
    '''
        get_output_frame() : Crea una imatge amb la informacio de la partida i la retorna. 
    '''
    def get_output_frame(self):
        self.output_frame = self.frame.copy()
        font = cv.FONT_HERSHEY_PLAIN   
        fontScale = 1
        thickness = 1
        for zona in self.estatPartida:
            if zona != 'extrems' and zona!='pou':                    
                for index in self.estatPartida[zona]:
                    fitxa = self.estatPartida[zona][index]
                    x,y,w,h = fitxa[0]
                    punts = fitxa[1]
                    orientacio = fitxa[2]
                    (x2,y2) = self.centered_coords((x,y))

                    if orientacio == 1:
                        ori = 'V'
                    else:
                        ori = 'H'
                    color = (255, 0, 0)
                    
                    self.output_frame = cv.putText(self.output_frame, '[{}:{}] {}'.format(punts[0],punts[1],ori), (x2+30,y2), font, fontScale, color, thickness, cv.LINE_AA) 
                    self.output_frame = cv.putText(self.output_frame, '({},{})'.format(x,y), (x2+30,y2+15), font, fontScale, color, thickness, cv.LINE_AA)
        ini_x = 15
        ini_y = 15
        padding = 10
        color = (0,0,0)
        nFitxes = len(self.estatPartida['pou'])+len(self.estatPartida['maHuma'])+len(self.estatPartida['maRobot'])+len(self.estatPartida['taulell'])
        i=0
        self.output_frame = cv.putText(self.output_frame, 'Nombre de fitxes: {}'.format(nFitxes), (ini_x,ini_y+padding+(i*ini_y)), font, fontScale, color, thickness, cv.LINE_AA) 
        i+=1
        self.output_frame = cv.putText(self.output_frame, 'Pou: {}'.format(len(self.estatPartida['pou'])), (ini_x,ini_y+padding+(i*ini_y)), font, fontScale, color, thickness, cv.LINE_AA) 
        i+=1
        self.output_frame = cv.putText(self.output_frame, 'Ma Huma: {}'.format(len(self.estatPartida['maHuma'])), (ini_x,ini_y+padding+(i*ini_y)), font, fontScale, color, thickness, cv.LINE_AA) 
        i+=1
        self.output_frame = cv.putText(self.output_frame, 'Ma Robot: {}'.format(len(self.estatPartida['maRobot'])), (ini_x,ini_y+padding+(i*ini_y)), font, fontScale, color, thickness, cv.LINE_AA) 
        i+=1
        self.output_frame = cv.putText(self.output_frame, 'Taulell: {}'.format(len(self.estatPartida['taulell'])), (ini_x,ini_y+padding+(i*ini_y)), font, fontScale, color, thickness, cv.LINE_AA) 
        
        i+=2
        if(len(self.estatPartida['extrems'])>1):
            self.output_frame = cv.putText(self.output_frame, 'Punts extrems: {} i {}'.format(self.estatPartida['extrems'][0][3],self.estatPartida['extrems'][1][3]), (ini_x,ini_y+padding+(i*ini_y)), font, fontScale, color, thickness, cv.LINE_AA) 
        elif (len(self.estatPartida['extrems'])>0):
            self.output_frame = cv.putText(self.output_frame, 'Punts extrems: {} i {}'.format(self.estatPartida['extrems'][0][1][0],self.estatPartida['extrems'][0][1][1]), (ini_x,ini_y+padding+(i*ini_y)), font, fontScale, color, thickness, cv.LINE_AA) 
        return self.output_frame
        

