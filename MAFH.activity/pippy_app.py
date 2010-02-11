import pippy, pygame, sys, math
from pygame.locals import *
from sugar.activity import activity
from time import time
import os.path
from random import *

from Items import get_item, Item
from Enemy import get_enemy, Enemy
from Hero import Hero
from Dungeon import Dungeon
from Puzzle import PuzzlePiece, PuzzleMap
from Comic import Comic
from Menu import Menu
from Map import Map
################################################################################
#Start of external classes and functions
###############################################################################

from constants import (
    BASE_PATH, SOUND_PATH, MAP_PATH, MENU_PATH, HUD_PATH, ENV_PATH,
    PUZZLE_PATH, FMC_PATH, TOUR_PATH, CHAR_PATH
)

#       STAT COLLECTION
#       for each difficulty, track each correct and incorrect for each attack
#       geometry attack, division, critical, shop purchases/sales, puzzle solve times/quits

################################################################################

# Player Class: stores info about the player ie. current position in dungeon etc

#########################################################################
class Player:
  ####LOADS EVERYTHING FOR THE GAME####
  def __init__(self,x=0,y=0):
    NORTH=1
    SOUTH=3
    EAST=0
    WEST=2
   
    self.dgn = None
    self.theme=None
    self.initializeMenu()
    self.currentX=x
    self.currentY=y
    self.battlePlayer=Hero(self)
    #Difficulty: 1=Easy 2=Meduim 3=Hard
    self.critDifficulty=2 
    self.divDifficulty=2
    self.geomDifficulty=2
    self.shopDifficulty=2

    #Player stats
    self.name=""  #player name: to be set in options menu or upon new game (character select screen?)
    self.multiplicationStats=[(0,0),(0,0),(0,0)]   #[easy problems,medium problems,hard problems]
    self.divisionStats=[(0,0),(0,0),(0,0)]        #[easy problems,medium problems,hard problems]
    self.geometryStats=[(0,0),(0,0),(0,0)]            #[easy,medium, hard]
    self.shopStats=[(0,0),(0,0),(0,0)]            #[spent too much money,didn't give enough money, game exact amount]
    self.puzzlesSolved=0

    self.curBattle=BattleEngine(self.battlePlayer,[None])
    self.movTutorial=False
    self.movTutorial2=False
    self.movTutorial3=False
    self.hpTutorial=False
    self.hiddenTutorial=False
    self.battleTutorial=False
    self.puzzleTutorial=False
    self.lockTutorial=False
    self.invTutorial=False
    self.shopTutorial=False
    self.itemsPickedUp=False

    #state variables
    self.inTutorial=False
    self.mainMenu=True
    self.traversal=False
    self.waiting=False
    self.battle=False
    self.inGameTutorial=False
    self.macroMap=False
    self.shop=False
    self.inComic=False
    self.inPuzzle=False

    self.msg1=""
    self.msg2=""
    self.msg3=""
    self.msg4=""
    self.msg5=""

    self.playerFacing=NORTH

    #sound
    self.comic=None
    pygame.mixer.init()
    self.doorEffect=pygame.mixer.Sound(SOUND_PATH+"door.wav")
    self.doorEffect.set_volume(.25)
    self.basicAtk=pygame.mixer.Sound(SOUND_PATH+"basicAtk.ogg")
    self.basicAtk.set_volume(.5)
    self.magicAtk=pygame.mixer.Sound(SOUND_PATH+"fireAtk.ogg")
    self.magicAtk.set_volume(.5)
    self.specialAtk=pygame.mixer.Sound(SOUND_PATH+"specialAtk.ogg")
    self.specialAtk.set_volume(.5)
    self.enemyDie=pygame.mixer.Sound(SOUND_PATH+"enemyDie1.ogg")
    self.enemyDie.set_volume(1)
    self.itemPickup=pygame.mixer.Sound(SOUND_PATH+"itemPickup.ogg")
    self.itemPickup.set_volume(.4)
    self.buySell=pygame.mixer.Sound(SOUND_PATH+"buySell.ogg")
    self.buySell.set_volume(.5)

  def toString(self):
    dataList=[]
    dataList.append(self.name)
    dataList.append(self.dgnIndex)
    dataList.append(self.critDifficulty)
    dataList.append(self.divDifficulty)
    dataList.append(self.geomDifficulty)
    dataList.append(self.shopDifficulty)
    dataList.append(self.multiplicationStats)
    dataList.append(self.divisionStats)
    dataList.append(self.geometryStats)
    dataList.append(self.shopStats)
    dataList.append(self.puzzlesSolved)
    dataList.append(self.battlePlayer.MHP)
    dataList.append(self.battlePlayer.HP)
    for item in self.battlePlayer.inv_Ar:
      dataList.append(item.id)
    dataList.append('End Inventory')
    for item in self.battlePlayer.eqItem:
      if item==None:
        dataList.append(item)
      else:
        dataList.append(item.id)
    dataList.append('End Equip')
    if self.battlePlayer.weapon==None:
      dataList.append(None)
    else:
      dataList.append(self.battlePlayer.weapon.id)
    if self.battlePlayer.armor==None:
      dataList.append(None)
    else:
      dataList.append(self.battlePlayer.armor.id)
    if self.battlePlayer.accessory==None:
      dataList.append(None)
    else:
      dataList.append(self.battlePlayer.accessory.id)
    dataList.append(self.battlePlayer.akhal)
    return(dataList)

  def initializeMenu(self):
    mafh_splashBG=MENU_PATH+"mafh_splash.gif"
    menuElementBG=[MENU_PATH+"TitleButton.gif"]

    adventureMenuOptions=["Continue","Load Game","New Game","Return to Title"]
    adventureMenu=Menu(adventureMenuOptions,self,mafh_splashBG,[MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif"],"Adventure Play")

    creativeMenuOptions=["Play Custom Map","New Custom Map","Share Map","Return to Title"]
    creativeMenu=Menu(creativeMenuOptions,self,mafh_splashBG,[MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif"],"Creative Play")

    networkMenuOptions=["Local Cooperative Play","Local Treasure Trekkers Play","View Scoreboards","Return to Title"]
    networkMenu=Menu(networkMenuOptions,self,mafh_splashBG,[MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif"],"Network Play")

    extrasMenuOptions=["View Awards","View Statistics","Return to Title"]
    extrasMenu=Menu(extrasMenuOptions,self,mafh_splashBG,[MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif"],"Extras")
	
    difficultyMenuOptions=["ON","OFF"]
    difficultyMenu=Menu(difficultyMenuOptions,self,mafh_splashBG,[MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif"],"Difficulty Menu")

    optionsMenuOptions=[difficultyMenu,difficultyMenu,difficultyMenu,difficultyMenu,"Return to Title"]
    optionsMenu=Menu(optionsMenuOptions,self,mafh_splashBG,[MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif"],"Options Menu")

    self.MainMenu=Menu(["Controls",adventureMenu,creativeMenu,networkMenu,extrasMenu,optionsMenu,"Exit Game"],self,mafh_splashBG,[MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif",MENU_PATH+"TitleButton.gif"],"Title Menu")

    statMenuOptions=["Weapon","Armor","Accessory"]
    statMenuImages=[MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif"]
    self.statsMenu=Menu(statMenuOptions,self,MENU_PATH+"PauseMenuBackground.gif",statMenuImages,"Stats")
    self.statsMenu.background.rect.top=10

    pauseMenuOptions=["Save","Close","Main Menu","Return to Game"]
    pauseMenuImages=[MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif"]
    self.pauseMenu=Menu(pauseMenuOptions,self,MENU_PATH+"VictoryScreen.gif",pauseMenuImages,"Pause Menu")
    self.pauseMenu.background.rect.top=11

    self.mathStats=Menu([],self,MENU_PATH+"VictoryScreen.gif",[],"Math Stats")
    self.mathStats.background.rect.top=11

    self.currentMenu=self.MainMenu
    self.previousMenu=self.MainMenu

  def loadImages(self,theme):
    LVL_PATH=ENV_PATH
    if theme==1:
      LVL_PATH=ENV_PATH+"Ice/"
      pygame.mixer.music.load(SOUND_PATH+"Ice.ogg")
      pygame.mixer.music.play(-1)
    elif theme==2:
      LVL_PATH=ENV_PATH+"Fire/"
    else:
      pygame.mixer.music.load(SOUND_PATH+"MAFHbg.ogg")
      pygame.mixer.music.play(-1)
    self.itemsGroup=pygame.sprite.Group()

    self.currentRoomSprite=pygame.sprite.Sprite()
    self.currentRoomSprite.image=pygame.image.load(ENV_PATH+"Black.gif")
    self.currentRoomSprite.rect=pygame.Rect(0,0,1200,700)

    self.Black=pygame.sprite.Sprite()
    self.Black.image=pygame.image.load(ENV_PATH+"Black.gif")
    self.Black.rect=pygame.Rect(0,0,1200,700)

    self.FLRSprite=pygame.sprite.Sprite()
    self.FLRSprite.image=pygame.image.load(LVL_PATH+"flr.gif")
    self.FLRSprite.rect=self.currentRoomSprite.rect

    self.FRSprite=pygame.sprite.Sprite()
    self.FRSprite.image=pygame.image.load(LVL_PATH+"fr.gif")
    self.FRSprite.rect=self.currentRoomSprite.rect

    self.FSprite=pygame.sprite.Sprite()
    self.FSprite.image=pygame.image.load(LVL_PATH+"f.gif")
    self.FSprite.rect=self.currentRoomSprite.rect

    self.FLSprite=pygame.sprite.Sprite()
    self.FLSprite.image=pygame.image.load(LVL_PATH+"fl.gif")
    self.FLSprite.rect=self.currentRoomSprite.rect

    self.LRSprite=pygame.sprite.Sprite()
    self.LRSprite.image=pygame.image.load(LVL_PATH+"lr.gif")
    self.LRSprite.rect=self.currentRoomSprite.rect

    self.LSprite=pygame.sprite.Sprite()
    self.LSprite.image=pygame.image.load(LVL_PATH+"l.gif")
    self.LSprite.rect=self.currentRoomSprite.rect

    self.NoSprite=pygame.sprite.Sprite()
    self.NoSprite.image=pygame.image.load(LVL_PATH+"_.gif")
    self.NoSprite.rect=self.currentRoomSprite.rect

    self.RSprite=pygame.sprite.Sprite()
    self.RSprite.image=pygame.image.load(LVL_PATH+"r.gif")
    self.RSprite.rect=self.currentRoomSprite.rect
    
    self.akhalSprite=pygame.sprite.Sprite()
    self.akhalSprite.image=pygame.image.load(MENU_PATH+"akhal.gif")
    self.akhalSprite.rect=pygame.Rect(0,0,50,50)

    divSwordImg=pygame.sprite.Sprite()
    divSwordImg.image=pygame.image.load(MENU_PATH+"DivSword.gif")
    divSwordImg.rect=(500,300,137,300)
    self.divSword=pygame.sprite.Group(divSwordImg)

    self.currentRoomGroup=pygame.sprite.Group(self.currentRoomSprite)
  def fromData(self,data):
    self.name=data[0]
    self.dgnIndex=data[1]-1
    ##FIXME: nextDungeon now uses file name not by id
    self.nextDungeon()
    self.critDifficulty=data[2]
    self.divDifficulty=data[3]
    self.geomDifficulty=data[4]
    self.shopDifficulty=data[5]
    self.multiplicationStats=data[6]
    self.divisionStats=data[7]
    self.geometryStats=data[8]
    self.shopStats=data[9]
    self.puzzlesSolved=data[10]
    self.battlePlayer.MHP=data[11]
    self.battlePlayer.HP=data[12]
    i=13
    self.battlePlayer.inv_Ar=[]
    while data[i]!= 'End Inventory':
      self.battlePlayer.inv_Ar.append(get_item(data[i]))
      i+=1
    i+=1
    line=data[i]
    j=0
    while data[i]!='End Equip':
      if data[i]==None:
        self.battlePlayer.eqItem[j]=None
      else:
        self.battlePlayer.eqItem[j]=get_item(data[i])
      i+=1
      j+=1

    i+=1
    if data[i]==None:
      self.battlePlayer.weapon=None
    else:
      self.battlePlayer.weapon=get_item(data[i])
    i+=1
    if data[i]==None:
      self.battlePlayer.armor=None
    else:
      self.battlePlayer.armor=get_item(data[i])
    i+=1
    if data[i]==None:
      self.battlePlayer.accessory=None
    else:
      self.battlePlayer.accessory=get_item(data[i])
    i+=1
    self.battlePlayer.akhal=data[i]

    
  def startComic(self,comicPath,soundPath):
    self.comic=Comic(comicPath,soundPath)
    self.inComic=True
    self.traversal=False
    self.mainMenu=False
  def stopComic(self):
    self.inComic=False
    del self.comic
    if self.inTutorial:
      self.mainMenu=True
      self.inTutorial=False
    else:
      self.traversal=True
    if self.traversal:
      self.nextDungeon()
      self.loadImages(self.dgn.theme)
      self.dgnMap.updateMacro(self)
      self.battlePlayer=Hero(self)
      setImage(player)
      pygame.display.flip()

  def migrateMessages(self,msg):
    self.msg1=self.msg2
    self.msg2=self.msg3
    self.msg3=self.msg4
    self.msg4=self.msg5
    self.msg5=msg
  def nextDungeon(self,reload=False):
      self.battlePlayer.MHP+=2
      self.dgnIndex+=1
      for item in self.battlePlayer.inv_Ar:
        if item.type=="key":
          self.battlePlayer.inv_Ar.remove(item)
      if reload:
          self.dgn=Dungeon(self.dgn.fileName)
      elif self.dgn:
          self.dgn=Dungeon(self.dgn.next)
      else:
          self.dgn=Dungeon('al1.txt')
      if self.dgn.theme != self.theme:
        self.loadImages(self.dgn.theme)
        self.theme=self.dgn.theme
      self.currentX=self.dgn.start[0]
      self.currentY=self.dgn.start[1]
      self.currentRoom=self.dgn.rooms.get((self.currentX,self.currentY))
      self.dgnMap=Map(self.dgn)
      self.currentRoom=self.dgn.rooms.get((self.currentX,self.currentY))

  def initInGameBattleTutorial(self,screen):
    batImages=[MENU_PATH+"Attack.gif",MENU_PATH+"Special.gif",MENU_PATH+"Magic.gif",MENU_PATH+"Blank.gif"]
    batBg=MENU_PATH+"battleMenubackground.gif"
    batBgRect=(0,300,400,400)
    numPadImages=[MENU_PATH+"1.gif",MENU_PATH+"2.gif",MENU_PATH+"3.gif",MENU_PATH+"4.gif",MENU_PATH+"5.gif",MENU_PATH+"6.gif",MENU_PATH+"7.gif",MENU_PATH+"8.gif",MENU_PATH+"9.gif",MENU_PATH+"0.gif",MENU_PATH+"Clear.gif",MENU_PATH+"Enter.gif"]
    geomImages=[MENU_PATH+"Fire.gif",MENU_PATH+"Lightning.gif",MENU_PATH+"Missile.gif",MENU_PATH+"Heal.gif"]
    itemMenuOption=["Wrong","Wrong","Wrong",self.curBattle.battleMenu]
    itemMenu=Menu(itemMenuOption,self,batBg,batImages,"ItemTut")
    itemMenu.background.rect=batBgRect
    geomMenu3Option=[itemMenu,itemMenu,itemMenu,itemMenu,itemMenu,itemMenu,itemMenu,itemMenu]
    geomMenu3=Menu(geomMenu3Option,self,batBg,[PUZZLE_PATH+"FireGlyph1btn.gif",PUZZLE_PATH+"FireGlyph2btn.gif",PUZZLE_PATH+"HealGlyph1btn.gif",PUZZLE_PATH+"FireGlyph3btn.gif",PUZZLE_PATH+"LightningGlyph1btn.gif",PUZZLE_PATH+"FireGlyph4btn.gif",PUZZLE_PATH+"HealGlyph3btn.gif",PUZZLE_PATH+"MissileGlyph2btn.gif"],"GeomTut3")
    geomMenu3.background.rect=batBgRect
    geomMenu3.numPad=True
    geomMenu2Option=[geomMenu3,"Wrong","Wrong","Wrong"]
    geomMenu2=Menu(geomMenu2Option,self,batBg,geomImages,"GeomTut2")
    geomMenu2.background.rect=batBgRect
    geomMenuOption=["Wrong","Wrong",geomMenu2,"Wrong"]
    geomMenu=Menu(geomMenuOption,self,batBg,batImages,"GeomTut")
    geomMenu.background.rect=batBgRect
    divMenu2Option=[geomMenu,geomMenu,geomMenu,geomMenu]
    divMenu2=Menu(divMenu2Option,self,batBg,[MENU_PATH+"12Power.gif",MENU_PATH+"14Power.gif",MENU_PATH+"13Power.gif",MENU_PATH+"16Power.gif"],"DivTut2")
    divMenu2.background.rect=batBgRect
    divMenuOption=["Wrong",divMenu2,"Wrong","Wrong"]
    self.divMenu=Menu(divMenuOption,self,batBg,batImages,"DivTut")
    self.divMenu.background.rect=batBgRect
    critMenuOption=[self.divMenu,self.divMenu,self.divMenu,self.divMenu,self.divMenu,self.divMenu,self.divMenu,self.divMenu,self.divMenu,self.divMenu,self.divMenu,"Enter"]
    critMenu=Menu(critMenuOption,self,batBg,numPadImages,"CritTut")
    critMenu.numPad=True
    critMenu.background.rect=batBgRect
    atkMenuOption=[critMenu,"Wrong","Wrong","Wrong"]
    atkMenu=Menu(atkMenuOption,self,batBg,batImages,"AtkTut")
    atkMenu.background.rect=batBgRect
    self.currentMenu=atkMenu
    self.battleTutorial=True

  def initMovTutorial(self,screen):
    font=pygame.font.SysFont("cmr10",35,False,False)
    y=0
    screen.fill((255,255,255),(0,20,500,400))
    lines=["Welcome to the first","     Dungeon!","To look around:","  press the left or right arrows.","To move forward:","  press the up arrow","To check inventory or stats:","  Press space or "]
    screen.blit(pygame.image.load(TOUR_PATH+"button/"+"buttonO.gif"),(260,300,40,40))
    for message in lines:
      screen.blit(font.render(message,True,(0,200,0)),(0,20+y,200,300))
      y+=40
  def initMovTutorial3(self,screen):
    font=pygame.font.SysFont("cmr10",35,False,False)
    y=0
    screen.fill((255,255,255),(0,20,500,300))
    lines=["While you are navigating the","maze-like dungeon, you might","want to look at a map.","To display a large map:","  press M or "]
    screen.blit(pygame.image.load(TOUR_PATH+"button/"+"buttonL.gif"),(240,200,40,40))
    for message in lines:
      screen.blit(font.render(message,True,(0,200,0)),(0,20+y,200,300))
      y+=40
  def initMovTutorial2(self,screen):
    font=pygame.font.SysFont("cmr10",35,False,False)
    y=0
    screen.fill((255,255,255),(0,20,450,400))
    lines=["This room has an item in it!","To pick it up:","   press    or E","To use it once equipped","  press E or  ","  on the stats screen","To unequip an item:","  press U or","  on the stats screen"]
    screen.blit(pygame.image.load(TOUR_PATH+"button/"+"buttonV.gif"),(135,90,40,40))
    screen.blit(pygame.image.load(TOUR_PATH+"button/"+"buttonL.gif"),(200,190,40,40))
    screen.blit(pygame.image.load(TOUR_PATH+"button/"+"buttonO.gif"),(200,300,40,40))
    for message in lines:
      screen.blit(font.render(message,True,(0,200,0)),(0,20+y,200,300))
      y+=40
  def checkRoom(self):
    message=""
    found=False
    hidden=False
    if isinstance( self.currentRoom.it1, Item ):
      self.battlePlayer.inv_Ar.append(self.currentRoom.it1)
      message+=self.currentRoom.it1.name
      found=True
      if self.currentRoom.it1.hidden:
        hidden=True
      self.currentRoom.it1=0
    if isinstance( self.currentRoom.it2, Item):
      self.battlePlayer.inv_Ar.append(self.currentRoom.it2)
      message+=" and "+self.currentRoom.it2.name
      found=True
      if self.currentRoom.it2.hidden:
        hidden=True
      self.currentRoom.it2=0
    if isinstance( self.currentRoom.it3, Item):
      self.battlePlayer.inv_Ar.append(self.currentRoom.it3)
      message+=" and "+self.currentRoom.it3.name
      found=True
      if self.currentRoom.it3.hidden:
        hidden=True
      self.currentRoom.it3=0
    if isinstance(self.currentRoom.it4, Item):
      self.battlePlayer.inv_Ar.append(self.currentRoom.it4)
      message+=" and "+self.currentRoom.it4.name
      found=True
      if self.currentRoom.it4.hidden:
        hidden=True
      self.currentRoom.it4=0
    if hidden and found==False:
      message+="nothing"
    if hidden==True and self.hiddenTutorial==False:
      self.hiddenTutorial=True
      player.migrateMessages("You have found items in your search, try searching every room for items!")
    if hidden:
      message+=" discovered!"
      player.itemPickup.play()
    elif found:
      message+=" picked up"
      player.itemPickup.play()
    else:
      message="No items found"

    return(message)

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
        self.fire.image=pygame.image.load(PUZZLE_PATH+"FireGlyph.gif")
        self.fire1=pygame.sprite.Sprite()
        self.fire1.image=pygame.image.load(PUZZLE_PATH+"FireGlyph1.gif")
        self.fire1btn=PUZZLE_PATH+"FireGlyph1btn.gif"
        self.fire2=pygame.sprite.Sprite()
        self.fire2.image=pygame.image.load(PUZZLE_PATH+"FireGlyph2.gif")
        self.fire2btn=PUZZLE_PATH+"FireGlyph2btn.gif"
        self.fire3=pygame.sprite.Sprite()
        self.fire3.image=pygame.image.load(PUZZLE_PATH+"FireGlyph3.gif")
        self.fire3btn=PUZZLE_PATH+"FireGlyph3btn.gif"
        self.fire4=pygame.sprite.Sprite()
        self.fire4.image=pygame.image.load(PUZZLE_PATH+"FireGlyph4.gif")
        self.fire4btn=PUZZLE_PATH+"FireGlyph4btn.gif"

        self.lightning=pygame.sprite.Sprite()
	self.lightning.image=pygame.image.load(PUZZLE_PATH+"LightningGlyph.gif")
        self.lightning1btn=PUZZLE_PATH+"LightningGlyph1btn.gif"
        self.lightning1=pygame.sprite.Sprite()
	self.lightning1.image=pygame.image.load(PUZZLE_PATH+"LightningGlyph1.gif")
        self.lightning2btn=PUZZLE_PATH+"LightningGlyph2btn.gif"
        self.lightning2=pygame.sprite.Sprite()
	self.lightning2.image=pygame.image.load(PUZZLE_PATH+"LightningGlyph2.gif")
        self.lightning3btn=PUZZLE_PATH+"LightningGlyph3btn.gif"
        self.lightning3=pygame.sprite.Sprite()
	self.lightning3.image=pygame.image.load(PUZZLE_PATH+"LightningGlyph3.gif")
        self.lightning4btn=PUZZLE_PATH+"LightningGlyph4btn.gif"
        self.lightning4=pygame.sprite.Sprite()
	self.lightning4.image=pygame.image.load(PUZZLE_PATH+"LightningGlyph4.gif")

        self.missile=pygame.sprite.Sprite()
	self.missile.image=pygame.image.load(PUZZLE_PATH+"MissileGlyph.gif")
        self.missile1btn=PUZZLE_PATH+"MissileGlyph1btn.gif"
        self.missile1=pygame.sprite.Sprite()
	self.missile1.image=pygame.image.load(PUZZLE_PATH+"MissileGlyph1.gif")
        self.missile2btn=PUZZLE_PATH+"MissileGlyph2btn.gif"
        self.missile2=pygame.sprite.Sprite()
	self.missile2.image=pygame.image.load(PUZZLE_PATH+"MissileGlyph2.gif")
        self.missile3btn=PUZZLE_PATH+"MissileGlyph3btn.gif"
        self.missile3=pygame.sprite.Sprite()
	self.missile3.image=pygame.image.load(PUZZLE_PATH+"MissileGlyph3.gif")
        self.missile4btn=PUZZLE_PATH+"MissileGlyph4btn.gif"
        self.missile4=pygame.sprite.Sprite()
	self.missile4.image=pygame.image.load(PUZZLE_PATH+"MissileGlyph4.gif")

        self.heal=pygame.sprite.Sprite()
	self.heal.image=pygame.image.load(PUZZLE_PATH+"HealGlyph.gif")
        self.heal1btn=PUZZLE_PATH+"HealGlyph1btn.gif"
        self.heal1=pygame.sprite.Sprite()
	self.heal1.image=pygame.image.load(PUZZLE_PATH+"HealGlyph1.gif")
        self.heal2btn=PUZZLE_PATH+"HealGlyph2btn.gif"
        self.heal2=pygame.sprite.Sprite()
	self.heal2.image=pygame.image.load(PUZZLE_PATH+"HealGlyph2.gif")
        self.heal3btn=PUZZLE_PATH+"HealGlyph3btn.gif"
        self.heal3=pygame.sprite.Sprite()
	self.heal3.image=pygame.image.load(PUZZLE_PATH+"HealGlyph3.gif")
        self.heal4btn=PUZZLE_PATH+"HealGlyph4btn.gif"
        self.heal4=pygame.sprite.Sprite()
	self.heal4.image=pygame.image.load(PUZZLE_PATH+"HealGlyph4.gif")

	self.glyphGroup=pygame.sprite.Group()
	self.glyphOverlayGroup=pygame.sprite.Group()
        self.enemyValue=0
        i=0
	for enemy in self.enemies:
          if enemy:
            enemy.place=i
          i+=1
	self.player.msg5= "Enemies are present, prepare to fight."

  def initializeMenus(self,player):
    battleOptions=["Attack"]

    battleBackground=MENU_PATH+"battleMenubackground.gif"
    battleOptImg=[MENU_PATH+"Attack.gif"]
    if isinstance(player,Player) and player.divDifficulty>0:
      battleOptions.append("Division")
      battleOptImg.append(MENU_PATH+"Special.gif")
    if isinstance(player,Player) and player.geomDifficulty>0:
      battleOptions.append("Geometry")
      battleOptImg.append(MENU_PATH+"Magic.gif")
    battleOptions.append("Scan")
    battleOptImg.append(MENU_PATH+"Blank.gif")
    
    self.battleMenu=Menu(battleOptions,player,battleBackground,battleOptImg,"Battle")
    self.battleMenu.background.rect=(0,300,0,200)

    numOptArr = ["1","2","3","4","5","6","7","8","9","0","Clear","Enter Answer"]
    numBG=MENU_PATH+"battleMenubackground.gif"
    numOptImg=[MENU_PATH+"1.gif",MENU_PATH+"2.gif",MENU_PATH+"3.gif",MENU_PATH+"4.gif",MENU_PATH+"5.gif",MENU_PATH+"6.gif",MENU_PATH+"7.gif",MENU_PATH+"8.gif",MENU_PATH+"9.gif",MENU_PATH+"0.gif",MENU_PATH+"Clear.gif",MENU_PATH+"Enter.gif"]
    self.numPadMenu=Menu(numOptArr,player,numBG,numOptImg,"Number Pad")
    self.numPadMenu.background.rect=(0,300,200,200)
    self.numPadMenu.numPad=True

    magicOptions=["Fire","Lightning","Missile","Heal"]
    magicBackground=MENU_PATH+"battleMenubackground.gif"
    magicOptImg=[MENU_PATH+"Fire.gif",MENU_PATH+"Lightning.gif",MENU_PATH+"Missile.gif",MENU_PATH+"Heal.gif"]
    self.magicMenu=Menu(magicOptions,player,magicBackground,magicOptImg,"Magic Menu")
    self.magicMenu.background.rect=(0,300,200,200)
    if isinstance(player,Player):
      if player.divDifficulty==1:
        divisionOptions=["1/2","1/3","1/4","1/6"]
        divisionBackground=MENU_PATH+"battleMenubackground.gif"
        divisionOptImg=[MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif"]
        self.divisionMenu=Menu(divisionOptions,player,divisionBackground,divisionOptImg,"Division Menu")
        self.divisionMenu.background.rect=(0,300,200,200) 
      elif player.divDifficulty==2:
        denom1=randint(2,9)
        denom2=randint(2,9)
        denom3=randint(2,9)
        denom4=randint(2,9)
        denom1=randint(2,3)
        denom2=randint(4,5)
        denom3=randint(6,7)
        denom4=randint(8,9)
        divisionOptions=["1/"+repr(denom1),"1/"+repr(denom2),"1/"+repr(denom3),"1/"+repr(denom4)]
        divisionBackground=MENU_PATH+"battleMenubackground.gif"
        divisionOptImg=[MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif"]
        self.divisionMenu=Menu(divisionOptions,player,divisionBackground,divisionOptImg,"Division Menu")
        self.divisionMenu.background.rect=(0,300,200,200) 
      elif player.divDifficulty==3:
        denom1=randint(2,3)
        denom2=randint(4,5)
        denom3=randint(6,7)
        denom4=randint(8,9)
        num1=randint(1,2)
        num2=randint(3,4)
        num3=randint(1,2)
        num4=randint(3,4)
        divisionOptions=[repr(num1)+"/"+repr(denom1),repr(num2)+"/"+repr(denom2),repr(num3)+"/"+repr(denom3),repr(num4)+"/"+repr(denom4)]
        divisionBackground=MENU_PATH+"battleMenubackground.gif"
        divisionOptImg=[MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif"]
        self.divisionMenu=Menu(divisionOptions,player,divisionBackground,divisionOptImg,"Division Menu")
        self.divisionMenu.background.rect=(0,300,200,200) 


    self.player.currentMenu=self.battleMenu
    self.player.previousMenu=self.numPadMenu

  def draw(self,player,screen):
    #draw enemies
    font = pygame.font.Font(None, 36)
    x=250
    y=150
    enemyGroup=pygame.sprite.Group()
    i=0
    for enemy in self.enemies:
      enemy.sprite.rect=pygame.Rect((x+(enemy.place*200),y,200,200))
      if i==self.selEnemyIndex:
        sel=pygame.sprite.Sprite()
        sel.image=pygame.transform.scale(pygame.image.load(HUD_PATH+"arrow_select_b.gif"),(40,60))
        sel.rect=pygame.Rect(x+(enemy.place*200)+20,y+45,40,20)
        enemyGroup.add(sel)
      i+=1
      enemyGroup.add(enemy.sprite)

    player.currentRoomGroup.draw(screen)
    screen.blit(font.render("HP:",True,(0,0,0)),(5,10,40,40))
    screen.blit(pygame.transform.scale(pygame.image.load(HUD_PATH+"hp_"+repr(int(float(player.battlePlayer.HP)/float(player.battlePlayer.MHP)*10)*10)+".gif"),(150,150)),(50,5,50,50))
    enemyGroup.draw(screen)
    self.glyphGroup.draw(screen)
    self.glyphOverlayGroup.draw(screen)

    #draw player
    if player.currentMenu.numPad==False:
      player.currentMenu.battleDraw(player,screen,235,450,45)
          
      if player.currentMenu.name=="Division Menu" or player.currentMenu.name=="DivTut2":
        screen.fill((0,0,0),(500,300,100,400))
        screen.fill((255,150,0),(500,(620-310*player.battlePlayer.fractionSum),137,310*player.battlePlayer.fractionSum))
        y=460
        
        player.divSword.draw(screen)
    else:
      if player.currentMenu.name=="GeomTut3" or player.currentMenu.name=="Glyph Menu":
        player.currentMenu.battleDraw(player,screen,235,390,60)
      else:
        player.currentMenu.battleDraw(player,screen,235,450,40)
      if not player.battlePlayer.currentProb1=="":
        font = pygame.font.Font(None, 36)
        probText=font.render(repr(player.battlePlayer.currentProb1)+" X "+repr(player.battlePlayer.currentProb2),True,(255,255,255))
        inputText=font.render(player.battlePlayer.currentInput,True,(50,0,150))
        if player.currentMenu.name=="Number Pad" or player.currentMenu.name=="CritTut":
          screen.blit(probText,pygame.Rect(250,350,200,30))
          screen.blit(inputText,pygame.Rect(250,400,200,30))
      
      
      if self.timeBonus<1:
        screen.blit(pygame.transform.scale(pygame.image.load(HUD_PATH+"bt_"+repr(int(self.timeBonus*10)*10)+".gif"),(275,50)),(5,200,150,50))
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
    defender=self.enemies[self.selEnemyIndex]
    if attackName=="critical":
      attacker.setBonusAP(attacker.currentAnswer+int(self.timeBonus*10))
      if isinstance(defender,Enemy) and defender.weakness=='normal':
        attacker.setBonusAP(attacker.BAB*2)
      self.player.basicAtk.play()
      tup=self.player.multiplicationStats[self.player.critDifficulty-1]
      tup=(tup[0]+1,tup[1])
      self.player.multiplicationStats[self.player.critDifficulty-1]=tup
      player.migrateMessages("Crit"+repr(attacker.attackPower("critical")))
    elif attackName=="Fire":
      attacker.setBonusAP(int(self.timeBonus*20)+10)
      if isinstance(defender,Enemy) and defender.weakness=='fire':
        attacker.setBonusAP(attacker.BAB+50)
      self.glyphGroup.empty()
      self.glyphOverlayGroup.empty()
      self.player.currentMenu=self.battleMenu
      self.player.magicAtk.play()
      tup=self.player.geometryStats[self.player.geomDifficulty-1]
      tup=(tup[0]+1,tup[1])
      self.player.geometryStats[self.player.geomDifficulty-1]=tup

    elif attackName=="Heal":
      attacker.setBonusAP(-1*(int(self.timeBonus*20)+10))
      self.glyphGroup.empty()
      self.glyphOverlayGroup.empty()
      self.player.currentMenu=self.battleMenu
      tup=self.player.geometryStats[self.player.geomDifficulty-1]
      tup=(tup[0]+1,tup[1])
      self.player.geometryStats[self.player.geomDifficulty-1]=tup

    elif attackName=="Lightning":
      attacker.setBonusAP(int(self.timeBonus)+10)
      if isinstance(defender,Enemy) and defender.weakness=='lightning':
        attacker.setBonusAP(attacker.BAB+60)
      self.glyphGroup.empty()
      self.glyphOverlayGroup.empty()
      self.player.magicAtk.play()
      self.player.currentMenu=self.battleMenu
      tup=self.player.geometryStats[self.player.geomDifficulty-1]
      tup=(tup[0]+1,tup[1])
      self.player.geometryStats[self.player.geomDifficulty-1]=tup
    elif attackName=="Missile":
      attacker.setBonusAP(int(self.timeBonus)+10)
      if isinstance(defender,Enemy) and defender.weakness=='missile':
        attacker.setBonusAP(attacker.BAB+55)
      self.glyphGroup.empty()
      self.glyphOverlayGroup.empty()
      self.player.magicAtk.play()
      self.player.currentMenu=self.battleMenu
      tup=self.player.geometryStats[self.player.geomDifficulty-1]
      tup=(tup[0]+1,tup[1])
      self.player.geometryStats[self.player.geomDifficulty-1]=tup
      print("Missile")
    elif attackName=="Division":
      if isinstance(defender,Enemy) and defender.weakness=='special':
        attacker.setBonusAP(attacker.BAE+4)
      else:
        attacker.setBonusAP(0)
      self.player.currentMenu=self.battleMenu
      self.player.specialAtk.play()
      tup=self.player.divisionStats[self.player.divDifficulty-1]
      tup=(tup[0]+1,tup[1])
      self.player.divisionStats[self.player.divDifficulty-1]=tup

    else:
      self.player.basicAtk.play()
    pygame.time.set_timer(USEREVENT+1,0)
    self.timeBonus=1

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
    prob1=0
    prob2=0
    if player.critDifficulty==1:
      prob1=randint(0,6)
      prob2=randint(0,6)
    elif player.critDifficulty==2:
      prob1=randint(0,12)
      prob2=randint(0,12)
    elif player.critDifficulty==3:
      prob1=randint(0,24)
      prob2=randint(0,24)
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

      glyphMenu=Menu(glyphMenuOptions,self.player,MENU_PATH+"battleMenubackground.gif",glyphMenuImages,"Glyph Menu")
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

      glyphMenu=Menu(glyphMenuOptions,self.player,MENU_PATH+"battleMenubackground.gif",glyphMenuImages,"Glyph Menu")
      glyphMenu.numPad=True
      glyphMenu.background.rect=(0,300,200,200)
      player.currentMenu=glyphMenu
      self.lightning.rect=(500,350,300,300)
      self.glyphGroup.add(self.lightning)

    elif name=="Missile":
      shuffle2D=[("Missile1",self.missile1btn),("Missile2",self.missile2btn),("Missile3",self.missile3btn),("Missile4",self.missile4btn),("Not",self.lightning1btn),("Not",self.heal4btn),("Not",self.fire3btn),("Not",self.lightning3btn)]
      shuffle(shuffle2D)
      glyphMenuOptions=[shuffle2D[0][0],shuffle2D[1][0],shuffle2D[2][0],shuffle2D[3][0],shuffle2D[4][0],shuffle2D[5][0],shuffle2D[6][0],shuffle2D[7][0]]
      glyphMenuImages=[shuffle2D[0][1],shuffle2D[1][1],shuffle2D[2][1],shuffle2D[3][1],shuffle2D[4][1],shuffle2D[5][1],shuffle2D[6][1],shuffle2D[7][1]]

      glyphMenu=Menu(glyphMenuOptions,self.player,MENU_PATH+"battleMenubackground.gif",glyphMenuImages,"Glyph Menu")
      glyphMenu.numPad=True
      glyphMenu.background.rect=(0,300,200,200)
      player.currentMenu=glyphMenu
      self.missile.rect=(500,350,300,300)
      self.glyphGroup.add(self.missile)
    elif name=="Heal":
      shuffle2D=[("Heal1",self.heal1btn),("Heal2",self.heal2btn),("Heal3",self.heal3btn),("Heal4",self.heal4btn),("Not",self.fire1btn),("Not",self.fire4btn),("Not",self.lightning3btn),("Not",self.lightning2btn)]
      shuffle(shuffle2D)
      glyphMenuOptions=[shuffle2D[0][0],shuffle2D[1][0],shuffle2D[2][0],shuffle2D[3][0],shuffle2D[4][0],shuffle2D[5][0],shuffle2D[6][0],shuffle2D[7][0]]
      glyphMenuImages=[shuffle2D[0][1],shuffle2D[1][1],shuffle2D[2][1],shuffle2D[3][1],shuffle2D[4][1],shuffle2D[5][1],shuffle2D[6][1],shuffle2D[7][1]]

      glyphMenu=Menu(glyphMenuOptions,self.player,MENU_PATH+"battleMenubackground.gif",glyphMenuImages,"Glyph Menu")
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
    elif name=="Missile1":
      if self.glyphOverlayGroup.has(self.missile1)==False:
	self.missile1.rect=self.missile.rect
        self.glyphOverlayGroup.add(self.missile1)
        if self.glyphOverlayGroup.has([self.missile1,self.missile2,self.missile3,self.missile4])==True:
	  self.attack(self.player.battlePlayer,"Missile")
    elif name=="Missile2":
      if self.glyphOverlayGroup.has(self.missile2)==False:
	self.missile2.rect=self.missile.rect
        self.glyphOverlayGroup.add(self.missile2)
        if self.glyphOverlayGroup.has([self.missile1,self.missile2,self.missile3,self.missile4])==True:
	  self.attack(self.player.battlePlayer,"Missile")
    elif name=="Missile3":
      if self.glyphOverlayGroup.has(self.missile3)==False:
	self.missile3.rect=self.missile.rect
        self.glyphOverlayGroup.add(self.missile3)
        if self.glyphOverlayGroup.has([self.missile1,self.missile2,self.missile3,self.missile4])==True:
	  self.attack(self.player.battlePlayer,"Missile")
    elif name=="Missile4":
      if self.glyphOverlayGroup.has(self.missile4)==False:
	self.missile4.rect=self.missile.rect
        self.glyphOverlayGroup.add(self.missile4)
        if self.glyphOverlayGroup.has([self.missile1,self.missile2,self.missile3,self.missile4])==True:
	  self.attack(self.player.battlePlayer,"Missile")
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
    if item!=None and item.type=="Usable":
      self.player.battlePlayer.HP+=int(self.player.battlePlayer.MHP*item.power)
      self.player.battlePlayer.eqItem[self.player.battlePlayer.eqItem.index(item)]=None
      print(len(self.player.battlePlayer.eqItem))
      player.migrateMessages("You heal for "+repr(int(self.player.battlePlayer.MHP*item.power)))
      if self.player.battlePlayer.HP>self.player.battlePlayer.MHP:
        self.player.battlePlayer.HP=self.player.battlePlayer.MHP
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
      tup=self.player.divisionStats[self.player.divDifficulty-1]
      tup=(tup[0],tup[1]+1)
      self.player.divisionStats[self.player.divDifficulty-1]=tup
      

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
  # Scans an enemy's HP and weaknesses
  ###	
  def scanEnemy(self):
    player.migrateMessages("Remaining HP: "+repr(self.enemies[self.selEnemyIndex].HP))
    player.migrateMessages("Enemy Weakness: "+repr(self.enemies[self.selEnemyIndex].weakness))
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

    if temp > 90:
      defender.defendAttack(enemy.attackPower("special"))
      player.migrateMessages("Enemy "+repr(enemy.name)+" "+repr(enemy.place)+" special attacks for "+repr(enemy.attackPower("special"))+" damage")
    #print special message differently depending on name
    elif temp < 6 and enemy.name == "Wizard":
      defender.defendAttack(enemy.attackPower("critical"))
      player.migrateMessages("Wizard "+repr(enemy.place)+" casts Divide By Zero, and blasts you for "+repr(enemy.attackPower("critical"))+" damage")
    elif temp < 6 and (enemy.name == "Goblin" or enemy.name == "Orc"):
      defender.defendAttack(enemy.attackPower("critical"))
      player.migrateMessages(enemy.name + repr(enemy.place)+ " head bonks you for " +repr(enemy.attackPower("critical"))+" damage. Ouch!")
    elif temp < 6:
      defender.defendAttack(enemy.attackPower("critical"))
      player.migrateMessages("Enemy "+repr(enemy.name)+" "+repr(enemy.place)+" critical attacks for "+repr(enemy.attackPower("critical"))+" damage")
    #TODO: add enemy types here as levels are added
    else:
      player.migrateMessages(repr(enemy.name)+" "+repr(enemy.place)+" attacks for "+repr(enemy.attackPower("basic"))+" damage")
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
    if isinstance( player.currentRoom.it1, Item ) and player.currentRoom.it1.battle:
      player.battlePlayer.inv_Ar.append(player.currentRoom.it1)
      self.battleItems.append(player.currentRoom.it1.name)
      player.currentRoom.it1=0
    if isinstance( player.currentRoom.it2, Item ) and player.currentRoom.it2.battle:
      self.battleItems.append(player.currentRoom.it2.name)
      player.battlePlayer.inv_Ar.append(player.currentRoom.it2)
      player.currentRoom.it2=0
    if isinstance( player.currentRoom.it3, Item ) and player.currentRoom.i3.battle:
      self.battleItems.append(player.currentRoom.it3.name)
      player.battlePlayer.inv_Ar.append(player.currentRoom.it3)
      player.currentRoom.it3=0
    if isinstance( player.currentRoom.it4, Item ) and player.currentRoom.it4.battle:
      self.battleItems.append(player.currentRoom.it4.name)
      player.battlePlayer.inv_Ar.append(player.currentRoom.it4)
      player.currentRoom.it4=0
    print(self.battleItems)
    self.player.currentRoom.en1=0
    self.player.currentRoom.en2=0
    self.player.currentRoom.en3=0
    self.player.currentRoom.en4=0
    victoryMenu=Menu(["Continue"],self.player,MENU_PATH+"VictoryScreen.gif",[MENU_PATH+"Blank.gif"],"Victory")
    self.player.battle=False
    self.player.mainMenu=True
    self.player.currentMenu=victoryMenu

  ###
  #Called when battle is over and player loses
  ###
  def Defeat(self):
    #self.player.defeatScreen=True
    self.player.battle=False
    defeatMenu=Menu(["LoseContinue","LoseExit"],self.player,MENU_PATH+"VictoryScreen.gif",[MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif"],"Defeat")
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
        if enemy.name=="Orc":
          self.enemyValue+=50
        elif enemy.name=="Wizard Adept":
          self.enemyValue+=150
        elif enemy.name=="Goblin":
          self.enemyValue+=50
        self.player.enemyDie.play()
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
          if player.currentMenu.name=="Number Pad" or player.currentMenu.name=="CritTut":
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
          if player.currentMenu.name=="Number Pad" or player.currentMenu.name=="CritTut":
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


      self.CheckEndBattle()
    else: 
      #print("Easy Mode")
      #self.playerTurn=True
      for enemy in self.enemies:
        self.GenerateEnemyAttack(enemy)
      #if enemy turn, randomly select enemy attack using GenerateEnemeyAttack() and attack

    #Run a check to see if battle is over
      self.CheckEndBattle()

#############################################################################
#End External Classes
######################################################################

# always need to init first thing
pygame.init()

# turn off cursor
pygame.mouse.set_visible(False)

# XO screen is 1200x900
size = width, height = 1200, 900

font=pygame.font.Font(None,36)
# create the window and keep track of the surface
# for drawing into
screen = pygame.display.set_mode(size)

player=Player(0,0)

#state variables
player.inTutorial=False
player.traversal=False
player.waiting=False
player.battle=False
player.mainMenu=True


# Font.render draws text onto a new surface.
#
# usage: Font.render(text, antialias, color, bg=None)
tl1=font.render(player.msg1,True,(255,255,255))
tl2=font.render(player.msg2,True,(255,255,255))
tl3=font.render(player.msg3,True,(255,255,255))
tl4=font.render(player.msg4,True,(255,255,255))
tl5=font.render(player.msg5,True,(255,255,255))

# the Rect object is used for positioning
bigRect = pygame.Rect(300,700,800,200)

#textRect=text.get_rect()
line1=pygame.Rect(300,700,800,36)
line2=pygame.Rect(300,736,800,36)
line3=pygame.Rect(300,772,800,36)
line4=pygame.Rect(300,808,800,36)
line5=pygame.Rect(300,844,800,36)

# start at the top left
bigRect.left = 300
bigRect.top = 700
bigRect.width=1000
bigRect.height=300

#####Functions for main class######
def enterRoom(direction,player,screen):
    player.movTutorial=True
    NORTH=1
    SOUTH=3
    EAST=0
    WEST=2
    if direction=='north':
        player.currentY-=1
        player.playerFacing=NORTH

    elif direction=='south':
        player.currentY+=1
        player.playerFacing=SOUTH

    elif direction=='east':
        player.currentX+=1
        player.playerFacing=EAST

    elif direction=='west':
        player.currentX-=1
        player.playerFacing=WEST

    else:
        print(direction)

    player.currentRoom=player.dgn.rooms.get((player.currentX,player.currentY))
    player.doorEffect.play()

    player.currentRoomGroup.remove(player.currentRoomSprite)
    player.currentRoomSprite=player.Black
    player.currentRoomGroup.add(player.currentRoomSprite)
    player.currentRoomGroup.draw(screen)
    player.waiting=True
    player.dgnMap.updateMacro(player)

    return("You enter room at "+repr(player.currentX)+", "+repr(player.dgn.sizeY-player.currentY-1))

def setImage(player):
    fileName=""
    NORTH=1
    SOUTH=3
    EAST=0
    WEST=2
    player.itemsGroup.empty()
    emptySprite=pygame.sprite.Sprite()
    emptySprite.image=pygame.image.load(ENV_PATH+"noItem.gif")
    emptySprite.rect=pygame.Rect(700,300,50,50)
    sprites=[emptySprite,emptySprite,emptySprite,emptySprite]

    if isinstance( player.currentRoom.it1, Item ) and player.currentRoom.it1.hidden==False and player.currentRoom.it1.battle==False:
      itemSprite=pygame.sprite.Sprite()
      if player.currentRoom.it1.type=="Weapon":
        itemSprite.image=(pygame.image.load(ENV_PATH+"Weapon.gif"))
      elif player.currentRoom.it1.type=="Armor":
        itemSprite.image=(pygame.image.load(ENV_PATH+"Armor.gif"))
      else:
        itemSprite.image=(pygame.image.load(ENV_PATH+player.currentRoom.it1.name+".gif"))
      sprites[0]=itemSprite

    if isinstance( player.currentRoom.it2, Item ) and player.currentRoom.it2.hidden==False and player.currentRoom.it2.battle==False:
      itemSprite=pygame.sprite.Sprite()
      if player.currentRoom.it2.type=="Weapon":
        itemSprite.image=(pygame.image.load(ENV_PATH+"Weapon.gif"))
      elif player.currentRoom.it2.type=="Armor":
        itemSprite.image=(pygame.image.load(ENV_PATH+"Armor.gif"))
      else:
        itemSprite.image=(pygame.image.load(ENV_PATH+player.currentRoom.it2.name+".gif"))
      sprites[1]=itemSprite

    if isinstance( player.currentRoom.it3, Item ) and player.currentRoom.it3.hidden==False and player.currentRoom.it3.battle==False:
      itemSprite=pygame.sprite.Sprite()
      if player.currentRoom.it3.type=="Weapon":
        itemSprite.image=(pygame.image.load(ENV_PATH+"Weapon.gif"))
      elif player.currentRoom.it3.type=="Armor":
        itemSprite.image=(pygame.image.load(ENV_PATH+"Armor.gif"))
      else:
        itemSprite.image=(pygame.image.load(ENV_PATH+player.currentRoom.it3.name+".gif"))
      sprites[2]=itemSprite

    if isinstance( player.currentRoom.it4, Item ) and player.currentRoom.it4.hidden==False and player.currentRoom.it4.battle==False:
      itemSprite=pygame.sprite.Sprite()
      if player.currentRoom.it4.type=="Weapon":
        itemSprite.image=(pygame.image.load(ENV_PATH+"Weapon.gif"))
      elif player.currentRoom.it4.type=="Armor":
        itemSprite.image=(pygame.image.load(ENV_PATH+"Armor.gif"))
      else:
        itemSprite.image=(pygame.image.load(ENV_PATH+player.currentRoom.it4.name+".gif"))
      sprites[3]=itemSprite

    ###Set up string for testing
    if player.playerFacing==NORTH:
        if player.currentRoom.doorN:
            fileName+="F"

        if player.currentRoom.doorW:
            fileName+="L"

        if player.currentRoom.doorE:
            fileName+="R"
        #set item image positions #Maybe based on a random positioning in the room?
        sprites[0].rect=(700,300,50,50)
        sprites[1].rect=(780,300,50,50)
        sprites[2].rect=(850,300,50,50)
        sprites[3].rect=(900,300,50,50)

    elif player.playerFacing==SOUTH:
        if player.currentRoom.doorS:
            fileName+="F"

        if player.currentRoom.doorE:
            fileName+="L"

        if player.currentRoom.doorW:
            fileName+="R"
     
        sprites[0].rect=(1300,300,50,50)
        sprites[1].rect=(1300,300,50,50)
        sprites[2].rect=(1300,300,50,50)
        sprites[3].rect=(1300,300,50,50)

    elif player.playerFacing==EAST:
        if player.currentRoom.doorE:
            fileName+="F"

        if player.currentRoom.doorN:
            fileName+="L"

        if player.currentRoom.doorS:
            fileName+="R"

        sprites[0].rect=(180,380,50,50)
        sprites[1].rect=(200,350,50,50)
        sprites[2].rect=(210,330,50,50)
        sprites[3].rect=(240,300,50,50)

    elif player.playerFacing==WEST:
        if player.currentRoom.doorW:
            fileName+="F"

        if player.currentRoom.doorS:
            fileName+="L"

        if player.currentRoom.doorN:
            fileName+="R"

        sprites[0].rect=(1110,550,50,50)
        sprites[1].rect=(1130,580,50,50)
        sprites[2].rect=(1155,600,50,50)
        sprites[3].rect=(1160,650,50,50)

    ###set sprite depending on string
    player.currentRoomGroup.empty()

    if fileName=="F":
        player.currentRoomSprite=player.FSprite

    elif fileName=="FL":
        player.currentRoomSprite=player.FLSprite

    elif fileName=="FR":
        player.currentRoomSprite=player.FRSprite

    elif fileName=="FLR":
        player.currentRoomSprite=player.FLRSprite

    elif fileName=="LR":
        player.currentRoomSprite=player.LRSprite

    elif fileName=="L":
        player.currentRoomSprite=player.LSprite

    elif fileName=="R":
        player.currentRoomSprite=player.RSprite

    else:
        player.currentRoomSprite=player.NoSprite

    player.currentRoomGroup.add(player.currentRoomSprite)
    for sprite in sprites:
      player.itemsGroup.add(sprite)

def checkDoor(direction,player,screen):
    NORTH=1
    SOUTH=3
    EAST=0
    WEST=2

    NONE=-1
    PUZZLE=0
    LOCKED=1
    BOTH=2
    UNLOCKED=3
    EXIT=4
    ENTRANCE=5
    SHOP=6
    PUZZLEROOM=7
    HIDDEN=8

    currentX=player.currentX
    currentY=player.currentY
    playerFacing=player.playerFacing
    currentRoom=player.currentRoom

    if direction=='down': 
         print("down pressed")

    elif direction=='up':
         if playerFacing==NORTH:
            if currentRoom.doorN:
                if currentRoom.doorNFlag==EXIT:
                  for item in player.battlePlayer.inv_Ar:
                    if item.name=="Big Key":
                      player.battlePlayer.inv_Ar.remove(item)
                      player.nextDungeon()
                      return("You use the BIG KEY, and the door slams behind you")
                  return("This door is locked, you need a BIG KEY")
                elif currentRoom.doorNFlag==ENTRANCE:
                  player.migrateMessages("There is no turning back now")
                elif currentRoom.doorNFlag==LOCKED:
                  for item in player.battlePlayer.inv_Ar:
                    if item.name=="Small Key":
                      return("You use a SMALL KEY, "+enterRoom('north',player,screen))
                  return("This door is locked, you need a SMALL KEY")
                elif currentRoom.doorNFlag==PUZZLE or currentRoom.doorNFlag==BOTH:
                  startPuzzle(player)
                else:
                  player.itemsGroup.empty()
                  return(enterRoom('north',player,screen))

            else:
                return("There is no door in front of you")

         elif playerFacing==SOUTH:
            if currentRoom.doorS:
                if currentRoom.doorSFlag==EXIT:
                  for item in player.battlePlayer.inv_Ar:
                    if item.name=="Big Key":
                      player.battlePlayer.inv_Ar.remove(item)
                      player.nextDungeon()
                      return("You use the BIG KEY, and the door slams behind you")
                  return("This door is locked, you need a BIG KEY to exit")
                elif currentRoom.doorSFlag==ENTRANCE:
                  player.migrateMessages("There is no turning back now")
                elif currentRoom.doorSFlag==LOCKED:
                  for item in player.battlePlayer.inv_Ar:
                    if item.name=="Small Key":
                      return("You use a SMALL KEY, "+enterRoom('south',player,screen))
                  return("This door is locked, you need a SMALL KEY")
                elif currentRoom.doorSFlag==PUZZLE or currentRoom.doorSFlag==BOTH:
                  startPuzzle(player)
                else:
                  player.itemsGroup.empty()
                  return(enterRoom('south',player,screen))

            else:
                return("There is no door in front of you")

         elif playerFacing==EAST:
            if currentRoom.doorE:
                if currentRoom.doorEFlag==EXIT:
                  for item in player.battlePlayer.inv_Ar:
                    if item.name=="Big Key":
                      player.battlePlayer.inv_Ar.remove(item)
                      player.nextDungeon()
                      return("You use the BIG KEY, and the door slams behind you")
                  return("This door is locked, you need a BIG KEY to exit")
                elif currentRoom.doorEFlag==ENTRANCE:
                  player.migrateMessages("There is no turning back now")
                elif currentRoom.doorEFlag==LOCKED:
                  for item in player.battlePlayer.inv_Ar:
                    if item.name=="Small Key":
                      return("You use a SMALL KEY, "+enterRoom('east',player,screen))
                  return("This door is locked, you need a SMALL KEY")
                elif currentRoom.doorEFlag==PUZZLE or currentRoom.doorEFlag==BOTH:
                  startPuzzle(player)
                else:
                  player.itemsGroup.empty()
                  return(enterRoom('east',player,screen))

            else:
                return("There is no door in front of you")

         elif playerFacing==WEST:
            if currentRoom.doorW:
                if currentRoom.doorWFlag==EXIT:
                  for item in player.battlePlayer.inv_Ar:
                    if item.name=="Big Key":
                      player.battlePlayer.inv_Ar.remove(item)
                      player.nextDungeon()
                      return("You use the BIG KEY, and the door slams behind you")
                  return("This door is locked, you need a BIG KEY to exit")
                elif currentRoom.doorWFlag==ENTRANCE:
                  player.migrateMessages("There is no turning back now")
                elif currentRoom.doorWFlag==LOCKED:
                  for item in player.battlePlayer.inv_Ar:
                    if item.name=="Small Key":
                      return("You use a SMALL KEY, "+enterRoom('west',player,screen))
                  return("This door is locked, you need a SMALL KEY")
                elif currentRoom.doorWFlag==PUZZLE or currentRoom.doorWFlag==BOTH:
                  startPuzzle(player)
                else:
                  player.itemsGroup.empty()
                  return(enterRoom('west',player,screen))

            else:
                return("There is no door in front of you")

    elif direction=='left':
        if playerFacing==NORTH:
            player.playerFacing=WEST

            return('You are now facing West')

        elif playerFacing==SOUTH:
            player.playerFacing=EAST
            return('You are now facing East')

        elif playerFacing==EAST:
            player.playerFacing=NORTH
            #setImage(player)
            return('You are now facing North')

        elif playerFacing==WEST:
            player.playerFacing=SOUTH
            #setImage(player)
            return('You are now facing South')

    elif direction=='right':
        if playerFacing==NORTH:
            player.playerFacing=EAST
            #setImage(player)
            return('You are now facing East')

        elif playerFacing==SOUTH:
            player.playerFacing=WEST
            #setImage(player)
            return('You are now facing West')

        elif playerFacing==EAST:
            player.playerFacing=SOUTH
            setImage(player)
            return('You are now facing South')

        elif playerFacing==WEST:
            player.playerFacing=NORTH
            #setImage(player)
            return('You are now facing North')

    else:
        print(direction)
def startPuzzle(player):
  myMap=(["00","01"],["10","11"],["20","21"])

  x=-1
  y=-1
  for row in myMap:
    x+=1
    y=-1
    for item in row:
      y+=1
      myMap[x][y]=PuzzlePiece(x,y,x,y,PUZZLE_PATH+"Puz0-"+repr(x)+repr(y)+".gif")
   
  player.puzzle=PuzzleMap(myMap)
  player.puzzle.randomize()
  player.inPuzzle=True
  player.traversal=False
def stopPuzzle(player,solved):
  NORTH=1
  SOUTH=3
  EAST=0
  WEST=2

  NONE=-1
  PUZZLE=0
  LOCKED=1
  BOTH=2
  UNLOCKED=3
  EXIT=4
  ENTRANCE=5
  SHOP=6
  PUZZLEROOM=7
  HIDDEN=8

  if solved:
    player.puzzleTutorial=True
    if player.playerFacing==NORTH:
      if player.currentRoom.doorNFlag==PUZZLE:
        player.currentRoom.doorNFlag=UNLOCKED
      else:
        player.currentRoom.doorNFlag=LOCKED
    elif player.playerFacing==SOUTH:
      if player.currentRoom.doorSFlag==PUZZLE:
        player.currentRoom.doorSFlag=UNLOCKED
      else:
        player.currentRoom.doorSFlag=LOCKED
    elif player.playerFacing==EAST:
      if player.currentRoom.doorEFlag==PUZZLE:
        player.currentRoom.doorEFlag=UNLOCKED
      else:
        player.currentRoom.doorEFlag=LOCKED
    elif player.playerFacing==WEST:
      if player.currentRoom.doorWFlag==PUZZLE:
        player.currentRoom.doorWFlag=UNLOCKED
      else:
        player.currentRoom.doorWFlag=LOCKED
  player.inPuzzle=False
  player.traversal=True

###Update methods###

def updateMenu(event,player):
    menu=player.currentMenu
    if event.type == QUIT:
      sys.exit()

    elif event.type == KEYDOWN:
      newKey=pygame.key.name(event.key)

      if newKey=='escape':
        sys.exit()

      elif newKey=='[1]' or newKey=='return':
        if menu.name != "Math Stats":
          menu.progress(player,screen)

      elif newKey=='[2]' or newKey=='down':
        menu.select("down")

      elif newKey=='[3]' or newKey=='r':
        #Swap menus to right on 'stats' screen
        if menu.name=="Stats":
          #set to pause menu
          player.currentMenu=player.pauseMenu
        elif menu.name=="Inventory":
          #set to stats menu
          player.currentMenu=player.statsMenu
        elif menu.name=="Pause Menu":
          #set to math stats
          player.currentMenu=player.mathStats
        elif menu.name=="Math Stats":
          player.currentMenu.createInventory(player)
            


      elif newKey=='[4]' or newKey=='left':
        if menu.name=="Defeat":
          menu.select("up")
        elif menu.name=="Inventory":
          for i in range(10):
            menu.select("down")
 
      elif newKey=='[5]':
        print('check')

      elif newKey=='[6]' or newKey=='right':
        if menu.name=="Defeat":
          menu.select("down")
        elif menu.name=="Inventory":
          for i in range(10):
            menu.select("up")
      elif newKey=='[7]' or newKey=='l':
        #Swap menus left on 'stats' screen
        if menu.name=="Stats":
          #set to pause menu
          player.currentMenu.createInventory(player)
        elif menu.name=="Inventory":
          #set to stats menu
          player.currentMenu=player.mathStats
        elif menu.name=="Pause Menu":
          #set to inventory menu
          player.currentMenu=player.statsMenu
        elif menu.name=="Math Stats":
          player.currentMenu=player.pauseMenu

      elif newKey=='[8]' or newKey=='up':
        menu.select("up")

      elif newKey=='[9]' or newKey=='backspace':
        player.mainMenu=False
        player.traversal=True
        

def updateTraversal(event,player,screen):
    if event.type == QUIT:
      sys.exit()

    elif event.type == KEYDOWN:
      newKey=pygame.key.name(event.key)
      if newKey=='escape':
        sys.exit()

      elif newKey=='[2]':
        player.migrateMessages(checkDoor('down',player,screen))

      elif newKey=='[3]' or newKey=='i':
        if player.traversal:
          player.traversal=False
          player.mainMenu=True
          pauseMenuOptions=["Save","Close","Main Menu","Return to Game"]
          pauseMenuImages=[MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif"]
          player.currentMenu=Menu(pauseMenuOptions,player,ENV_PATH+"Black.gif",pauseMenuImages,"Pause Menu")

      elif newKey=='[4]' or newKey=='left':
        player.migrateMessages(checkDoor('left',player,screen))

      elif newKey=='[1]' or newKey=='e':
        player.migrateMessages(player.checkRoom())

      elif newKey=='[6]' or newKey=='right':
        player.migrateMessages(checkDoor('right',player,screen))

      elif newKey=='[7]' or newKey=='m':
        player.macroMap=True
        player.traversal=False
        player.dgnMap.drawMacro(player,screen)

      elif newKey=='[8]' or newKey=='up':
        player.migrateMessages(checkDoor('up',player,screen))

      elif newKey=='[9]' or newKey=='space':
        player.traversal=False
        player.mainMenu=True
        player.currentMenu=player.statsMenu
        player.previousMenu=player.statsMenu

def updateComic(event,player):
    if event.type == QUIT:
      sys.exit()

    elif event.type == KEYDOWN:
      newKey=pygame.key.name(event.key)

      if newKey=='escape':
        sys.exit()

      elif newKey=='[1]' or newKey=='right':
        player.comic.next(player)

      elif newKey=='[3]' or newKey=='left':
        player.comic.previous()

      elif newKey=='[4]' or newKey=='backspace':
        player.comic.previous()

      elif newKey=='[6]' or newKey=='return':
        player.comic.next(player)

#while waiting between rooms...
def updateWaiting(event,player):
  pygame.time.set_timer(USEREVENT+2,500)
  enemyList=[]
  player.traversal=False
  player.waiting=False

  ############################
  #Check enemies in room
  #####################
  if  not int(player.currentRoom.en1)==0:
    en=get_enemy( player.currentRoom.en1 )
    en.place=0
    enemyList.append(en)
  if  not int(player.currentRoom.en2)==0:
    en=get_enemy(player.currentRoom.en2)
    en.place=1
    enemyList.append(en)
  if  not int(player.currentRoom.en3)==0:
    en=get_enemy(player.currentRoom.en3)
    en.place=2
    enemyList.append(en)
  if  not int(player.currentRoom.en4)==0:
    en=get_enemy(player.currentRoom.en4)
    en.place=3
    enemyList.append(en)
  if len(enemyList)>0:   
    player.migrateMessages('initiating battle...')
    player.traversal=False
    player.curBattle=BattleEngine(player,enemyList)
  #################
  #check items in room
  #################
  ####MOVED TO setImage() and player.checkRoom()
def updateBattle(event,player):
  player.curBattle.Run(event,screen)

def updateMacroMap(event,player):
  if event.type == QUIT:
      sys.exit()

  elif event.type == KEYDOWN:
      newKey=pygame.key.name(event.key) 
      if newKey=='m' or newKey=='[7]':
        player.macroMap=False
        player.traversal=True
def updatePuzzle(event,player):
    if event.type == QUIT:
      sys.exit()

    elif event.type == KEYDOWN:
      newKey=pygame.key.name(event.key)
      if newKey=='escape':
        sys.exit()

      elif newKey=='[2]' or newKey=='down':
        player.puzzle.do_move(2)
        if player.puzzle.is_solved():
          stopPuzzle(player,True)

      elif newKey=='[3]' or newKey=='backspace':
        stopPuzzle(player,False)

      elif newKey=='[4]' or newKey=='left':
        player.puzzle.do_move(3)
        if player.puzzle.is_solved():
          stopPuzzle(player,True)

      elif newKey=='[1]' or newKey=='e':
        player.puzzle.showFull=not player.puzzle.showFull

      elif newKey=='[6]' or newKey=='right':
        player.puzzle.do_move(4)
        if player.puzzle.is_solved():
          stopPuzzle(player,True)

      elif newKey=='[7]' or newKey=='m':
        player.puzzle.showFull=not player.puzzle.showFull
        #display solved? might add later

      elif newKey=='[8]' or newKey=='up':
        player.puzzle.do_move(1)
        if player.puzzle.is_solved():
          stopPuzzle(player,True)

      elif newKey=='[9]' or newKey=='space':
        player.puzzle.showFull=not player.puzzle.showFull
      drawPuzzle(player,screen)
###Draw methods###
def drawTraversal(player,screen):
  setImage(player)

def drawPuzzle(player,screen):
  #draw background and completed image
  screen.fill((0,0,0),(0,0,1200,900))
  screen.blit(player.puzzle.puzBG,(75,-750,1200,900))
  if player.puzzleTutorial==False:
    font=pygame.font.SysFont("cmr10",35,False,False)
    y=0
    screen.fill((255,255,255),(0,2,1200,200))
    lines=["This door is locked with a special lock.  In order to unlock it, you must"," re-arrange the tiles and make the image whole.  Use the arrow keys ","to slide the tiles.  You can view the completed image by pressing","any other button.  To give up, press  or backspace."]
    screen.blit(pygame.image.load(TOUR_PATH+"button/"+"buttonX.gif"),(570,150,40,40))
    for message in lines:
      screen.blit(font.render(message,True,(75,0,0)),(0,20+y,200,300))
      y+=40
  if player.puzzle.showFull:
    screen.blit(player.puzzle.completedPuzzle,(300,100,600,400))
  else:
  #draw pieces in their position
    totalGroup=pygame.sprite.Group()
    x=-1
    y=-1
    for row in player.puzzle.pieceMap:
      x+=1
      y=-1
      for piece in row:
        y+=1
        piece=player.puzzle.pieceMap[x][y]
        spt=pygame.sprite.Sprite()
        spt.image=pygame.image.load(piece.filename)
        spt.rect=(300+(x*200),200+(y*200),200,200)
        if not piece.isHole:
          totalGroup.add(spt)
    totalGroup.draw(screen)
  pygame.display.flip()
def drawWaiting(player,screen):
  screen.fill(0,(0,0,1290,700),0)
def drawMacroMap(player,screen):
  player.dgnMap.drawMacro(player,screen)
  
def drawTextBox(player,screen):
  screen.fill(0,bigRect,0)
  # draw the text
  tl1=font.render(player.msg1,True,(255,255,255))
  tl2=font.render(player.msg2,True,(255,255,255))
  tl3=font.render(player.msg3,True,(255,255,255))
  tl4=font.render(player.msg4,True,(255,255,255))
  tl5=font.render(player.msg5,True,(255,255,255))
  player.dgnMap.display(player,screen)

  #screen.blit(text, textRect)
  screen.blit(tl1,line1)
  screen.blit(tl2,line2)
  screen.blit(tl3,line3)
  screen.blit(tl4,line4)
  screen.blit(tl5,line5)

while pippy.pygame.next_frame():

  for event in pygame.event.get():
    if event.type==USEREVENT+2:
      pygame.time.set_timer(USEREVENT+2,0)
      drawWaiting(player,screen)
      player.waiting=False
      if player.msg5=='Enemies are present, prepare to fight.':
        player.battle=True
      if player.currentRoom.roomFlag==6:
        player.currentRoom.setShop(player)
        player.shop=True
        player.traversal=False
        player.currentRoom.shop.draw(screen,player)

      if player.battle==False and player.shop==False:
####################################
###TEST FOR IN GAME TUTORIALS
####################################
      #  if player.currentX==0 and player.currentY==2 and player.battleTutorial==False:
      #    player.traversal=False
      #    player.battle=True
       #   player.curBattle=BattleEngine(player,[get_enemy( '3' )])
      #    player.initInGameBattleTutorial(screen)
        if player.currentX==1 and player.currentY==4 and player.movTutorial==False:
          player.initMovTutorial(screen)
        elif player.currentX==1 and player.currentY==3 and player.hpTutorial==False:
          player.battlePlayer.HP-=10
          player.migrateMessages("You trip on a crack in the floor and lose 10 HP")
          player.migrateMessages("But you can heal yourself with the remedy that you picked up")
          player.hpTutorial=True
          player.traversal=True
        elif player.currentX==2 and player.currentY==1 and player.hiddenTutorial==False:
          player.migrateMessages("You sense hidden items in this room, to search the room, press e or check")
          player.migrateMessages("If you discover an item, it will be added to your inventory, try it now")
          player.traversal=True
        else:
          player.traversal=True
      setImage(player)
    if event.type==QUIT:
      sys.exit()
    elif player.inComic:
      updateComic(event,player)
    elif player.traversal:
      if player.waiting==True:
        updateWaiting(event,player)
      else:
        #################UPDATE##############################
        updateTraversal(event,player,screen)


    elif player.battle:
      ##battle processes
      updateBattle(event,player)
    elif player.inPuzzle:
      updatePuzzle(event,player)
    elif player.mainMenu:
      ## main menu processes
        updateMenu(event,player)
    elif player.macroMap:
      updateMacroMap(event,player)
    elif player.shop:
      player.currentRoom.shop.update(event,player)

  ###############DRAW#########################
  #draw based on state
  if player.mainMenu==True:
    if player.currentMenu.name=="Stats" or player.currentMenu.name=="Inventory" or player.currentMenu.name=="Math Stats" or player.currentMenu.name=="Victory" or player.currentMenu.name=="Defeat":
      player.currentMenu.pauseMenuDraw(player,screen,450,400,24)
      drawTextBox(player,screen)
    elif player.currentMenu.name=="Pause Menu":
      player.currentMenu.pauseMenuDraw(player,screen,540,240,24)
      drawTextBox(player,screen)
    elif player.currentMenu.name=="Difficulty Menu":
      player.currentMenu.mainMenuDraw(player,screen,player.currentMenu.sX,player.currentMenu.sY,40)
    elif player.currentMenu.name=="Defeat":
      player.currentMenu.mainMenuDraw(player,screen,500,500,50)
      
    else:
      player.currentMenu.mainMenuDraw(player,screen,450,400,50)
  else:
    if player.traversal:
      if player.waiting:
        drawWaiting(player,screen)
      else:
        drawTextBox(player,screen)
        drawTraversal(player,screen)
    elif player.macroMap:
      player.dgnMap.drawMacro(player,screen)
    elif player.battle:
      drawTextBox(player,screen)
      player.curBattle.draw(player,screen)
    elif player.inPuzzle:
      drawPuzzle(player,screen)
    elif player.inComic:
      player.comic.draw(screen)
    elif player.shop:
      drawTextBox(player,screen)
      player.currentRoom.shop.draw(screen,player)
  if player.traversal:
    player.currentRoomGroup.draw(screen)
    player.itemsGroup.draw(screen)

    if player.movTutorial==False:
      player.initMovTutorial(screen)
    if player.movTutorial2==False and player.dgnIndex==0 and player.currentX==1 and player.currentY==3:
      player.initMovTutorial2(screen)
    if player.movTutorial3==False and player.dgnIndex==0 and player.currentX==0 and player.currentY==0:
      player.initMovTutorial3(screen)
    pygame.display.flip()
  # update the display




