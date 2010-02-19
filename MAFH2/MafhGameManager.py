import pygame

from GameEngine import GameEngineElement

from TermBox import TermBox
from Dungeon import Dungeon

class MafhGameManager(GameEngineElement):
    def __init__(self):
        GameEngineElement.__init__(self, has_draw=False, has_event=True)
        self.add_to_engine()

        self.game_engine.add_object('mesg', TermBox(200,700,1000,200,5) )
        self.game_engine.get_object('mesg').add_line("Welcome to Fortune Hunter")

        self.game_engine.add_object('dungeon', Dungeon( self.game_engine.get_object('profile').dungeon_id))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            newKey=pygame.key.name(event.key)

            if newKey=='escape':
                print "SHOW Pause Menu"
                return True
