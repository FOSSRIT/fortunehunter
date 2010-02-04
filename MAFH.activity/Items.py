from gettext import gettext as _

class InvalidItemException(Exception): pass

WEAPONS = {
    '1':{'name':_("Ancient Amulet"),'power':1},
    '2':{'name':_("Rusted Blade"),'power':5},
    '3':{'name':_("Great Sword"),'power':15},
    '4':{'name':_("Crescent Sword"),'power':25},
    '5':{'name':_("Cardinal"),'power':35},
    '6':{'name':_("Sun Moon"),'power':50}
}

ARMOR = {
    '7':{'name':_("Earth Vest"),'power':5},
    '8':{'name':_("Wind Breaker"),'power':15},
    '9':{'name':_("Flame Leggings"),'power':25},
    'a':{'name':_("Dark Cowl"),'power':35},
    'b':{'name':_("Celestial Armor"),'power':50}
}

ACCESSORY = {
    'c':{'name':_("Jewel Shard"),'power':10},
    'd':{'name':_("Broken Hourglass"),'power':10},
    'e':{'name':_("Radiant Vial"),'power':20},
    'f':{'name':_("Honor Tome"),'power':.2},
    'g':{'name':_("Valor Tome"),'power':.2}
    }

USABLE = {
    'h':{'name':_("Ruby"),'sell':500},
    'i':{'name':_("Sapphire"),'sell':500},
    'j':{'name':_("Emerald"),'sell':500},
    'k':{'name':_("Diamond"),'sell':500},
    'l':{'name':_("Remedy"),'sell':2,'buy':20,'power':.10},
    'm':{'name':_("Elixir"),'sell':10,'buy':60,'power':.20},
    'n':{'name':_("Panacea"),'sell':50,'buy':150,'power':.80},
    'o':{'name':_("High Elixir"),'sell':20,'buy':400,'power':.40},
    'p':{'name':_("Nostrum"),'sell':100,'buy':250,'power':.5},
}
KEYS = {
    'q':{'name':_("Small Key")},
    'r':{'name':_("Big Key")}
}

SPECIAL = {
    's':{'name':_("Calculator")}
}

class Item:
    def __init__(self, name, id, type):
        self.name = name
        self.id = id
        self.type = type
        self.power=0
        self.buyVal=0
        self.sellVal=1
        self.hidden=False
        self.battle=False

class Key(Item):
    def __init__(self, key):
        Item.__init__(self, KEYS[key]['name'], key, 'key')

class Weapon(Item):
    def __init__(self, key):
        Item.__init__(self, WEAPONS[key]['name'], key, 'Weapon')
        self.power = WEAPONS[key]['power']

class Armor(Item):
    def __init__(self, key):
        Item.__init__(self, ARMOR[key]['name'], key, 'Armor')
        self.power = ARMOR[key]['power']

class Usable(Item):
    def __init__(self, key):
        Item.__init__(self, USABLE[key]['name'], key, 'Usable')

        if USABLE[key].has_key( 'sell' ):
            self.sellVal = USABLE[key]['sell']

        if USABLE[key].has_key( 'buy' ):
            self.buyVal = USABLE[key]['buy']

        if USABLE[key].has_key( 'power' ):
            self.power = USABLE[key]['power']

class Accessory(Item):
    def __init__(self, key):
        Item.__init__(self, ACCESSORY[key]['name'], key, 'Accessory')
        self.power = ACCESSORY[key]['power']

class Special(Item):
    def __init__(self, key):
        Item.__init__(self, SPECIAL[key]['name'], key, 'Special')


def get_item(key):
    if key in WEAPONS:
        return Weapon( key )
    elif key in ARMOR:
        return Armor( key )
    elif key in ACCESSORY:
        return Accessory( key )
    elif key in USABLE:
        return Usable( key )
    elif key in KEYS:
        return Key( key )
    elif key in SPECIAL:
        return Special( key )
    else:
        raise InvalidItemException()
