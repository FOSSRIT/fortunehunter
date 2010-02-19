from Actor import Actor
from Items import get_item

#######################################################################
#Hero class - represents the player in battle and holds all of their data
##########################################################################
class Hero(Actor):
  def __init__(self):
    Actor.__init__(self)

    self.weapon=None
    self.armor=None
    self.accessory=None
    self.eqItem=[]          #player can equip up to 4 usable items to use in battle
    self.inv_Ar     = []        #inventory
    self.attacks_Ar = []        #associated array for attack string names and attack power values
    self.currentInput=""
    self.currentProb1=0
    self.currentProb2=0
    self.currentAnswer=0
    self.fractionSum=0
    self.akhal=0

    #amulet=get_item('1')
    #calculator=get_item('s')
    #emptyItem=None
    #self.eqItem=[emptyItem,emptyItem,emptyItem,emptyItem]
    #self.inv_Ar=[amulet,calculator]

  #returns player's current attack power
  def attackPower(self,name):
    if name=="basic":
      return self.ATT+self.BAE
    elif name=="critical":
      return self.ATT+self.BAE+self.BAB
    elif name=="Fire":
      return self.ATT+self.BAB
    elif name=="Heal":
      return self.BAB-10
    elif name=="Lightning":
      return self.ATT+self.BAB
    elif name=="Division":
      return (self.ATT+self.BAE+self.BAB)*1.5
    elif name=="Missile":
      return self.ATT+self.BAB
  def setBonusAP(self,BAP):
    self.BAB=BAP
#****INVENTORY MUTATORS********************************************#
  #add item to equipment
  def equip(self,item):
    #add  _item to equipment
    if item.type=="Weapon":
      if not self.weapon==None:
        self.inv_Ar.append(self.weapon)
      self.weapon=item
      self.inv_Ar.remove(item)
      self.BAE=item.power
    elif item.type=="Armor":
      if not self.armor==None:
        self.inv_Ar.append(self.armor)
      self.armor=item
      self.inv_Ar.remove(item)
      self.BDE=item.power
    elif item.type=="Accessory":
      if not self.accessory==None:
        self.inv_Ar.append(self.accessory)
      self.accessory=item
      self.inv_Ar.remove(item)
      self.BHP=item.power
    elif item.type=="Usable":
        if self.HP < self.MHP:
          self.HP+=int(self.MHP*item.power)
          self.player.migrateMessages("You heal for "+repr(int(self.MHP*item.power)))
          self.inv_Ar.remove(item)
        else:
          self.player.migrateMessages("You are already at full health")
        if self.HP>self.MHP:
          self.HP=self.MHP


  #remove item from equipment
  def remEquipment(self,item):
    if item != None:
      if item.type=="Weapon":
        self.weapon=None
        self.BAE=0
        self.inv_Ar.append(item)
      elif item.type=="Armor":
        self.armor=None
        self.BDE=0
        self.inv_Ar.appen(item)
      elif item.type=="Accessory":
        self.accessory=None
        self.BHP=0
        self.inv_Ar.append(item)
      elif item==None:
        i=0
      else:
        if item in self.eqItem:
          self.eqItem[self.eqItem.index(item)]=None
          self.inv_Ar.append(item)
    #remove _item from equipment -- leave cell empty

  #add item to inventory
  def addInventory(self,item):
    self.inv_Ar.append(item)
    #add _item to end of inventory

  def remInventory(self,item):
    self.inv_Ar.remove(item)
    #remove _item from inventory
#end class Hero
