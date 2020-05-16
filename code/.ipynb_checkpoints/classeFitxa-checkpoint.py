class Fitxa(pygame.sprite.Sprite):
    def __init__(self,src,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.scale = (20,40)
        self.src = 'src/fitxes/fitxa_{}.png'.format(src)
        self.scale = scale
        self.original_frame = pygame.image.load(self.src)
        self.image = self.original_frame.copy().convert_alpha()
        #self.image.fill((255,127,0))
        self.image = pygame.transform.scale(self.image,self.scale)
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width/2,self.rect.height/2)
        self.rect.x = x
        self.rect.y = y
        
        # Propietats fitxa dins el joc
        self.drag = False
        self.placed=False
        self.angle = 0.0
        self.perpendicular = False
        self.rotate(45)
        
    def __str__(self):
        ret = str("{} :: {} ::{}".format(self.rect.center,self.drag,self.placed))
        return ret
    
    
    def hovered(self,x,y):
        if x in range(self.rect.left, self.rect.right) and y in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False
    def moveTo(self,x,y):
        self.rect.center = (x,y)
        
    def rotate(self, angle):
        self.angle = (self.angle+angle)%360
        old_center = self.rect.center
        self.image = self.original_frame.copy().convert_alpha()
        
        self.image = pygame.transform.scale(self.image,self.scale)
        self.image = pygame.transform.rotate(self.image,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
        
# En el pygame heu de crear fora del bucle del joc un grup de fitxes
fitxes = pygame.sprite.Group()
# i despres crear-ne una i afegir-la
#src=id que correspon el numero de imatge de la fitxa a la carpeta (src/fitxes/)
# x,y = posicio en pixels
#scale = escala de la fitxa (en vertical)->(amplada,alcada)
fitxes.add( Fitxa(src,x,y,scale) 
# recordeu actualitzar el grup i pintar les fitxes a cada iteracio del bucle
fitxes.update()
fitxes.draw(pWindow)
