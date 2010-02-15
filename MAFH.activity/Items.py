from gettext import gettext as _

class InvalidItemException(Exception): pass

WEAPONS = {
    '1':{'name':_("Ancient Amulet"),'power':3,'path':'Weapon.gif'},
    '2':{'name':_("Rusted Blade"),'power':9,'path':'Weapon.gif'},
    '3':{'name':_("Great Sword"),'power':15,'path':'Weapon.gif'},
    '4':{'name':_("Crescent Sword"),'power':25,'path':'Weapon.gif'},
    '5':{'name':_("Cardinal"),'power':35,'path':'Weapon.gif'},
    '6':{'name':_("Sun Moon"),'power':50,'path':'Weapon.gif'}
}

ARMOR = {
    '7':{'name':_("Earth Vest"),'power':8,'path':'Armor.gif'},
    '8':{'name':_("Wind Breaker"),'power':15,'path':'Armor.gif'},
    '9':{'name':_("Flame Leggings"),'power':25,'path':'Armor.gif'},
    'a':{'name':_("Dark Cowl"),'power':35,'path':'Armor.gif'},
    'b':{'name':_("Celestial Armor"),'power':50,'path':'Armor.gif'}
}

ACCESSORY = {
    'c':{'name':_("Jewel Shard"),'power':10,'path':'noItem.gif'},
    'd':{'name':_("Broken Hourglass"),'power':10,'path':'noItem.gif'},
    'e':{'name':_("Radiant Vial"),'power':20,'path':'noItem.gif'},
    'f':{'name':_("Honor Tome"),'power':.2,'path':'noItem.gif'},
    'g':{'name':_("Valor Tome"),'power':.2,'path':'noItem.gif'}
    }

USABLE = {
    'h':{'name':_("Ruby"),'sell':500,'path':'Ruby.gif'},
    'i':{'name':_("Sapphire"),'sell':500,'path':'Sapphire.gif'},
    'j':{'name':_("Emerald"),'sell':500,'path':'Emerald.gif'},
    'k':{'name':_("Diamond"),'sell':500,'path':'Diamond.gif'},
    'l':{'name':_("Remedy"),'sell':6,'buy':20,'power':.30,'path':'Remedy.gif'},
    'm':{'name':_("Elixir"),'sell':15,'buy':60,'power':.5,'path':'Elixir.gif'},
    'n':{'name':_("Panacea"),'sell':50,'buy':100,'power':1.0,'path':'Panacea.gif'},
    'o':{'name':_("High Elixir"),'sell':30,'buy':300,'power':.65,'path':'High Elixir.gif'},
    'p':{'name':_("Nostrum"),'sell':100,'buy':200,'power':.75,'path':'Nostrum.gif'},
}
KEYS = {
    'q':{'name':_("Small Key"),'path':'Small Key.gif'},
    'r':{'name':_("Big Key"),'path':'Big Key.gif'}
}

SPECIAL = {
    's':{'name':_("Calculator")}
}

class Item:
    def __init__(self, name, id, type, path='noItem.gif'):
        self.name = name
        self.id = id
        self.type = type
        self.power=0
        self.buyVal=0
        self.path=path
        self.sellVal=1
        self.hidden=False
        self.battle=False

class Key(Item):
    def __init__(self, key):
        Item.__init__(self, KEYS[key]['name'], key, 'key', KEYS[key]['path'])

class Weapon(Item):
    def __init__(self, key):
        Item.__init__(self, WEAPONS[key]['name'], key, 'Weapon', WEAPONS[key]['path'])
        self.power = WEAPONS[key]['power']

class Armor(Item):
    def __init__(self, key):
        Item.__init__(self, ARMOR[key]['name'], key, 'Armor', ARMOR[key]['path'])
        self.power = ARMOR[key]['power']

class Usable(Item):
    def __init__(self, key):
        Item.__init__(self, USABLE[key]['name'], key, 'Usable', USABLE[key]['path'])

        if USABLE[key].has_key( 'sell' ):
            self.sellVal = USABLE[key]['sell']

        if USABLE[key].has_key( 'buy' ):
            self.buyVal = USABLE[key]['buy']

        if USABLE[key].has_key( 'power' ):
            self.power = USABLE[key]['power']

class Accessory(Item):
    def __init__(self, key):
        Item.__init__(self, ACCESSORY[key]['name'], key, 'Accessory', ACCESSORY[key]['path'])
        self.power = ACCESSORY[key]['power']

class Special(Item):
    def __init__(self, key):
        Item.__init__(self, SPECIAL[key]['name'], key, 'Special', SPECIAL[key]['path'])

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
