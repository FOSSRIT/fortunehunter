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
    '8':_("Dark Cowl"),
    '9':_("Celestial Armor"),
    'a':_("Jewel Shard"),
    'b':_("Broken Hourglass"),
    'c':_("Radiant Vial"),
    'd':_("Honor Tome"),
    'e':_("Valor Tome"),
    'f':_("Ruby"),
    'g':_("Sapphire"),
    'h':_("Emerald"),
    'i':_("Diamond"),
    'j':_("Remedy"),
    'k':_("Elixir"),
    'l':_("Panacea"),
    'm':_("High Elixir"),
    'n':_("Nostrum")
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
