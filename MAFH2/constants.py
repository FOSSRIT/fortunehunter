import os.path
from gettext import gettext as _

BASE_PATH = os.path.dirname(__file__) + "/assets/"
#BASE_PATH = "/home/liveuser/GIT_REPOS/MAFH/mainline/MAFH.activity/assets/"
SOUND_PATH = BASE_PATH + "sound/"
MAP_PATH = BASE_PATH + "map/"
MENU_PATH = BASE_PATH + "image/menu/"
HUD_PATH = BASE_PATH + "image/hud/"
ENV_PATH = BASE_PATH + "image/environment/"
ITEM_PATH = BASE_PATH + "image/item/"
PUZZLE_PATH = BASE_PATH + "image/puzzle/"
FMC_PATH = BASE_PATH + "fmc/"
TOUR_PATH = BASE_PATH + "image/tutorial/"
CHAR_PATH = BASE_PATH + "image/character/"

DOOR_ORDER = ['N','S','E','W']
DOOR_INDEX = {
    'N':_('North'),
    'S':_('South'),
    'E':_('East'),
    'W':_('West')
    }


UNLOCKED_DOOR = 'u'
LOCKED_DOOR = 'l'
PUZZLE_DOOR = 'p'
LOCKED_PUZZLE_DOOR = 'b'
ENTRANCE_DOOR = 'e'
EXIT_DOOR = 'x'

DOOR_FLAGS = {
    '0':_('None'),
    UNLOCKED_DOOR:_('Unlocked'),
    LOCKED_DOOR:_('Locked'),
    PUZZLE_DOOR:_('Puzzle'),
    LOCKED_PUZZLE_DOOR:_('Locked Puzzle'),
    ENTRANCE_DOOR:_('Entrance'),
    EXIT_DOOR:_('Exit')
    }

SPEC_FLAGS = {
    '0':_('None'),
    'M':_('Merchant'),
    'P':_('Puzzle')
    }

ENEM_INDEX = {
    '0':_('None'),
    '1':_('Wizard Adept'),
    '2':_('Goblin'),
    '3':_('Orc'),
    '4':_('Stone Golem'),
    '5':_('Serratula'),
    '6':_('Feren')
    }

ITEM_INDEX = {
    '0':_('None'),
    '1':_("Ancient Amulet"),
    '2':_("Rusted Blade"),
    '3':_("Great Sword"),
    '4':_("Crescent Sword"),
    '5':_("Cardinal"),
    '6':_("Sun Moon"),
    '7':_("Earth Vest"),
    '8':_("Wind Breaker"),
    '9':_("Flame Leggings"),
    'a':_("Dark Cowl"),
    'b':_("Celestial Armor"),
    'c':_("Jewel Shard"),
    'd':_("Broken Hourglass"),
    'e':_("Radiant Vial"),
    'f':_("Honor Tome"),
    'g':_("Valor Tome"),
    'h':_("Ruby"),
    'i':_("Sapphire"),
    'j':_("Emerald"),
    'k':_("Diamond"),
    'l':_("Remedy"),
    'm':_("Elixir"),
    'n':_("Panacea"),
    'o':_("High Elixir"),
    'p':_("Nostrum"),
    'q':_("Small Key"),
    'r':_("Big Key"),
}

ITEM_FLAGS = {
    '0':_('None'),
    'v':_('Visible'),
    'h':_('Hidden'),
    'b':_('Battle')
}

# Integer Driven
THEME_NAME = [
    _('Default Theme'),
    _('Ice'),
    _('Fire'),
    _('Ice'),
    _('Jungle'),
    _('Desert'),
    _('Astral')
    ]

NORTH=1
SOUTH=3
EAST=0
WEST=2

RIGHT = 4
LEFT = 5
