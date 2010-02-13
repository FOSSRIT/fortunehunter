import pygame, ezmenu

class GameMenuHolder:
    def __init__(self, game_engine, callback, background=None, width=1200, height=900):
        self.ge = game_engine
        self.menu = None
        self.callback = callback
        self.background = background
        self.width = width
        self.height = height
        self._in_engine = False

    def draw(self, screen):
        if self.background:
            screen.blit(pygame.image.load(self.background),(0,0,self.width,self.height))
        else:
            screen.fill((0, 0, 255))

    def __del__(self):
        self.remove_from_engine()

    def add_to_engine(self):
        if not self._in_engine:
            self._in_engine = True
            self.ge.add_draw_callback( self.draw )

    def remove_from_engine(self):
        if self._in_engine:
            self._in_engine = False
            self._clear_menu()
            self.ge.remove_draw_callback(self.draw)

    def _clear_menu(self):
        if self.menu:
            self.ge.remove_event_callback( self.menu.event_handler )
            self.ge.remove_draw_callback( self.menu.draw )
            self.menu = None

    def menu_called(self, id):
        self.callback(id, self)

    def show_menu(self,id):
        if self._in_engine:
            self._clear_menu()
        else:
            self.add_to_engine()

        if id == "title":
            menu_options = [
                    ["Controls", lambda: self.menu_called("controls"), "View Controls"],
                    ["Adventure Play", lambda: self.show_menu("adventure"), "Play standard adventure mode"],
                    ['Creative Play', lambda: self.show_menu("creative"), "Play Custom Maps"],
                    ['Extras', lambda: self.show_menu("extras"), "View Extra Options"],
                    ['Options', lambda: self.menu_called("options"), "View Options Menu"],
                    ['Exit Game', lambda: self.ge.stop_event_loop(), "Exit Game"]
            ]

        elif id == "adventure":
            menu_options = [
                        ["Continue",  lambda: self.menu_called("continue"), "Continues Last Saved Game"],
                        ["Load Game", lambda: self.menu_called("load"), "Loads a saved game"],
                        ["New Game",  lambda: self.menu_called("new"), "Creates a new game"],
                        ["Return to Title", lambda: self.show_menu("title"),"Return to title menu"]
            ]

        elif id == "creative":
            menu_options = [
                        ["Play Custom Map",  lambda: self.menu_called("playcustom"),"NOT IMPLEMENTED"],
                        ["New Custom Map", lambda: self.menu_called("newcustom"),"NOT IMPLEMENTED"],
                        ["Share Map",  lambda: self.menu_called("sharecustom"),"NOT IMPLEMENTED"],
                        ["Return to Title", lambda: self.show_menu("title"), "Return to title menu"]
            ]

        elif id == "network":
            menu_options = [
                        ["Local Cooperative Play",  lambda: self.menu_called("networklocal"),"NOT IMPLEMENTED"],
                        ["Local Treasure Trekkers Play", lambda: self.menu_called("networktreasure"),"NOT IMPLEMENTED"],
                        ["View Scoreboards",  lambda: self.menu_called("networkscore"),"NOT IMPLEMENTED"],
                        ["Return to Title", lambda: self.show_menu("title"), "Returns to title menu"]
            ]

        elif id == "extras":
            menu_options = [
                        ["View Bestiary",  lambda: self.menu_called("viewbestiary"),"NOT IMPLEMENTED"],
                        ["View Awards", lambda: self.menu_called("viewawards"),"NOT IMPLEMENTED"],
                        ["View Statistics",  lambda: self.menu_called("viewstats"),"NOT IMPLEMENTED"],
                        ["Return to Title", lambda: self.show_menu("title"),"NOT IMPLEMENTED"]
            ]

        else:
            print "Invalid Menu", id
            return

        self.menu = GameMenu(menu_options)
        self.ge.add_event_callback( self.menu.event_handler )
        self.ge.add_draw_callback( self.menu.draw )

class GameMenu:
    def __init__(self, game_menu, center_x=800, center_y=400):
        self.menu = ezmenu.EzMenu(game_menu)
        self.menu.center_at(center_x, center_y)
        self.menu.set_font(pygame.font.SysFont("Arial", 32))
        self.menu.set_highlight_color((0, 255, 0))
        self.menu.set_normal_color((255, 255, 255))

    def event_handler(self, event, engine):
        self.menu.update([event])

    def draw(self, screen):
        self.menu.draw( screen )
