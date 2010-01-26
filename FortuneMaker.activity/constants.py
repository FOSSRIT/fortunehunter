from gettext import gettext as _
DOOR_ORDER = ['N','S','E','W']
DOOR_INDEX = {
    'N':_('North'),
    'S':_('South'),
    'E':_('East'),
    'W':_('West')
    }

DOOR_FLAGS = {
    '0':_('None'),
    'u':_('Unlocked'),
    'l':_('Locked'),
    'p':_('Puzzle'),
    'b':_('Locked Puzzle'),
    'e':_('Entrance'),
    'x':_('Exit')
    }

DOOR_COLOR = {
    'u':"#000000",
    'l':"#666666",
    'p':"#006600",
    'b':"#008800",
    'e':"#ff0000",
    'x':"#ffff00"
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
    '0':_('None')

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
    _('Theme 2')
    ]
