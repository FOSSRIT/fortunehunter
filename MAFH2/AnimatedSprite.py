import pygame

class Spritesheet:
    """
    Class from http://www.scriptedfun.com/transcript-2-using-sprite-sheets-and-drawing-the-background/

    This class can be used to seporate images from the sprite sheet
    """
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def imgat(self, rect, colorkey = None):
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def imgsat(self, rects, colorkey = None):
        imgs = []
        for rect in rects:
            imgs.append(self.imgat(rect, colorkey))
        return imgs

    def img_extract( self, cols, rows, width, height ):
        rect_list = []
        for y in range(0, rows):
            for x in range(0, cols):
                rect_list.append( (width*x, height*y, width, height) )
        return self.imgsat( rect_list, -1 )


class AnimatedSprite(pygame.sprite.Sprite):
    """
    http://shinylittlething.com/2009/07/21/pygame-and-animated-sprites/
    """

    def __init__(self, images, fps = 10):
        pygame.sprite.Sprite.__init__(self)
        self._images = images

        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_update = 0
        self._frame = 0

        # Call update to set our first image.
        self.update(pygame.time.get_ticks())

    def update(self, t):
        # Note that this doesn't work if it's been more that self._delay
        # time between calls to update(); we only update the image once
        # then, but it really should be updated twice.

        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self._images): self._frame = 0
            self.image = self._images[self._frame]
            self._last_update = t
