import pygame
from GameEngine import GameEngineElement

from constants import MENU_PATH
from gettext import gettext as _

class BattleMenuHolder( GameEngineElement ):
    def __init__(self, callback):
        GameEngineElement.__init__(self, has_draw=True, has_event=False)
        self.menu = None
        self.callback = callback
        self.background = pygame.image.load(MENU_PATH + "battleMenubackground.gif")
        self.buttonback = pygame.image.load(MENU_PATH + "Blank.gif")

    def remove_from_engine(self):
        super( GameMenuHolder, self ).remove_from_engine()
        self.clear_menu()

    def draw(self, screen):
        screen.blit(self.background,(0,286,452,414))

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

        if id == "selection":
            menu_options = [
                        [_("Attack"), lambda: self.show_menu("attack")],
                        [_('Special'), lambda: self.show_menu("special")],
                        [_('Magic'), lambda: self.show_menu("magic")],
                        [_('Scan'), lambda: self.menu_called("scan")],
            ]

        elif id == "attack":
            menu_options = [
                        ["__TODO__",  lambda: self.menu_called("TODO")],
                        [_("Back"), lambda: self.show_menu("selection")]
            ]

        elif id == "special":
            menu_options = [
                        ["__TODO__",  lambda: self.menu_called("TODO")],
                        [_("Back"), lambda: self.show_menu("selection")]
            ]

        elif id == "magic":
            menu_options = [
                        [_("Fire"),  lambda: self.menu_called("fire")],
                        [_("Lightning"),  lambda: self.menu_called("lightning")],
                        [_("Missile"), lambda: self.menu_called("missile")],
                        [_("Heal"),  lambda: self.menu_called("heal")],
                        [_("Back"), lambda: self.show_menu("selection")]
            ]

        else:
            print "Invalid Menu", id
            return

        self.menu = BattleMenu(menu_options, 230, 375, self.buttonback)


class BattleMenu(GameEngineElement):
    def __init__(self, game_menu, x, y, button):
        GameEngineElement.__init__(self, has_draw=True, has_event=True)
        self.menu = Menu(game_menu, button)
        self.menu.set_pos(x, y)
        self.add_to_engine()

    def event_handler(self, event):
        return self.menu.update(event)

    def draw(self, screen):
        self.menu.draw( screen )

class Menu(object):
    def __init__(self, options, button):
        """Initialise the EzMenu! options should be a sequence of lists in the
        format of [option_name, option_function]"""

        self.options = options
        self.button = button
        self.x = 0
        self.y = 0
        self.font = pygame.font.SysFont("cmr10",18,False,False)
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [255, 0, 0]
        self.height = len(self.options)*self.font.get_height()

    def draw(self, surface):
        """Draw the menu to the surface."""
        i=0
        help_txt = ""
        for o in self.options:
            if i==self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = o[0]
            ren = self.font.render(text, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(self.button, (self.x, self.y + i*45))
            surface.blit(ren, (self.x + 15, self.y + 12 + i*45))
            i+=1


    def update(self, event):
        """Update the menu and get input for the menu."""
        return_val = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.option += 1
                return_val = True
            elif event.key == pygame.K_UP:
                self.option -= 1
                return_val = True
            elif event.key == pygame.K_RETURN:
                self.options[self.option][1]()
                return_val = True

        if self.option > len(self.options)-1:
            self.option = 0
        elif self.option < 0:
            self.option = len(self.options)-1

        return return_val

    def set_pos(self, x, y):
        """Set the topleft of the menu at x,y"""
        self.x = x
        self.y = y
