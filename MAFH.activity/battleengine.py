
######
# Begin Battle Engine Class
######

class BattleEngine:

	#Bool if it is the players turn or not
	self.playerTurn = 1
	
	#Index that tracks which enemy is up to attack
	self.enemyTurnIndex = 0

	###
	# Basic constructor, takes in the player and a group of enemies
	###
	def __init__(self,character,enemyArr):
		self.player = character
		self.enemies = enemyArr
		self.t = 0
		self.tTracker = 0
		self.maxBonusTime = 0
		print "Enemies are prestent, prepare to fight."
	
	###
	# Attack function. Takes in the attacker, 
	# name of the attack, and trhe defender
	# Subtractgs the damage from defenders 
	# health based off of how much power the attack has.
	###
	def attack(self,attacker,attackName,defender):
		setBonusAP(self.maxBonusTime)
		defender.defendAttack(attacker.attackPower(attackName))
	###
	#Returns a list of attacks for any player or enemy passed in
	###
	def ListAttacks(self,char):
		return char.avaliableAttacks()
	
	###
	# Keeps track of the Bonus Timer, 
	# takes in how long the timer should run
	###
	def BonusTimer(self,timeLength):
		print timeLength

		#Create and Start Timer
				
		self.t = Timer(timeLength,TimerExpire)
		self.t.start()
		self.maxBonusTime = timeLength
		self.tTracker = Timer(1,trackerExpires)
		
		#Update GUI Timer Bar
	
	###
	# Tracks how long the bonus timer has been running
	###
	def trackerExpires(self):
		self.maxBonusTime = self.maxBonusTime - 1
	
	###
	#
	###
	def TimerEpxire(self):
		print "The bonus time is up"
		
		#Change timer GUI bar color????
	
	
	###
	#Picks an attack for the enemy to perform. 
	# takes in which enemy is attacking.
	###
	def GenerateEnemyAttack(self,enemy):
		AvalAttacks = ListAttacks(enemy)
		
		#Fill in AI logic here to pick an attack, for now Math.random
		return AvalAttacks(random.randrange((len(AvalAttacks)-1))
		
	###
	#Called when battle is over and player wins
	###
	def Victory(self):
		print "Victory Method"
		#fill in needed logic
		#Return to travesal system
	
	###
	#Called when battle is over and player wins
	###
	def Defeat(self):
		print "Defeat Method"
		#fill in needed logic
		#end the game
		
	###
	#Checks if the battle is over
	###
	def CheckEndBattle(self):
		if player.healthPoints() < 0:
			Defeat()
		else:
			allDead = true
			for enem in enemies:
				if enem.health <= 0:
					allDead = false
					break
			
			if allDead == true:
				Victory()
	
	###
	# Run updates the battle and keeps things progressing
	###
	def Run(self):
		print "Run Method"
		#Insert logic that updates the battle here
		
		#If player turn, wait for player to select attack then start timer
		
		# if enemy turn, randomly select enemy attack using GenerateEnemeyAttack() and attack
		
		#Run a check to see if battle is over
		self.CheckEndBattle()
	###
	# Uses an item
	###
	def useItem(self,inventoryID):
		#Access players inventory and use the selected item
		
		#Add Health or do damage according to the items description
		
		#Delete Item From Inventory
		
		#Resume
		self.Run()
	
		
		