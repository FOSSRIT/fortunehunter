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

SPEC_COLOR = {
    '0':"#6666CC",
    'M':'#666633',
    'P':'#CC6666'
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
    _('Theme 2')
    ]
