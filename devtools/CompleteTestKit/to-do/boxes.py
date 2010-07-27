import pygame

class BouncingBox(pygame.sprite.Sprite):
    def __init__(self, imagesList, initial_position):
        pygame.sprite.Sprite.__init__(self)
        self.images = imagesList
        self.listLen = len(imagesList)
        self.listPos = 0
        self.image = imagesList[self.listPos]
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.going_down = True # Start going downwards
        self.going_right = True # Start going right

    def update(self, right, bottom):
        # If we're at the top or bottom of the screen, switch directions.
        if self.rect.bottom >= bottom: self.going_down = False
        elif self.rect.top <= 0: self.going_down = True
        # If we're at the right or left of the screen, switch directions.
        if self.rect.right >= right: self.going_right = False
        elif self.rect.left <= 0: self.going_right = True
 
        # Move our position up or down by 2 pixels
        if self.going_down: self.rect.top += 2
        else: self.rect.top -= 2
        # Move our position left or right by 2 pixels
        if self.going_right: self.rect.right += 2
        else: self.rect.right -= 2

        if self.listPos < self.listLen - 1:
           self.listPos += 1
        else:
           self.listPos = 0
           
        self.image = self.images[self.listPos]
