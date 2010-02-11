import pippy, pygame

class GameEngine:
    def __init__(self, width=1200, height=900):
        pygame.init()
        pygame.mouse.set_visible(False)

        size = width, height

        self.font = pygame.font.Font(None,36)

        self.screen = pygame.display.set_mode(size)

        self.__event_cb = {}

    def start_event_loop(self):
        while pippy.pygame.next_frame():
            for event in pygame.event.get():

                # Send event to all event listeners
                for cb_key in self.__event_cb:
                    self.__event_cb[cb_key](event)


    def add_event_callback(self, id, cb):
        self.__event_cb[id] = cb

    def remove_event_callback(self, id):
        try:
            del self.__event_cb[id]
        except KeyError:
            return False
        return True
