import pygame

class Spritesheet:
    """
    Class from http://www.scriptedfun.com/transcript-2-using-sprite-sheets-and-drawing-the-background/

    This class can be used to seporate images from the sprite sheet
    """
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()
        self.sheet = self.imgat(self.sheet.get_rect())

    def imgat(self, rect, myColorKey = None):
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size).convert()
        if myColorKey == None: myColorKey = image.get_at((0,0))
        image.set_colorkey(myColorKey)
        image.blit(self.sheet, (0, 0), rect)
        return image

    def imgsat(self, rects, myColorKey = None):
        imgs = []
        for rect in rects:
            imgs.append(self.imgat(rect, myColorKey))
        return imgs

    def img_extract( self, cols, rows, width, height, myColorKey = None):
        rect_list = []
        for y in range(0, rows):
            for x in range(0, cols):
                rect_list.append( (width*x, height*y, width, height,) )
        return self.imgsat( rect_list, myColorKey)