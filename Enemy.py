#Enemy class - represents an enemy and holds all of its data
class Enemy:
#****property********value**********************description**********************#
	self.MHP 	= 40;				#maximum health points (base HP)
	self.HP		= 40;				#current health points
	self.BHP 	= 0;				#bonus health points (from equipment)
	self.ATT 	= 10; 				#base attack power
	self.BAE	= 0;				#bonus attack power (from equipment)
	self.DEF	= 1;				#base defense power
	self.BDE	= 0;				#bonus defense  power(from equipment)
	self.eqItems_Ar	= new Array();	#equipped items
	self.attacks_Ar = new Array();	#associated array for attack string names and attack power values
	
	#initialize class
	def __init__(self):
		self.eqItem_Ar = [];
		self.inv_Ar = [];
		self.attacks_Ar = [];
	
#****ENEMY ACCESSORS*********************************************#
	#returns enemy's maximum health
	def maxHealthPoints(self):
		return (self.HP + self.BHP);
	
	#returns enemy's current health
	def healthPoints(self):
		return (self.HP);
	
	#returns enemy's current attack power
	def attackPower(self):
		return (self.ATT + self.BAB + self.BAE);
	
	#returns enemy's current defense power
	def defensePower(self):
		return (self.DEF + self.BDE);
		
	#returns enemy's equipped items
	def equipment(self):
		return self.eqItems_Ar;
	
	#returns enemy's current inventory
	def inventory(self):
		return self.inv_Ar;
		
#****ENEMY MUTATORS************************************************#
	#sets enemy's current health
	def setHealth(self,_HP):
		self.HP = _HP;
		
	#sets enemy's bonus health
	def setBonusHP(self,_BHP):
		self.BHP = _BHP;
		
	#sets enemy's bonus attack power (from battle timer)
	def setBonusAP(self,_BAP):
		self.BAB = _BAB;
		
	#sets enemy's bonus attack power (from equipment)
	def setBonusAE(self,_BAE):
		self.BAE = _BAE;
	
	#sets enemy's bonus defense power (from equipment)
	def setBonusDE(self,_BDE):
		self.BDE = _BDE;
		
	#increases enemy's current health by given amount
	def giveHealth(self,_inc):
		self.HP += _inc;
		
		if(healthPoints(self) > maxHealthPoints(self))
			setHealth(self,maxHealthPoints(self));
	
	#enemy is attacked by given damage
	def defendAttack(self,dmg):
		self.HP -= (dmg - defensePower(self));
		
#****BATTLE ACCESSORS***********************************************#
	#returns player's list of attacks that are currently available for use
	def availableAttacks(self):
		return self.attacks_Ar;
		
#****INVENTORY MUTATORS********************************************#
	#add item to equipment
	def addEquipment(self,_item):
		#add  _item to equipment
		#if _item is weapon - add to first slot
		#if _item is armor - add to second slot
		#if _item is consumable - add to slots 3-6
		
	#remove item from equipment
	def remEquipment(self,_item):
		#remove _item from equipment -- leave cell empty
	
#end class Enemy