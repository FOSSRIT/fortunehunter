import pygame, ezmenu
from fortuneengine.GameEngineElement import GameEngineElement
from fortuneengine.DrawableObject import DrawableObject

class GameMenuHolder( GameEngineElement ):
    def __init__(self, callback, background=None, width=1200, height=900):
        GameEngineElement.__init__(self, has_draw=True, has_event=False)
        self.menu = None
        self.callback = callback
        self.background = DrawableObject([pygame.image.load(background).convert()])
        self.background.scale(width, height)
        self.game_engine.get_scene().addObject(self.background)
        self.width = width
        self.height = height

    def remove_from_engine(self):
        self.game_engine.get_scene().removeObject(self.background)
        super( GameMenuHolder, self ).remove_from_engine()
        self.clear_menu()

    def draw(self,screen,time_delta):
        if self.background:
            self.background.setPosition(0,0)
        else:
            screen.fill((0, 0, 255))

    def menu_called(self, id):
        self.callback(id, self)

    def clear_menu(self):
        if self.menu:
            self.menu.clear_menu()
            self.menu.remove_from_engine()
            self.menu = None

    def show_menu(self,id):
        if self.is_in_engine():
            self.clear_menu()
        else:
            self.add_to_engine()

        if id == "title":
            menu_options = [
                        ["Adventure Play", lambda: self.show_menu("adventure"), "Begin a new game, create a new profile, or continue from a saved profile game"],
                        #['Creative Play', lambda: self.show_menu("creative"), "Play custom maps and learn how to create them"],
                        #['Network', lambda: self.show_menu("network"), "Play games with special rules or see the scoreboard"],
                        #['Extras', lambda: self.show_menu("extras"), "View special information for the loaded player profile"],
                        #['Options', lambda: self.menu_called("options"), "Change controls, language, difficulty, and other game settings"],
                        #['Options', lambda: self.show_menu("options"), "Change controls, language, difficulty, and other game settings"],
                        ['Exit Game', lambda: self.game_engine.stop_event_loop(), "Exit the game"]
            ]

        elif id == "adventure":
            menu_options = [
                        #["Continue",  lambda: self.menu_called("continue"), "Continue loaded game from the latest save"],
                        #["Level Select",  lambda: self.menu_called("level"), "Play completed levels from loaded game"],
                        #["Load Game", lambda: self.menu_called("load"), "Load player profile game data"],
                        ["New Game",  lambda: self.menu_called("new"), "Play story mode from the beginning"],
                        #["New Player Profile",  lambda: self.menu_called("newpro"), "Create a new player profile"],
                        ["Return to Title", lambda: self.show_menu("title"), "Return to the title menu"]
            ]

        elif id == "creative":
            menu_options = [
                        ["Play Custom Map",  lambda: self.menu_called("playcustom"), "NOT AVAILABLE-Play a custom made map"],
                        ["New Custom Map", lambda: self.menu_called("newcustom"), "NOT AVAILABLE-Learn how to create your own custom map"],
                        ["Share Map",  lambda: self.menu_called("sharecustom"), "NOT AVAILABLE-Share created maps with friends"],
                        ["Return to Title", lambda: self.show_menu("title"), "Return to the title menu"]
            ]

        elif id == "network":
            menu_options = [
                        ["Local Treasure Trekkers Play", lambda: self.menu_called("networktreasure"), "NOT AVAILABLE-Play a special time trial version of Fortune Hunter"],
                        ["View Scoreboard",  lambda: self.menu_called("networkscore"), "NOT AVAILABLE-View the scoreboard for your team"],
                        ["Return to Title", lambda: self.show_menu("title"), "Return to the title menu"]
            ]

        elif id == "extras":
            menu_options = [
                        ["View Bestiary",  lambda: self.menu_called("viewbestiary"), "NOT AVAILABLE-View monster information"],
                        ["View Treasures",  lambda: self.menu_called("viewtreasures"), "NOT AVAILABLE-View collected treasures"],
                        ["View Awards", lambda: self.menu_called("viewawards"), "NOT AVAILABLE-View awards"],
                        ["View Statistics",  lambda: self.menu_called("viewstats"), "NOT AVAILABLE-View statistics"],
                        ["Return to Title", lambda: self.show_menu("title"), "Return to the title menu"]
            ]

        elif id == "options":
            menu_options = [
                       ["Controls", lambda: self.menu_called("controls"), "NOT AVAILABLE-Change control scheme"],
                       ["Language", lambda: self.menu_called("language"), "NOT AVAILABLE-Change language setting"],
                       ["Audio", lambda: self.menu_called("audiu"), "NOT AVAILABLE-Toggle audio on or off"],
                       ["Subtitles", lambda: self.menu_called("subtitles"), "NOT AVAILABLE-Toggle subtitles on or off"],
                       ["FMCs", lambda: self.menu_called("fmcs"), "NOT AVAILABLE-Toggle FMCs on or off"],
                       ["Cooperative Play", lambda: self.menu_called("coop"), "NOT AVAILABLE-Toggle coop mode on or off"],
                       ["Game Difficulty", lambda: self.menu_called("difficulty"), "NOT AVAILABLE-Change the game difficulty setting"],
                       ["Merchant Difficulty", lambda: self.menu_called("merchant"), "NOT AVAILABLE-Change the merchant difficulty setting"],
                       ["Credits", lambda: self.menu_called("credits"), "NOT AVAILABLE-Watch the credits reel"],
                       ["About", lambda: self.menu_called("about"), "NOT AVAILABLE-Information on game and version"],
                       ["Return to Title", lambda: self.show_menu("title"), "Return to the title menu"]
            ]

        else:
            print "Invalid Menu", id
            return

        self.menu = GameMenu(menu_options, self.width, self.height)

class GameMenu(GameEngineElement):
    def __init__(self, game_menu, width=800, height=400):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)
        self.menu = ezmenu.EzMenu(game_menu, self.game_engine.get_scene())
        self.menu.center_at(width - (width/3), height/2)
        self.menu.help_text_at( 0, height-(height/10))
        self.menu.set_font(pygame.font.SysFont("Arial", 20))
        self.menu.set_highlight_color((0, 255, 0))
        self.menu.set_normal_color((255, 255, 255))
        self.add_to_engine()

    def event_handler(self, event):
        return self.menu.update(event)

    def clear_menu(self):
        self.menu.clear_menu()
        
    def draw(self,screen,time_delta):
        self.menu.draw( screen )
