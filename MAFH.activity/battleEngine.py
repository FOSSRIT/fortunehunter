import pippy, pygame, sys, math
from player import *
from hero import *
from enemy import *
from menu import *
from pygame.locals import *
from random import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

###################################################################

# Begin Battle Engine Class

################################################################
class BattleEngine:
  def __init__(self,player,enemyArr):
	#Bool if it is the players turn or not
	self.playerTurn = True
	#Index that tracks which enemy is up to attack
	self.enemyTurnIndex = 0
	###
	# Basic constructor, takes in the player and a group of enemies
	###
	self.player = player
	self.enemies = enemyArr
	self.t = 0
	self.tTracker = 0
	self.maxBonusTime = 0
        self.initializeMenus(player)
        self.selEnemyIndex=0
        self.timeBonus=1
        #load glyphs and buttons
        self.fire=pygame.sprite.Sprite()
        self.fire.image=pygame.image.load(IMG_PATH+"FireGlyph.gif")
        self.fire1=pygame.sprite.Sprite()
        self.fire1.image=pygame.image.load(IMG_PATH+"FireGlyph1.gif")
        self.fire1btn=IMG_PATH+"FireGlyph1btn.gif"
        self.fire2=pygame.sprite.Sprite()
        self.fire2.image=pygame.image.load(IMG_PATH+"FireGlyph2.gif")
        self.fire2btn=IMG_PATH+"FireGlyph2btn.gif"
        self.fire3=pygame.sprite.Sprite()
        self.fire3.image=pygame.image.load(IMG_PATH+"FireGlyph3.gif")
        self.fire3btn=IMG_PATH+"FireGlyph3btn.gif"
        self.fire4=pygame.sprite.Sprite()
        self.fire4.image=pygame.image.load(IMG_PATH+"FireGlyph4.gif")
        self.fire4btn=IMG_PATH+"FireGlyph4btn.gif"

        self.lightning=pygame.sprite.Sprite()
	self.lightning.image=pygame.image.load(IMG_PATH+"LightningGlyph.gif")
        self.lightning1btn=IMG_PATH+"LightningGlyph1btn.gif"
        self.lightning1=pygame.sprite.Sprite()
	self.lightning1.image=pygame.image.load(IMG_PATH+"LightningGlyph1.gif")
        self.lightning2btn=IMG_PATH+"LightningGlyph2btn.gif"
        self.lightning2=pygame.sprite.Sprite()
	self.lightning2.image=pygame.image.load(IMG_PATH+"LightningGlyph2.gif")
        self.lightning3btn=IMG_PATH+"LightningGlyph3btn.gif"
        self.lightning3=pygame.sprite.Sprite()
	self.lightning3.image=pygame.image.load(IMG_PATH+"LightningGlyph3.gif")
        self.lightning4btn=IMG_PATH+"LightningGlyph4btn.gif"
        self.lightning4=pygame.sprite.Sprite()
	self.lightning4.image=pygame.image.load(IMG_PATH+"LightningGlyph4.gif")

        self.missile=pygame.sprite.Sprite()
	self.missile.image=pygame.image.load(IMG_PATH+"MagicGlyph.gif")

        self.heal=pygame.sprite.Sprite()
	self.heal.image=pygame.image.load(IMG_PATH+"HealGlyph.gif")
        self.heal1btn=IMG_PATH+"HealGlyph1btn.gif"
        self.heal1=pygame.sprite.Sprite()
	self.heal1.image=pygame.image.load(IMG_PATH+"HealGlyph1.gif")
        self.heal2btn=IMG_PATH+"HealGlyph2btn.gif"
        self.heal2=pygame.sprite.Sprite()
	self.heal2.image=pygame.image.load(IMG_PATH+"HealGlyph2.gif")
        self.heal3btn=IMG_PATH+"HealGlyph3btn.gif"
        self.heal3=pygame.sprite.Sprite()
	self.heal3.image=pygame.image.load(IMG_PATH+"HealGlyph3.gif")
        self.heal4btn=IMG_PATH+"HealGlyph4btn.gif"
        self.heal4=pygame.sprite.Sprite()
	self.heal4.image=pygame.image.load(IMG_PATH+"HealGlyph4.gif")

	self.glyphGroup=pygame.sprite.Group()
	self.glyphOverlayGroup=pygame.sprite.Group()
        self.enemyValue=0
        i=0
	for enemy in self.enemies:
          enemy.place=i
          i+=1
	self.player.msg5= "Enemies are present, prepare to fight."

  def initializeMenus(self,player):

    battleOptions=["Attack","Division","Geometry","Use Item"]
    battleBackground=IMG_PATH+"battleMenubackground.gif"
    battleOptImg=[IMG_PATH+"Attack.gif",IMG_PATH+"Special.gif",IMG_PATH+"Magic.gif",IMG_PATH+"Item.gif"]
    
    self.battleMenu=Menu(battleOptions,player,battleBackground,battleOptImg,"Battle")
    self.battleMenu.background.rect=(0,300,0,200)

    numOptArr = ["1","2","3","4","5","6","7","8","9","0","Clear","Enter Answer"]
    numBG=IMG_PATH+"battleMenubackground.gif"
    numOptImg=[IMG_PATH+"1.gif",IMG_PATH+"2.gif",IMG_PATH+"3.gif",IMG_PATH+"4.gif",IMG_PATH+"5.gif",IMG_PATH+"6.gif",IMG_PATH+"7.gif",IMG_PATH+"8.gif",IMG_PATH+"9.gif",IMG_PATH+"0.gif",IMG_PATH+"Clear.gif",IMG_PATH+"Enter.gif"]
    self.numPadMenu=Menu(numOptArr,player,numBG,numOptImg,"Number Pad")
    self.numPadMenu.background.rect=(0,300,200,200)
    self.numPadMenu.numPad=True

    magicOptions=["Fire","Lightning","Missile","Heal"]
    magicBackground=IMG_PATH+"battleMenubackground.gif"
    magicOptImg=[IMG_PATH+"Fire.gif",IMG_PATH+"Lightning.gif",IMG_PATH+"Missile.gif",IMG_PATH+"Heal.gif"]
    self.magicMenu=Menu(magicOptions,player,magicBackground,magicOptImg,"Magic Menu")
    self.magicMenu.background.rect=(0,300,200,200)

    divisionOptions=["1/2","1/3","1/4","1/6"]
    divisionBackground=IMG_PATH+"battleMenubackground.gif"
    divisionOptImg=[IMG_PATH+"12Power.gif",IMG_PATH+"13Power.gif",IMG_PATH+"14Power.gif",IMG_PATH+"16Power.gif"]
    self.divisionMenu=Menu(divisionOptions,player,divisionBackground,divisionOptImg,"Division Menu")
    self.divisionMenu.background.rect=(0,300,200,200) 

    itemOptions=["Item1","Item2","Item3","Item4"]
    itemBackground=IMG_PATH+"battleMenubackground.gif"
    itemOptImg=[IMG_PATH+"Blank.gif",IMG_PATH+"Blank.gif",IMG_PATH+"Blank.gif",IMG_PATH+"Blank.gif"]
    
    self.itemMenu=Menu(itemOptions,player,itemBackground,itemOptImg,"Item")
    self.itemMenu.background.rect=(0,300,200,200)

    self.player.currentMenu=self.battleMenu
    self.player.previousMenu=self.numPadMenu

  def draw(self,player,screen):
    #draw enemies
    x=250
    y=150
    enemyGroup=pygame.sprite.Group()
    i=0
    for enemy in self.enemies:
      enemy.sprite.rect=pygame.Rect((x+(enemy.place*200),y,200,200))
      if i==self.selEnemyIndex:
        sel=pygame.sprite.Sprite()
        sel.image=pygame.image.load(IMG_PATH+"0.gif")
        sel.rect=pygame.Rect(x+(enemy.place*200)+30,y+100,40,20)
        enemyGroup.add(sel)
      i+=1
      enemyGroup.add(enemy.sprite)

    player.currentRoomGroup.draw(screen)
    enemyGroup.draw(screen)
    self.glyphGroup.draw(screen)
    self.glyphOverlayGroup.draw(screen)

    #draw player
    if player.currentMenu.numPad==False:
      player.currentMenu.draw(player,screen,235,450,45)
      if player.currentMenu.name=="Item":
        i=0
        for image in player.currentMenu.optionsImages:
          if i<len(player.battlePlayer.eqItem):
            font = pygame.font.Font(None, 36)
            t=font.render(player.battlePlayer.eqItem[i].name,True,(255,255,255))
            screen.blit(t,image.rect) 
            i+=1     
      elif player.currentMenu.name=="Division Menu" or player.currentMenu.name=="DivTut2":
        screen.fill((0,0,0),(500,300,100,400))
        screen.fill((255,150,0),(500,(620-310*player.battlePlayer.fractionSum),137,310*player.battlePlayer.fractionSum))
        player.divSword.draw(screen)
    else:
      if player.currentMenu.name=="GeomTut3" or player.currentMenu.name=="Glyph Menu":
        player.currentMenu.draw(player,screen,235,390,60)
      else:
        player.currentMenu.draw(player,screen,235,450,40)
      if not player.battlePlayer.currentProb1=="":
        font = pygame.font.Font(None, 36)
        probText=font.render(repr(player.battlePlayer.currentProb1)+" X "+repr(player.battlePlayer.currentProb2),True,(255,255,255))
        inputText=font.render(player.battlePlayer.currentInput,True,(50,0,150))
        if player.currentMenu.name=="Number Pad" or player.currentMenu.name=="CritTut":
          screen.blit(probText,pygame.Rect(250,350,200,30))
          screen.blit(inputText,pygame.Rect(250,400,200,30))
      
      screen.fill((50,250,50),pygame.Rect(200,50,self.timeBonus*500,50))
    pygame.display.flip()

  ###
  # Attack function. Takes in the attacker, 
  # name of the attack, and trhe defender
  # Subtractgs the damage from defenders 
  # health based off of how much power the attack has.
  ###
  def doNothing(self):
    self.playerTurn=False
    self.player.currentMenu=self.battleMenu

  def attack(self,attacker,attackName):
    if attackName=="critical":
      attacker.setBonusAP(attacker.currentAnswer+int(self.timeBonus*10))
    elif attackName=="Fire":
      attacker.setBonusAP(int(self.timeBonus*20)+50)
      self.glyphGroup.empty()
      self.glyphOverlayGroup.empty()
      self.player.currentMenu=self.battleMenu
    elif attackName=="Heal":
      attacker.setBonusAP(-1*(int(self.timeBonus*20)+10))
      self.glyphGroup.empty()
      self.glyphOverlayGroup.empty()
      self.player.currentMenu=self.battleMenu
    elif attackName=="Lightning":
      attacker.setBonusAP(int(self.timeBonus)+70)
      self.glyphGroup.empty()
      self.glyphOverlayGroup.empty()
      self.player.currentMenu=self.battleMenu
    elif attackName=="Missile":
      attacker.setBonusAP(0)
      self.player.currentMenu=self.battleMenu
    elif attackName=="Division":
      self.player.currentMenu=self.battleMenu

    pygame.time.set_timer(USEREVENT+1,0)
    self.timeBonus=1

    defender=self.enemies[self.selEnemyIndex]
    if attackName=="Heal":
      defender=attacker
      if -1*int(attacker.attackPower(attackName))>attacker.MHP:
        player.migrateMessages("You heal to full health")
      else:
        player.migrateMessages("You heal "+repr(-1*int(attacker.attackPower(attackName)))+" HP")
    else:
      player.migrateMessages("You attack for "+repr(int(attacker.attackPower(attackName)))+" damage")
      player.migrateMessages("Enemy HP is "+repr(int(defender.HP)))

    defender.defendAttack(attacker.attackPower(attackName))
    self.playerTurn=False
    #self.CheckEndBattle()
    player.currentMenu=self.battleMenu

  def critical(self,player):
    pygame.time.set_timer(USEREVENT+1,1000)
    player.battlePlayer.currentInput=""
    player.currentMenu=self.numPadMenu
    prob1=randint(0,12)
    prob2=randint(0,12)
    player.battlePlayer.currentProb1=prob1
    player.battlePlayer.currentProb2=prob2
    player.battlePlayer.currentAnswer=prob1*prob2

  def magic(self,player):
    player.currentMenu=self.magicMenu
    pygame.time.set_timer(USEREVENT+1,1000)
  def startGlyph(self,name):
    self.glyphGroup.empty()
    self.glyphOverlayGroup.empty()
    if name=="Fire":
      shuffle2D=[("Fire1",self.fire1btn),("Fire2",self.fire2btn),("Fire3",self.fire3btn),("Fire4",self.fire4btn),("Not",self.heal1btn),("Not",self.heal4btn),("Not",self.lightning3btn),("Not",self.lightning1btn)]
      shuffle(shuffle2D)
      glyphMenuOptions=[shuffle2D[0][0],shuffle2D[1][0],shuffle2D[2][0],shuffle2D[3][0],shuffle2D[4][0],shuffle2D[5][0],shuffle2D[6][0],shuffle2D[7][0]]
      glyphMenuImages=[shuffle2D[0][1],shuffle2D[1][1],shuffle2D[2][1],shuffle2D[3][1],shuffle2D[4][1],shuffle2D[5][1],shuffle2D[6][1],shuffle2D[7][1]]
      glyphMenu=Menu(glyphMenuOptions,self.player,IMG_PATH+"battleMenubackground.gif",glyphMenuImages,"Glyph Menu")
      glyphMenu.numPad=True
      glyphMenu.background.rect=(0,300,200,200)
      player.currentMenu=glyphMenu
      self.fire.rect=(500,350,300,300)
      self.glyphGroup.add(self.fire)
    elif name=="Lightning":
      shuffle2D=[("Lightning1",self.lightning1btn),("Lightning2",self.lightning2btn),("Lightning3",self.lightning3btn),("Lightning4",self.lightning4btn),("Not",self.heal1btn),("Not",self.heal2btn),("Not",self.fire3btn),("Not",self.fire1btn)]
      shuffle(shuffle2D)
      glyphMenuOptions=[shuffle2D[0][0],shuffle2D[1][0],shuffle2D[2][0],shuffle2D[3][0],shuffle2D[4][0],shuffle2D[5][0],shuffle2D[6][0],shuffle2D[7][0]]
      glyphMenuImages=[shuffle2D[0][1],shuffle2D[1][1],shuffle2D[2][1],shuffle2D[3][1],shuffle2D[4][1],shuffle2D[5][1],shuffle2D[6][1],shuffle2D[7][1]]
      glyphMenu=Menu(glyphMenuOptions,self.player,IMG_PATH+"battleMenubackground.gif",glyphMenuImages,"Glyph Menu")
      glyphMenu.numPad=True
      glyphMenu.background.rect=(0,300,200,200)
      player.currentMenu=glyphMenu
      self.lightning.rect=(500,350,300,300)
      self.glyphGroup.add(self.lightning)

    elif name=="Missile":
	self.attack(self.player.battlePlayer,"Missile")
    elif name=="Heal":
      shuffle2D=[("Heal1",self.heal1btn),("Heal2",self.heal2btn),("Heal3",self.heal3btn),("Heal4",self.heal4btn),("Not",self.fire1btn),("Not",self.fire4btn),("Not",self.lightning3btn),("Not",self.lightning2btn)]
      shuffle(shuffle2D)
      glyphMenuOptions=[shuffle2D[0][0],shuffle2D[1][0],shuffle2D[2][0],shuffle2D[3][0],shuffle2D[4][0],shuffle2D[5][0],shuffle2D[6][0],shuffle2D[7][0]]
      glyphMenuImages=[shuffle2D[0][1],shuffle2D[1][1],shuffle2D[2][1],shuffle2D[3][1],shuffle2D[4][1],shuffle2D[5][1],shuffle2D[6][1],shuffle2D[7][1]]
      glyphMenu=Menu(glyphMenuOptions,self.player,IMG_PATH+"battleMenubackground.gif",glyphMenuImages,"Glyph Menu")
      glyphMenu.numPad=True
      glyphMenu.background.rect=(0,300,200,200)
      player.currentMenu=glyphMenu
      self.heal.rect=(500,350,300,300)
      self.glyphGroup.add(self.heal)
    #set glyph menu

  def checkGlyph(self,name):
    if name=="Fire1":
      if self.glyphOverlayGroup.has(self.fire1)==False:
        self.fire1.rect=self.fire.rect
        self.glyphOverlayGroup.add(self.fire1)
        #check if glyph is complete
        if self.glyphOverlayGroup.has([self.fire1,self.fire2,self.fire3,self.fire4])==True:
	  self.attack(self.player.battlePlayer,"Fire")
    elif name=="Fire2":
      if self.glyphOverlayGroup.has(self.fire2)==False:
	self.fire2.rect=self.fire.rect
        self.glyphOverlayGroup.add(self.fire2)
        if self.glyphOverlayGroup.has([self.fire1,self.fire2,self.fire3,self.fire4])==True:
	  self.attack(self.player.battlePlayer,"Fire")
    elif name=="Fire3":
      if self.glyphOverlayGroup.has(self.fire3)==False:
	self.fire3.rect=self.fire.rect
        self.glyphOverlayGroup.add(self.fire3)
        if self.glyphOverlayGroup.has([self.fire2,self.fire1,self.fire3,self.fire4])==True:
	  self.attack(self.player.battlePlayer,"Fire")
    elif name=="Fire4":
      if self.glyphOverlayGroup.has(self.fire4)==False:
	self.fire4.rect=self.fire.rect
        self.glyphOverlayGroup.add(self.fire4)
        if self.glyphOverlayGroup.has([self.fire4,self.fire2,self.fire3,self.fire1])==True:
	  self.attack(self.player.battlePlayer,"Fire")
    elif name=="Heal1":
      if self.glyphOverlayGroup.has(self.heal1)==False:
	self.heal1.rect=self.heal.rect
        self.glyphOverlayGroup.add(self.heal1)
        if self.glyphOverlayGroup.has([self.heal1,self.heal2,self.heal3,self.heal4])==True:
	  self.attack(self.player.battlePlayer,"Heal")
    elif name=="Heal2":
      if self.glyphOverlayGroup.has(self.heal2)==False:
	self.heal2.rect=self.heal.rect
        self.glyphOverlayGroup.add(self.heal2)
        if self.glyphOverlayGroup.has([self.heal1,self.heal2,self.heal3,self.heal4])==True:
	  self.attack(self.player.battlePlayer,"Heal")
    elif name=="Heal3":
      if self.glyphOverlayGroup.has(self.heal3)==False:
	self.heal3.rect=self.heal.rect
        self.glyphOverlayGroup.add(self.heal3)
        if self.glyphOverlayGroup.has([self.heal1,self.heal2,self.heal3,self.heal4])==True:
	  self.attack(self.player.battlePlayer,"Heal")
    elif name=="Heal4":
      if self.glyphOverlayGroup.has(self.heal4)==False:
	self.heal4.rect=self.heal.rect
        self.glyphOverlayGroup.add(self.heal4)
        if self.glyphOverlayGroup.has([self.heal1,self.heal2,self.heal3,self.heal4])==True:
	  self.attack(self.player.battlePlayer,"Heal")
    elif name=="Lightning1":
      if self.glyphOverlayGroup.has(self.lightning1)==False:
	self.lightning1.rect=self.lightning.rect
        self.glyphOverlayGroup.add(self.lightning1)
        if self.glyphOverlayGroup.has([self.lightning1,self.lightning2,self.lightning3,self.lightning4])==True:
	  self.attack(self.player.battlePlayer,"Lightning")
    elif name=="Lightning2":
      if self.glyphOverlayGroup.has(self.lightning2)==False:
	self.lightning2.rect=self.lightning.rect
        self.glyphOverlayGroup.add(self.lightning2)
        if self.glyphOverlayGroup.has([self.lightning1,self.lightning2,self.lightning3,self.lightning4])==True:
	  self.attack(self.player.battlePlayer,"Lightning")
    elif name=="Lightning3":
      if self.glyphOverlayGroup.has(self.lightning3)==False:
	self.lightning3.rect=self.lightning.rect
        self.glyphOverlayGroup.add(self.lightning3)
        if self.glyphOverlayGroup.has([self.lightning1,self.lightning2,self.lightning3,self.lightning4])==True:
	  self.attack(self.player.battlePlayer,"Lightning")
    elif name=="Lightning4":
      if self.glyphOverlayGroup.has(self.lightning4)==False:
	self.lightning4.rect=self.lightning.rect
        self.glyphOverlayGroup.add(self.lightning4)
        if self.glyphOverlayGroup.has([self.lightning1,self.lightning2,self.lightning3,self.lightning4])==True:
	  self.attack(self.player.battlePlayer,"Lightning")

  ###
  #uses an item in the player's equipped item list
  ###
  def useItem(self,item):
    if item.type=="Usable":
      self.player.battlePlayer.HP+=int(self.player.battlePlayer.MHP*item.power)
      self.player.battlePlayer.eqItem.remove(item)
      self.player.battlePlayer.eqItem.append(Item("",""))
    self.playerTurn=False
    self.player.currentMenu=self.battleMenu

  def decrementBonus(self):
    self.timeBonus-=.05
    if self.timeBonus==0:
      pygame.time.set_timer(USEREVENT+1,0)
  ###
  #Returns a list of attacks for any player or enemy passed in
  ###
  def ListAttacks(self,char):
    return char.avaliableAttacks()

  #checks the fraction sum, close to 1 results in a division attack, over 1 is a miss
  def checkFraction(self):
    if player.battlePlayer.fractionSum > .98 and player.battlePlayer.fractionSum < 1.01:
      player.migrateMessages("Fraction correct!")
      self.attack(self.player.battlePlayer,"Division")
      
    elif player.battlePlayer.fractionSum > 1.01:
      self.player.migrateMessages("Fraction sum incorrect")
      self.playerTurn=False
      self.player.currentMenu=self.battleMenu	
      self.player.battlePlayer.fractionSum=0
      

  def divisionAttack(self):
    self.player.battlePlayer.fractionSum=0
    self.player.currentMenu=self.divisionMenu
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

  def TimerEpxire(self):
    print "The bonus time is up"
    #Change timer GUI bar color????

  ###
  #Picks an attack for the enemy to perform. 
  # takes in which enemy is attacking.
  ###
  def GenerateEnemyAttack(self,enemy):

    #determines which attack the enemy should use by finding a random int b/w
    #1-100 and using that to pick an attack in attackPower.
    seed()
    temp = randint(1,100)
    defender=self.player.battlePlayer

    if temp < 6:
      defender.defendAttack(enemy.attackPower("critical"))
      player.migrateMessages("Enemy critical attacks for "+repr(enemy.attackPower("critical"))+" damage")
    elif temp > 90:
      defender.defendAttack(enemy.attackPower("special"))
    #print special message differently depending on name
    if enemy.name == "Wizard":
      player.migrateMessages("Enemy casts Divide By Zero, and blasts you for "+repr(enemy.attackPower("special"))+" damage")
    elif enemy.name == "Goblin" or enemy.name == "Orc":
      player.migrateMessages("Enemy head bonks you for "+repr(enemy.attackPower("special"))+" damage. Ouch!")
    #TODO: add enemy types here as levels are added
    else:
      player.migrateMessages("Enemy attacks for "+repr(enemy.attackPower("basic"))+" damage")
      defender.defendAttack(enemy.attackPower("basic"))
    self.playerTurn=True

  ###
  #the value generated by enemies in current battle
  ###
  def checkValue(self):
    return self.enemyValue
  ###
  #Called when battle is over and player wins
  ##
  def Victory(self):
    self.battleItems=["Items Won: "]
    if type(player.currentRoom.it1)==type(Item("","")) and player.currentRoom.it1.battle:
      player.battlePlayer.inv_Ar.append(player.currentRoom.it1)
      self.battleItems.append(player.currentRoom.it1.name)
      player.currentRoom.it1=0
    if type(player.currentRoom.it2)==type(Item("","")) and player.currentRoom.it2.battle:
      self.battleItems.append(player.currentRoom.it2.name)
      player.battlePlayer.inv_Ar.append(player.currentRoom.it2)
      player.currentRoom.it2=0
    if type(player.currentRoom.it3)==type(Item("","")) and player.currentRoom.i3.battle:
      self.battleItems.append(player.currentRoom.it3.name)
      player.battlePlayer.inv_Ar.append(player.currentRoom.it3)
      player.currentRoom.it3=0
    if type(player.currentRoom.it4)==type(Item("","")) and player.currentRoom.it4.battle:
      self.battleItems.append(player.currentRoom.it4.name)
      player.battlePlayer.inv_Ar.append(player.currentRoom.it4)
      player.currentRoom.it4=0
    print(self.battleItems)
    self.player.currentRoom.en1=0
    self.player.currentRoom.en2=0
    self.player.currentRoom.en3=0
    self.player.currentRoom.en4=0
    victoryMenu=Menu(["Continue"],self.player,IMG_PATH+"VictoryScreen.gif",[IMG_PATH+"Blank.gif"],"Victory")
    self.player.battle=False
    self.player.mainMenu=True
    self.player.currentMenu=victoryMenu

  ###
  #Called when battle is over and player loses
  ###
  def Defeat(self):
    #self.player.defeatScreen=True
    self.player.battle=False
    defeatMenu=Menu(["LoseContinue","LoseExit"],self.player,IMG_PATH+"VictoryScreen.gif",[IMG_PATH+"Blank.gif",IMG_PATH+"Blank.gif"],"Defeat")
    self.player.currentMenu=defeatMenu
    self.player.mainMenu=True	

  def bringOutYerDead(self,enemies):
    for enemy in enemies:
      if enemy.HP<=0:
        if enemy.place==0:
          self.player.currentRoom.en1='0'
        elif enemy.place==1:
          self.player.currentRoom.en2='0'
        elif enemy.place==2:
          self.player.currentRoom.en3='0'
        elif enemy.place==3:
          self.player.currentRoom.en4='0'
        self.selEnemyIndex=0
        if enemy.name=="Gru":
          self.enemyValue+=50
        elif enemy.name=="Wizard":
          self.enemyValue+=150
        elif enemy.name=="Goblin":
          self.enemyValue+=50

        enemies.remove(enemy)
    return enemies
  ###
  #Checks if the battle is over
  ###
  def CheckEndBattle(self):
    if player.battlePlayer.HP <= 0:
      self.Defeat()

    else:
	allDead = True
	for enem in self.enemies:
	    if enem.HP > 0:
	      allDead = False
	for i in range(3):
          self.enemies=self.bringOutYerDead(self.enemies)

	if allDead == True:
          self.Victory()

###
# Run updates the battle and keeps things progressing
##
  def Run(self,event,screen):
#Insert logic that updates the battle here

    #If player turn, wait for player to select attack then start timer
    if self.playerTurn==True:
      if event.type == QUIT:
        sys.exit()
      elif event.type==USEREVENT+1:
        self.decrementBonus()
        self.draw(self.player,screen)
      #handle key input
      elif event.type == KEYDOWN:
        newKey=pygame.key.name(event.key)

        if newKey=='escape':
          sys.exit()

        elif newKey=='[6]' or newKey=='right':
          #Right
          if player.currentMenu.numPad==True:
              player.currentMenu.select("down")
          else:
            if self.selEnemyIndex<len(self.enemies)-1:
              self.selEnemyIndex+=1
            else:
              self.selEnemyIndex=len(self.enemies)-1

        elif newKey=='[2]' or newKey=='down':
          #Down
          if player.currentMenu.name=="Number Pad":
            for i in range(3):
              player.currentMenu.select("down")
          elif player.currentMenu.name=="GeomTut3" or player.currentMenu.name=="Glyph Menu":
            for i in range(2):
              player.currentMenu.select("down")
          else:
            player.currentMenu.select("down")

        elif newKey=='[4]' or newKey=='left':
          #Left
          if player.currentMenu.numPad==True:
            player.currentMenu.select('up')
          else:
            if self.selEnemyIndex>0:
              self.selEnemyIndex-=1
            else:
              self.selEnemyIndex=0
        elif newKey=='[8]' or newKey=='up':
          #Up
          if player.currentMenu.name=="Number Pad":
            for i in range(3):
              player.currentMenu.select("up")
          elif player.currentMenu.name=="GeomTut3" or player.currentMenu.name=="Glyph Menu":
            for i in range(2):
              player.currentMenu.select("up")
          else:
            player.currentMenu.select("up")
          
        elif newKey=='[1]' or newKey=='return':
          #Check
          player.currentMenu.progress(player,screen)

        elif newKey=='[7]':
          #Square
          msg5='square'

        elif newKey=='[9]':
          msg5='circle'
      self.CheckEndBattle()
    else: 
      #print("Easy Mode")
      #self.playerTurn=True
      for enemy in self.enemies:
        self.GenerateEnemyAttack(enemy)
      #if enemy turn, randomly select enemy attack using GenerateEnemeyAttack() and attack

    #Run a check to see if battle is over
      self.CheckEndBattle()

