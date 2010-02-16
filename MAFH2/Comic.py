import pygame
import os
from GameEngine import GameEngineElement
######################################################################
#Comic Class: stores an image list and possible BGM, traverses through list and tries to play BGM
######################################################################
class Comic(GameEngineElement):
    def __init__(self,Folder,BGM,endcb):
        GameEngineElement.__init__(self)
        self.currentIndex = 0
        self.images=[]
        self.endcb = endcb
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

        self.add_to_engine()

    def end(self):
        self.remove_from_engine()
        self.game_engine.remove_object("comic")
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
                    return True
                else:
                    self.end()
                    return True

            elif newKey=='[3]' or newKey=='left':
                self.previous()
                return True
