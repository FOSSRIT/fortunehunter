#Hero class - represents the player and holds all of their data
class Hero:
#****property********value**********************description**********************#
	self.MHP 	= 40;				#maximum health points (base HP)
	self.HP		= 40;				#current health points
	self.BHP 	= 0;				#bonus health points (from equipment)
	self.ATT 	= 10; 				#base attack power
	self.BAB	= 0;				#bonus attack power (from battle timer)
	self.BAE	= 0;				#bonus attack power (from equipment)
	self.DEF	= 1;				#base defense power
	self.BDE	= 0;				#bonus defense  power(from equipment)
	self.eqItems_Ar	= new Array(6);	#equipped items
	self.inv_Ar 	= new Array();	#inventory
	self.attacks_Ar = new Array();	#associated array for attack string names and attack power values
	
	#initialize class
	def __init__(self):
		self.inv_Ar = [];
		self.attacks_Ar = [];
	
#****HERO ACCESSORS*********************************************#
	#returns player's maximum health
	def maxHealthPoints(self):
		return (self.HP + self.BHP);
	
	#returns player's current health
	def healthPoints(self):
		return (self.HP);
	
	#returns player's current attack power
	def attackPower(self):
		return (self.ATT + self.BAB + self.BAE);
	
	#returns player's current defense power
	def defensePower(self):
		return (self.DEF + self.BDE);
		
	#returns player's equipped items
	def equipment(self):
		return self.eqItems_Ar;
	
	#returns player's current inventory
	def inventory(self):
		return self.inv_Ar;
		
#****HERO MUTATORS************************************************#
	#sets player's current health
	def setHealth(self,_HP):
		self.HP = _HP;
		
	#sets player's bonus health
	def setBonusHP(self,_BHP):
		self.BHP = _BHP;
		
	#sets player's bonus attack power (from battle timer)
	def setBonusAP(self,_BAP):
		self.BAB = _BAB;
		
	#sets player's bonus attack power (from equipment)
	def setBonusAE(self,_BAE):
		self.BAE = _BAE;
	
	#sets player's bonus defense power (from equipment)
	def setBonusDE(self,_BDE):
		self.BDE = _BDE;
		
	#increases player's current health by given amount
	def giveHealth(self,_inc):
		self.HP += _inc;
		
		if(healthPoints( ) > maxHealthPoints( ))
			setHealth(maxHealthPoints( ));
	
	#player is attacked by given damage
	def defendAttack(self,dmg):
		self.HP -= (dmg - defensePower( ));

#****BATTLE ACCESSORS***********************************************#
	#returns player's list of attacks that are currently available for use
	def availableAttacks(self):
		return self.attacks_Ar;
	
#****INVENTORY MUTATORS********************************************#
	#add item to equipment
	def addEquipment(self,_item):
		#add  _item to equipment
		if _item.getType( ) is "WEAPON":
			eqItem_Ar[0] = _item;
		else if _item.getType( ) is "ARMOR":
			eqItem_Ar[1] = _item;
		else:
			for i in range(2,5):  # go through the rest of the equipped items, trade out values
			#look through last 4 slots, find empty cell and add. Otherwise you must unequip an item first to have an empty cell
			
		#alternative
			#depending on item type - only give access to certain cells. So, if item is WEAP, only allow equip on slot 0, if item is ARM, only allow equip on slot1, if item is ITEM, only allow equip on slots2-5, whatever slot is picked -trade values (unequip item and equip new)
		
	#remove item from equipment
	def remEquipment(self,_item):
		#remove _item from equipment -- leave cell empty
		
	#add item to inventory
	def addInventory(self,_item):
		#add _item to end of inventory
		
	#remove item from inventory
	def remInventory(self,_item):
		#remove _item from inventory
		
#end class Hero