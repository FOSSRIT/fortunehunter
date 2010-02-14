import pygame
import os

######################################################################
#Comic Class: stores an image list and possible BGM, traverses through list and tries to play BGM
######################################################################
class Comic:
    def __init__(self,ge,Folder,BGM,endcb):
        self.currentIndex = 0
        self.images=[]
        self.endcb = endcb
        self.ge = ge
        #load images into sprites
        i=0
        for image in os.listdir(Folder):
            spt=pygame.sprite.Sprite()
            spt.image=pygame.image.load(Folder+image)
            spt.rect=pygame.Rect(0,0,1200,900)
            self.images.append(spt)
            i+=1
        self.size=i
        #try to load music
        if BGM != None:
            pygame.mixer.muxic.stop()
            pygame.mixer.music.load(SOUND_PATH+BGM)
            pygame.mixer.music.play(-1)

        self.__inEngine = False
        self.add_to_engine()

    def add_to_engine(self):
        if not self.__inEngine:
            self.__inEngine = True
            self.ge.add_draw_callback( self.draw )
            self.ge.add_event_callback( self.event_handler )

    def remove_from_engine(self):
        if self.__inEngine:
            self.__inEngine = False
            self.ge.remove_draw_callback( self.draw )
            self.ge.remove_event_callback( self.event_handler )

    def end(self):
        self.remove_from_engine()
        self.ge.remove_object("comic")
        self.endcb()

    def next(self):
        if self.currentIndex < self.size - 1:
            self.currentIndex+=1

    def previous(self):
        if self.currentIndex > 0:
            self.currentIndex-=1

    def has_next(self):
        if self.currentIndex < self.size - 1:
            return True
        else:
            return False

    def draw(self,screen):
        screen.blit(self.images[self.currentIndex].image,(0,0,1200,900))

    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            newKey=pygame.key.name(event.key)

            if newKey=='[1]' or newKey=='right':
                if self.has_next():
                    self.next()
                else:
                    self.end()

            elif newKey=='[3]' or newKey=='left':
                self.previous()
