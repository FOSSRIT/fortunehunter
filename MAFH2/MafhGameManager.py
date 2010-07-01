import pygame

from fortuneengine.GameEngineElement import GameEngineElement

from TermBox import TermBox
from Dungeon import Dungeon

class MafhGameManager(GameEngineElement):
    def __init__(self):
        GameEngineElement.__init__(self, has_draw=False, has_event=True)
        self.add_to_engine()

        game_size_ratio_x = self.game_engine.width/1200.0
        game_size_ratio_y = self.game_engine.height/900.0

        term_width_offset = game_size_ratio_x * 200
        term_height = game_size_ratio_y * 200
        term_height_offset = game_size_ratio_y * 700
        term_width = game_size_ratio_x * 1000

        """
        term_width_offset = self.game_engine.width/4
        term_height = self.game_engine.height/6
        term_height_offset = self.game_engine.height - term_height
        term_width = self.game_engine.width - term_width_offset
        """

        self.game_engine.add_object('mesg', TermBox(term_width_offset, term_height_offset,term_width,term_height,5) )
        self.game_engine.get_object('mesg').add_line("Welcome to Fortune Hunter")

        self.game_engine.add_object('dungeon', Dungeon( self.game_engine.get_object('profile').dungeon_id))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            newKey=pygame.key.name(event.key)

            if newKey=='escape':
                print "SHOW Pause Menu"
                return True
