import pygame
from fortuneengine.GameEngineElement import GameEngineElement
from fortuneengine.DrawableFontObject import DrawableFontObject
from fortuneengine.DrawableObject import DrawableObject
class TermBox(GameEngineElement):
    def __init__(self, x,y,width,height,lines):
        GameEngineElement.__init__(self, has_draw=True, has_event=False)

        self.max_lines = lines
        self.x = x
        self.y = y
        surf = pygame.Surface((int(width),int(height)))
        surf.fill([0,0,0])
        self.box = DrawableObject([surf],"")
        self.box.setPosition(int(x),int(y))
        self.font = pygame.font.Font(None, 28)
        self.__lines = []
        for i in range(lines):
            self.__lines.append(DrawableFontObject('', self.font))
        self.game_engine.get_scene().addObject(self.box)
        self.game_engine.get_scene().addObjects(self.__lines)
        self.add_to_engine()

    def add_line(self, line):
        for i in range(0, self.max_lines, 1):
            print i
            if i == self.max_lines-1:
                self.__lines[i].changeText(line, [255,255,255])
            else:
                self.__lines[i].changeText(self.__lines[i+1].getText(), [255,255,255])

    def draw(self,screen,time_delta):
        i=0
        for line in self.__lines:
            line.setPosition(int(self.x), int(self.y + i*self.font.get_height()))
            i+=1
