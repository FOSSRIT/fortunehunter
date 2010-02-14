from GameEngine import GameEngine
from MafhGameMenu import GameMenuHolder

from constants import MENU_PATH, FMC_PATH, TOUR_PATH

from Comic import Comic
from TermBox import TermBox
ge = GameEngine()

def start_game():
    ge.add_object('mesg', TermBox(300,700,800,200,5) )
    ge.get_object('mesg').add_line("Welcome to Fortune Hunter")

    if not ge.has_object('profile'):
        #TODO Create game profile

        pass

    print "START GAME NOW"

def menu_screen():
    ge.add_object('menu', GameMenuHolder( menu_called, MENU_PATH + "mafh_splash.gif"))
    ge.get_object('menu').show_menu('title')

def menu_called(id, menu):
    if id == 'new':
        #ge.get_object('menu').remove_from_engine()
        menu.remove_from_engine()
        ge.remove_object('menu')
        ge.add_object('comic', Comic(ge, FMC_PATH+"FMC1/",None,start_game))
    if id == 'controls':
        menu.remove_from_engine()
        ge.remove_object('menu')
        ge.add_object('comic', Comic(ge, TOUR_PATH+"setup/",None,menu_screen))
    else:
        print "MENU CALLED %s" % id

# Build menu and add to engine.  Then show menu
menu_screen()

# Draw and start event loop
ge.draw()
ge.start_event_loop()
