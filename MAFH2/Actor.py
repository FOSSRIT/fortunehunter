class Actor:
    def __init__(self):
        self.MHP    = 40    #maximum health points (base HP)
        self.HP     = 40    #current health points
        self.BHP    = 0     #bonus health points (from equipment)
        self.ATT    = 10    #base attack power
        self.BAB    = 0     #bonus attack power (from battle timer)
        self.BAE    = 0     #bonus attack power (from equipment)
        self.DEF    = 1     #base defense power
        self.BDE    = 0     #bonus defense  power(from equipment)
        self.AL     = 0     #Attack Level (0-?)

    #returns actor's current attack power
    def attackPower(self):
        return (self.ATT+self.BAE)
    
    #returns actor's current attack level
    def attackLevel(self):
        return (self.AL)
        
    #returns actor's maximum health
    def maxHealthPoints(self):
        return (self.HP + self.BHP)

    #returns actor's current health
    def healthPoints(self):
        return (self.HP)

    #returns actor's current defense power
    def defensePower(self):
        return (self.DEF + self.BDE)

    #returns actor's equipped items
    def equipment(self):
        return self.eqItems_Ar

    #returns actor's current inventory
    def inventory(self):
        return self.inv_Ar

    #sets enemy's current health
    def setHealth(self,_HP):
        self.HP = _HP

    #sets enemy's bonus health
    def setBonusHP(self,_BHP):
        self.BHP = _BHP

    #sets enemy's bonus attack power (from battle timer)
    def setBonusAP(self,_BAP):
        self.BAP = _BAP

    #sets enemy's bonus attack power (from equipment)
    def setBonusAE(self,_BAE):
        self.BAE = _BAE

    #sets enemy's bonus defense power (from equipment)
    def setBonusDE(self,_BDE):
        self.BDE = _BDE

    #increases player's current health by given amount
    def giveHealth(self,_inc):
        self.HP += _inc
        if self.HP  > self.MHP :
            self.HP = self.MHP

    #player is attacked by given damage
    def defendAttack(self,dmg):
        self.HP -= (dmg - self.defensePower())
        if self.HP<0:
            self.HP=0
        elif self.HP>self.MHP:
            self.HP=self.MHP

    #returns player's list of attacks that are currently available for use
    def availableAttacks(self):
        return self.attacks_Ar

    #add item to equipment
    def addEquipment(self,_item):
        print("add equip")

    def remEquipment(self,_item):
        print("remove equip")
