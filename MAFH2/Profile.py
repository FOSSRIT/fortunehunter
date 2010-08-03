import pygame

from fortuneengine.GameEngineElement import GameEngineElement
from fortuneengine.DrawableFontObject import DrawableFontObject
from fortuneengine.DrawableObject import DrawableObject
from constants import MENU_PATH, NORTH, RIGHT, LEFT
from Hero import Hero

from gettext import gettext as _

class Profile(GameEngineElement):
    def __init__(self, recall_string=None, name_entry_cb=None):
        GameEngineElement.__init__(self)
        self.name = ""
        self.dungeon_id = "al1.txt"
        self.position = (-1, -1)
        self.playerFacing=NORTH
        self.hero = Hero()

        # 4 types of stats and difficulties
        self.problem_stats = {}
        self.difficulty = {}
        for stat in ['mult', 'div', 'geo', 'shop']:

            # Each type of stat has 3 "levels" easy, medium, hard
            # Shop uses level for too much, too little, exact
            self.problem_stats[stat] = [(0,0), (0,0), (0,0)]

            #Difficulty: 1=Easy 2=Meduim(default) 3=Hard
            self.difficulty[stat] = 2

        self.puzzlesSolved=0
        self.inventory = []

        bg = pygame.image.load(MENU_PATH+"mafh_splash.gif").convert()
        self.background = DrawableObject([bg], '')
        self.background.scale(self.game_engine.width, self.game_engine.height)
        self.game_engine.get_scene().addObject(self.background)

        #create background rect
        draw_width = self.game_engine.width/4
        draw_height = self.game_engine.height/4
        surf = pygame.Surface((draw_width+60,draw_height+60))
        surf.fill((150,150,255))
        self.blueRect = DrawableObject([surf],"")
        self.game_engine.get_scene().addObject(self.blueRect)
        
        font = pygame.font.Font(None, 16)
        self.text_list = []
        self.text_list.append(DrawableFontObject("1", font))
        self.text_list.append(DrawableFontObject("2", font))
        self.text_list.append(DrawableFontObject("name",font))
        self.game_engine.get_scene().addObjects(self.text_list)
        
        
        if recall_string:
            self.load_from_json_string( recall_string )

        if self.name == "":
            self.name_cb = name_entry_cb
            self.add_to_engine()

    def load_from_json_string( self, recall_string ):
        print "TO BE IMPLEMENTED"

    def dump_to_json_string( self ):
        print "TO BE IMPLEMENTED"

    def update_problem_stat( self, p_type, level, correct ):
        assert( p_type in self.problem_stats )
        assert( level >= 0 and level < len(self.problem_stats) - 1 )

        correct, wrong = self.problem_stats[p_type][level]
        if correct:
            self.problem_stats[p_type][level] = (correct + 1, wrong)
        else:
            self.problem_stats[p_type][level] = (correct, wrong + 1)

    def move_to(self, x, y):
        self.position = (x, y)

    def turn(self, dir):
        if dir == RIGHT:
            self.playerFacing = (self.playerFacing - 1) % 4

        elif dir == LEFT:
            self.playerFacing = (self.playerFacing + 1) % 4

    def give_item(self, item):
        self.inventory.append(item)

    def add_to_engine(self):
        super( Profile, self).add_to_engine()

    def remove_from_engine(self):
        super( Profile, self).remove_from_engine()
        self.game_engine.get_scene().removeObject(self.background)
        self.game_engine.get_scene().removeObject(self.blueRect)
        
        for dfo in self.text_list:
            self.game_engine.get_scene().removeObject(dfo)
            
    def event_handler(self, event):
        """
        Handles user input (used only for name entry)
        """
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key)=='backspace':
                self.name = self.name[0:-1]
                return True
            elif pygame.key.name(event.key)=='return':
                self.remove_from_engine()
                self.name_cb()
                return True
            else:
                self.name+=event.unicode
                return True

    def draw(self,screen,time_delta):
        """
        Draws user input for name to the screen
        """
        width = self.game_engine.width
        height = self.game_engine.height

        draw_width = width/4
        draw_height = height/4

        #font = pygame.font.Font(None, 16)
        #text=font.render(self.name,True,(0,0,0))
        #textRect=(draw_width+60,draw_height+60,text.get_width(),text.get_height())
        #screen.blit(self.background_img,(0,0,width,height))
        #screen.fill((150,150,255),(draw_width,draw_height,2*draw_width,2*draw_height))
        #screen.blit(font.render(_("Enter name:"),True,(0,0,0)),(draw_width,draw_height))
        #screen.blit(font.render(_("Return to continue"),True,(0,0,0)),(draw_width+20,draw_height+20,20,20))
        #screen.blit(text, textRect)
        
        self.background.setPosition(0,0)
        self.blueRect.setPosition(draw_width, draw_height)
        
        #name
        self.text_list[0].changeText(self.name,(0,0,0))
        self.text_list[0].setPosition(draw_width+60, draw_height+60)
        #text1
        self.text_list[1].changeText(_("Enter Name:"), (0,0,0))
        self.text_list[1].setPosition(draw_width,draw_height)
        #text2
        self.text_list[2].changeText(_("Return to continue"), (0,0,0))
        self.text_list[2].setPosition(draw_width+20,draw_height+20)
        

