from GameEngine import GameEngineElement

from TermBox import TermBox

class MafhGameManager(GameEngineElement):
    def __init__(self):
        GameEngineElement.__init__(self)
        self.game_engine.add_object('mesg', TermBox(300,700,800,200,5) )
        self.game_engine.get_object('mesg').add_line("Welcome to Fortune Hunter")
