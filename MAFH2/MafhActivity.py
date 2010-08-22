#!/usr/bin/env python

try:
    from fortuneengine.GameEngine import GameEngine
except:
    # Target system is an xo, so we may not have the module
    # installed, so we want to load the one in our folder
    print "Using forutune engine from path"
    import sys
    sys.path.append( 'fortuneengine' )
    from fortuneengine.GameEngine import GameEngine

from MafhGameMenu import GameMenuHolder
from constants import MENU_PATH, FMC_PATH, TOUR_PATH

from Comic import Comic
from Profile import Profile
from MafhGameManager import MafhGameManager

ge = GameEngine(width=1200, height=900, always_draw=True, fps_cap=24,
                version=True, title="Mathematical Adventure: Fortune Hunter")

def start_game():
    ge.add_object('manager', MafhGameManager() )

def menu_screen():
    ge.add_object('menu', GameMenuHolder( menu_called, MENU_PATH + "mafh_splash.gif", width=ge.width, height=ge.height))
    ge.get_object('menu').show_menu('title')

def menu_called(id, menu):
    if id == 'new':
        #ge.get_object('menu').remove_from_engine()
        menu.remove_from_engine()
        ge.remove_object('menu')

        if not ge.has_object('profile'):
            ge.add_object( 'profile',
                #Profile( name_entry_cb=lambda: ge.add_object('comic', Comic(FMC_PATH+"FMC1/",None,start_game)) ) )
                Profile( name_entry_cb=start_game  ))

    elif id == 'controls':
        menu.remove_from_engine()
        ge.remove_object('menu')
        ge.add_object('comic', Comic(TOUR_PATH+"setup/",None,menu_screen))
    else:
        print "MENU CALLED %s" % id

# Build menu and add to engine.  Then show menu
menu_screen()

# Start event loop
ge.start_main_loop()
