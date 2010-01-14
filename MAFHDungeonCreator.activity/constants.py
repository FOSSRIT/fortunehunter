from gettext import gettext as _
DOOR_ORDER = ['N','S','E','W']
DOOR_INDEX = {
    'N':_('North'),
    'S':_('South'),
    'E':_('East'),
    'W':_('West')
    }

DOOR_FLAGS = {
    'u':_('Unlocked'),
    'l':_('Locked'),
    'p':_('Puzzle'),
    'b':_('Locked Puzzle'),
    'e':_('Entrance'),
    'x':_('Exit')
    }

SPEC_FLAGS = {
    '0':_(''),
    'M':_('Merchant'),
    'P':_('Puzzle')
    }

ENEM_INDEX = {
    '0':_('none'),
    '1':_('Wizard Adept'),
    '2':_('Goblin'),
    '3':_('Orc'),
    '4':_('Stone Golem'),
    '5':_('Serratula'),
    '6':_('Feren')
    }

ITEM_INDEX = {

}

ITEM_FLAGS = {
    'v':_('Visible'),
    'h':_('Hidden'),
    'b':_('Battle')
}
