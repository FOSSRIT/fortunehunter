from fortuneengine.GameEngine import GameEngine

class GameEngineElement(object):
    def __init__(self, has_draw=True, has_event=True):
        self.__has_draw = has_draw
        self.__has_event = has_event
        self.__in_engine = False
        self.game_engine = GameEngine.instance

    def is_in_engine(self):
        return self.__in_engine

    def add_to_engine(self):
        if not self.__in_engine:
            self.__in_engine = True

            if self.__has_draw:
                self.game_engine.add_draw_callback( self.draw )

            if self.__has_event:
                self.game_engine.add_event_callback( self.event_handler )

    def remove_from_engine(self):
        if self.__in_engine:
            self.__in_engine = False

            if self.__has_draw:
                self.game_engine.remove_draw_callback(self.draw)

            if self.__has_event:
                self.game_engine.remove_event_callback( self.event_handler )

    def event_handler(self, event):
        pass

    def draw(self, screen):
        pass
