import pygame

class Spritesheet:
    """
    Class from http://www.scriptedfun.com/transcript-2-using-sprite-sheets-and-drawing-the-background/

    This class can be used to seporate images from the sprite sheet
    """
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename)#.convert()

    def imgat(self, rect):
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size)#.convert()
        image.blit(self.sheet, (0, 0), rect)
        return image

    def imgsat(self, rects):
        imgs = []
        for rect in rects:
            imgs.append(self.imgat(rect))
        return imgs

    def img_extract( self, cols, rows, width, height ):
        rect_list = []
        for y in range(0, rows):
            for x in range(0, cols):
                rect_list.append( (width*x, height*y, width, height) )
        return self.imgsat( rect_list)