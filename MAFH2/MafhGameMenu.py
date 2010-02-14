import pygame, ezmenu
from GameEngine import GameEngineElement

class GameMenuHolder( GameEngineElement ):
    def __init__(self, callback, background=None, width=1200, height=900):
        GameEngineElement.__init__(self, has_draw=True, has_event=False)
        self.menu = None
        self.callback = callback
        self.background = background
        self.width = width
        self.height = height

    def remove_from_engine(self):
        super( GameMenuHolder, self ).remove_from_engine()
        self.clear_menu()

    def draw(self, screen):
        if self.background:
            screen.blit(pygame.image.load(self.background),(0,0,self.width,self.height))
        else:
            screen.fill((0, 0, 255))

    def menu_called(self, id):
        self.callback(id, self)

    def clear_menu(self):
        if self.menu:
            self.menu.remove_from_engine()
            self.menu = None

    def show_menu(self,id):
        if self.is_in_engine():
            self.clear_menu()
        else:
            self.add_to_engine()

        if id == "title":
            menu_options = [
                    ["Controls", lambda: self.menu_called("controls"), "View Controls"],
                    ["Adventure Play", lambda: self.show_menu("adventure"), "Play standard adventure mode"],
                    ['Creative Play', lambda: self.show_menu("creative"), "Play Custom Maps"],
                    ['Extras', lambda: self.show_menu("extras"), "View Extra Options"],
                    ['Options', lambda: self.menu_called("options"), "View Options Menu"],
                    ['Exit Game', lambda: self.game_engine.stop_event_loop(), "Exit Game"]
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

class GameMenu(GameEngineElement):
    def __init__(self, game_menu, center_x=800, center_y=400):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)
        self.menu = ezmenu.EzMenu(game_menu)
        self.menu.center_at(center_x, center_y)
        self.menu.set_font(pygame.font.SysFont("Arial", 32))
        self.menu.set_highlight_color((0, 255, 0))
        self.menu.set_normal_color((255, 255, 255))
        self.add_to_engine()

    def event_handler(self, event):
        self.menu.update([event])

    def draw(self, screen):
        self.menu.draw( screen )
