import pygame
import os

######################################################################
#Comic Class: stores an image list and possible BGM, traverses through list and tries to play BGM
######################################################################
class Comic:
    def __init__(self,Folder,BGM):
        self.currentIndex = 0
        self.images=[]
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

    def next(self,player):
        if self.currentIndex < self.size - 1:
            self.currentIndex+=1

        else:
            player.stopComic()

    def previous(self):
        if self.currentIndex > 0:
            self.currentIndex-=1

        else:
            self.currentIndex=0

    def draw(self,screen):
        screen.blit(self.images[self.currentIndex].image,(0,0,1200,900))
        pygame.display.flip()
