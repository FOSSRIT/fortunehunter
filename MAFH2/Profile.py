import pygame

from GameEngine import GameEngineElement
from constants import MENU_PATH

from gettext import gettext as _

class Profile(GameEngineElement):
    def __init__(self, recall_string=None, name_entry_cb=None):
        GameEngineElement.__init__(self)
        self.name = ""
        self.dungeon_id = -1
        self.position = (0, 0)

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

    def event_handler(self, event):
        """
        Handles user input (used only for name entry)
        """
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key)=='backspace':
                self.name = self.name[0:-1]
            elif pygame.key.name(event.key)=='return':
                self.remove_from_engine()
                self.name_cb()
            else:
                self.name+=event.unicode

    def draw(self, screen):
        """
        Draws user input for name to the screen
        """
        font = pygame.font.Font(None, 32)
        text=font.render(self.name,True,(0,0,0))
        textRect=(400,400,400,400)
        screen.blit(pygame.image.load(MENU_PATH+"mafh_splash.gif"),(0,0,1200,900))
        screen.fill((150,150,255),(250,250,600,400))
        screen.blit(font.render(_("Enter name:"),True,(0,0,0)),(300,300,20,20))
        screen.blit(font.render(_("Return to continue"),True,(0,0,0)),(500,500,20,20))
        screen.blit(text, textRect)

