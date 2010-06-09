import pygame
from fortuneengine.GameEngineElement import GameEngineElement
class TermBox(GameEngineElement):
    def __init__(self, x,y,width,height,lines):
        GameEngineElement.__init__(self, has_draw=True, has_event=False)

        self.max_lines = lines
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 32)
        self.__lines = []

        self.add_to_engine()

    def add_line(self, line):
        self.__lines.append( line )
        if len( self.__lines ) > self.max_lines:
            self.__lines.pop(0)

    def draw(self, screen):
        pygame.draw.rect(screen, [0, 0, 0], (self.x, self.y, self.width, self.height))
        i=0
        for line in self.__lines:
            ren = self.font.render(line, 1, [255, 255, 255])
            screen.blit(ren, (self.x, self.y + i*self.font.get_height()))
            i+=1
