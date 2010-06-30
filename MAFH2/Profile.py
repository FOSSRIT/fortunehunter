import pygame

from fortuneengine.GameEngineElement import GameEngineElement
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
        self.background_img = pygame.image.load(MENU_PATH+"mafh_splash.gif")
        super( Profile, self).add_to_engine()

    def remove_from_engine(self):
        super( Profile, self).remove_from_engine()
        del self.background_img

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
        font = pygame.font.Font(None, 32)
        text=font.render(self.name,True,(0,0,0))
        textRect=(400,400,400,400)
        screen.blit(self.background_img,(0,0,1200,900))
        screen.fill((150,150,255),(250,250,600,400))
        screen.blit(font.render(_("Enter name:"),True,(0,0,0)),(300,300,20,20))
        screen.blit(font.render(_("Return to continue"),True,(0,0,0)),(500,500,20,20))
        screen.blit(text, textRect)

