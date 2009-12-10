import pippy, pygame, sys, math
from pygame.locals import *
from random import *
import os.path
################################################################################
#Start of external classes and functions
###############################################################################

#IMG_PATH = os.path.dirname(__file__) + "/images/"
IMG_PATH="/home/olpc/images/"
  ########################################################################
  #Dungeon class:  stores a 2d array of rooms representing the dungeon
  #                reads/parses a text file containing the data for a dungeon
  #######################################################################

class Dungeon:
  def __init__(self,sizeX=5,sizeY=5,fileName="dungeon2.txt"):
    self.sizeX=sizeX
    self.sizeY=sizeY
    self.fileName=fileName
    self.types=["none","Wizard","Goblin","Gru","Eye","Octopus"]
    ###INITALIZE DICTIONARY, TUPLE:ROOM PAIRINGS
    self.rooms={}

  def fill(self):
    #####open text file######
    dgnFile=open(self.fileName,'r')
    currentX=0
    currentY=0
    for line in dgnFile:
      ###print line for testing###

      ###initialize room variables###
      doorN=False
      doorNLock=False
      doorNPuzzle=False
      doorS=False
      doorSLock=False
      doorSPuzzle=False
      doorE=False
      doorELock=False
      doorEPuzzle=False
      doorW=False
      doorWLock=False
      doorWPuzzle=False
      shop=False
      puzzle=False
      event=None
      transport=False
      en1=0
      en2=0
      en3=0
      en4=0
      it1=0
      it2=0
      it3=0
      it4=0
      ###check characters in current line, set variables accordingly###
      ###KEY:1st character=door to north
      ###    2nd=door to south
      ###    3rd=door to east
      ###    4th=door to west
      ###    5th=if the room is a shop
      ###    6-9=enemy number in each slot (0 for no enemy)

      if line[0]=='N':
        doorN=True
      elif line[1]=='L':
        doorNLocked=True
      elif line[1]=='P':
        doorNPuzzle=True

      if line[2]=='S':
        doorS=True
      elif line[3]=='L':
        doorSLocked=True
      elif line[3]=='P':
        doorSPuzzle=True

      if line[4]=='E':
        doorE=True
      elif line[5]=='L':
        doorELocked=True
      elif line[5]=='P':
        doorEPuzzle=True

      if line[6]=='W':
        doorW=True
      elif line[7]=='L':
        doorWLocked=True
      elif line[7]=='P':
        doorWPuzzle=True

      if line[8]=='S':
        shop=True
      elif line[8]=='T':
        transport=True
      elif line[8]=='P':
        puzzle=True
      elif line[8]=='_':
        event=None
      else:
        event=int(line[8])

      rm=Room(doorN,doorNLock,doorNPuzzle,doorS,doorSLock,doorSPuzzle,doorE,doorELock,doorEPuzzle,doorW,doorWLock,doorWPuzzle,shop,puzzle,event,line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16])

      rm.transport=transport
      
      self.rooms[(currentX,currentY)]=rm
      ###update position in array###
      currentX+=1

      if currentX==self.sizeX:
        currentY+=1
        currentX=0

      if currentY>self.sizeY:
        break

##################################################################################

#Room class: stores data about a room in the dungeon.  IE doors, enemies, mood etc
####################################################################################
class Room:
  def __init__(self,doorN,doorNLock,doorNPuzzle,doorS,doorSLock,doorSPuzzle,doorE,doorELock,doorEPuzzle,doorW,doorWLock,doorWPuzzle,shop,puzzle,event,en1,en2,en3,en4,it1,it2,it3,it4):
    self.doorN=doorN
    self.doorNLock=doorNLock
    self.doorNPuzzle=doorNPuzzle
    self.doorS=doorS
    self.doorSLock=doorSLock
    self.doorSPuzzle=doorSPuzzle
    self.doorE=doorE
    self.doorELock=doorELock
    self.doorEPuzzle=doorEPuzzle
    self.doorW=doorW
    self.doorWLock=doorWLock
    self.doorWPuzzle=doorWPuzzle
    self.shop=shop
    self.puzzle=puzzle
    self.en1=en1
    self.en2=en2
    self.en3=en3
    self.en4=en4
    self.it1=it1
    self.it2=it2
    self.it3=it3
    self.it4=it4
    self.image=0
    self.transport=False
  #######To string method########
  def getData(self):
    string=""
    string+=repr(self.doorN)+repr(self.doorS)+repr(self.doorE)+repr(self.doorW)
    string+=self.en1+self.en2+self.en3+self.en4
    return(string)

  def setImage(self,imagePath):
    self.image=pygame.image.load(imagePath)

#################################################################################
  #Map class: stores information about the layout of the dungeon for easy display
###############################################################################
class Map:
  def __init__(self,dgn=Dungeon(0,0,'')):
    self.sizeX=dgn.sizeX
    self.sizeY=dgn.sizeY
    self.rectSizeX=38
    self.rectSizeY=38
    self.rects={}
    self.fullRooms={}
    self.totalSurface=pygame.Surface((self.sizeX*40,self.sizeY*40))

    for y in range(self.sizeY):
      for x in range(self.sizeX):
        curRect=pygame.Rect(x*40,y*40,self.rectSizeX,self.rectSizeX)
        self.rects[(x,y)]=curRect
        if dgn.rooms.get((x,y)).doorN:
          self.fullRooms[(x,y)]=True
          self.totalSurface.fill((255,255,255),curRect,0)

        elif dgn.rooms.get((x,y)).doorS:
          self.fullRooms[(x,y)]=True
          self.totalSurface.fill((255,255,255),curRect,0)

        elif dgn.rooms.get((x,y)).doorE:
          self.fullRooms[(x,y)]=True
          self.totalSurface.fill((255,255,255),curRect,0)

        elif dgn.rooms.get((x,y)).doorW:
          self.fullRooms[(x,y)]=True
          self.totalSurface.fill((255,255,255),curRect,0)

  def display(self,player,screen):
    mapView=pygame.transform.chop(self.totalSurface,(0,0,0,0))
    mapView.fill((255,0,0),(player.currentX*40,player.currentY*40,38,38))
    NORTH=1
    SOUTH=3
    EAST=0
    WEST=2
    angle=0

    if player.playerFacing==NORTH:
      angle=0
      mapView=pygame.transform.rotate(mapView,angle)
      angle=90
    elif player.playerFacing==SOUTH:
      angle=180
      mapView=pygame.transform.rotate(mapView,angle)
      angle=270
    elif player.playerFacing==EAST:
      angle=90
      mapView=pygame.transform.rotate(mapView,angle)
      angle=0
    elif player.playerFacing==WEST:
      angle=270
      mapView=pygame.transform.rotate(mapView,angle)
      angle=180

    angle=angle*(math.pi/180)
    curSect=pygame.Rect(0,700,200,200)
    curSect.top+=((player.currentX*40-81)*math.cos(angle))-((player.currentY*40-81)*math.sin(angle))
    curSect.left-=((player.currentX*40-81)*math.sin(angle))+((player.currentY*40-81)*math.cos(angle))

    screen.fill(0,(0,700,200,300),0)
    screen.blit(mapView,curSect)
    screen.fill(0,(200,700,1200,300),0)
        
###########################################################################
#  Menu class:  contains a list of options (which can be other menus)
#               has a background image as well as images for each option
###########################################################################
class Menu:
    def __init__(self,options,player,bgImageFile,optionImageFiles,name):
        self.options=options
        self.currentOption=0
        self.background=pygame.sprite.Sprite()
        self.background.image=pygame.image.load(bgImageFile)
        self.background.rect=pygame.Rect(0,0,1290,900)
        self.optionsImages=[]
        self.numPad=False
        self.name=name
        self.inventoryUp=False
        self.sX=0
        self.xY=0
        i=0
        for name in optionImageFiles:
            sprite=pygame.sprite.Sprite()
            sprite.image=pygame.image.load(name)
            sprite.rectangle=pygame.Rect(0,0,1290,60)
            self.optionsImages.append(sprite)
            i+=1

        self.size=i

    def draw(self,player,screen,xStart,yStart,height):
        menuGroup=pygame.sprite.Group()
	bgGroup=pygame.sprite.Group(self.background)
        bgGroup.draw(screen)
        i=0
        sel=0
        if self.numPad==False and not self.name=="Stats" and not self.name=="Inventory":
          for image in self.optionsImages:
              if i==self.currentOption:
                image.rect=pygame.Rect(xStart+30,yStart+(i*height),1290,height)

              else:
                image.rect=pygame.Rect(xStart,yStart+(i*height),1290,height)
              menuGroup.add(image)
              i+=1
        elif self.numPad==True:
          for image in self.optionsImages:
            if i==3:
              i=0
              yStart+=height
            if self.options[sel]=="Enter Answer":
              yStart+=height
              height*=3
              i=0
            image.rect=pygame.Rect(xStart+(i*height),yStart,height,height)
            menuGroup.add(image)
            if sel==self.currentOption:
              fillRect=image.rect
              fillRect.top-=5
              fillRect.left-=5
              fillRect.width+=10
              fillRect.height+=10
              screen.fill((50,50,255),fillRect,0)
            i+=1
            sel+=1
          
        if self.name=="Stats":
          #add screen-sized image with transparency
          bgGroup.empty()
          screen.fill((250,250,50),pygame.Rect(200,0,800,900))
          screen.fill((0,0,0),pygame.Rect(200,0,250,250))
          font=pygame.font.Font(None,42)
          hp=font.render("HP: "+repr(player.battlePlayer.HP),True,(0,0,0))
          hpRect=pygame.Rect(210,320,200,42)
          screen.blit(hp,hpRect)
          att=font.render("Attack: "+repr(player.battlePlayer.attackPower("basic")),True,(0,0,0))
          attRect=pygame.Rect(210,370,200,42)
          screen.blit(att,attRect)
          defense=font.render("Defense: "+repr(player.battlePlayer.defensePower()),True,(0,0,0))
          defenseRect=pygame.Rect(210,420,200,42)
          screen.blit(defense,defenseRect)
          #define rectangles
          weaponRect=pygame.Rect(470,20,200,42)
          self.optionsImages[0].rect=weaponRect
          armorRect=pygame.Rect(470,70,200,42)
          self.optionsImages[1].rect=armorRect
          accessoryRect=pygame.Rect(470,120,200,42)
          self.optionsImages[2].rect=accessoryRect
          itemRect=pygame.Rect(500,220,200,42)
          self.optionsImages[3].rect=itemRect
          item2Rect=pygame.Rect(500,270,200,42)
          self.optionsImages[4].rect=item2Rect
          item3Rect=pygame.Rect(500,320,200,42)
          self.optionsImages[5].rect=item3Rect
          item4Rect=pygame.Rect(500,370,200,42)
          self.optionsImages[6].rect=item4Rect
          self.optionsImages[self.currentOption].rect.left+=10
          #draw buttons
          bgButtonGroup=pygame.sprite.Group(self.optionsImages)
          bgButtonGroup.draw(screen)
	  #draw dynamic text
          if player.battlePlayer.weapon.name=="":
            wp="Weapon Slot"
          else:
            wp=player.battlePlayer.weapon.name
          if player.battlePlayer.armor.name=="":
            arm="Armor Slot"
          else:
            arm=player.battlePlayer.armor.name
          if player.battlePlayer.accessory.name=="":
            acc="Accessory Slot"
          else:
            acc=player.battlePlayer.accessory.name
          if len(player.battlePlayer.eqItem)>0:
            it1=player.battlePlayer.eqItem[0].name
          if len(player.battlePlayer.eqItem)>1:
            it2=player.battlePlayer.eqItem[1].name
          if len(player.battlePlayer.eqItem)>2:
            it3=player.battlePlayer.eqItem[2].name
          if len(player.battlePlayer.eqItem)==4:
            if player.battlePlayer.eqItem[0].name=="":
              it1="Item Slot 1"
            else:
              it1=player.battlePlayer.eqItem[0].name
            if player.battlePlayer.eqItem[1].name=="":
              it2="Item Slot 2"
            else:
              it2=player.battlePlayer.eqItem[1].name
            if player.battlePlayer.eqItem[2].name=="":
              it3="Item Slot 3"
            else:
              it3=player.battlePlayer.eqItem[2].name
            if player.battlePlayer.eqItem[3].name=="":
              it4="Item Slot 4"
            else:
              it4=player.battlePlayer.eqItem[3].name


          weapon=font.render(wp,True,(0,0,0))
          screen.blit(weapon,weaponRect)
          armor=font.render(arm,True,(0,0,0))
          screen.blit(armor,armorRect)
          accessory=font.render(acc,True,(0,0,0))
          screen.blit(accessory,accessoryRect)
          item1=font.render(it1,True,(0,0,0))
          screen.blit(item1,itemRect)
          item2=font.render(it2,True,(0,0,0))
          screen.blit(item2,item2Rect)
          item3=font.render(it3,True,(0,0,0))
          screen.blit(item3,item3Rect)
          item4=font.render(it4,True,(0,0,0))
          screen.blit(item4,item4Rect)
        if self.name=="Inventory":
            font=pygame.font.Font(None,42)
            y=0
            sel=0
            screen.fill((50,255,50),pygame.Rect(xStart,yStart,200,40*len(player.battlePlayer.inv_Ar)))
            for item in player.battlePlayer.inv_Ar:
              if sel==self.currentOption:
                screen.fill((250,50,50),pygame.Rect(self.sX,self.sY+y,200,40))
              screen.blit(font.render(item.name,True,(0,0,0)),pygame.Rect(self.sX,self.sY+y,200,40))
              y+=40
              sel+=1
        menuGroup.draw(screen)

        if player.battle==False:
          pygame.display.flip()

    def select(self,direction):
        if direction=="up":
            if self.currentOption>0:
                self.currentOption-=1

            else:
                self.currentOption=0
        else:
            if self.currentOption<self.size-1:
                self.currentOption+=1

            else:
                self.currentOption=self.size-1

    def progress(self,player,screen):
        if type(self.options[self.currentOption])==type(self):
            player.currentMenu=self.options[self.currentOption]
            player.previousMenu=self
        else:
            self.updateByName(self.options[self.currentOption],player,screen)

    def regress(self,player):
        if self.name=="Stats":
          player.mainMenu=False
          player.traversal=True
        else:
          temp=player.currentMenu
          player.currentMenu=player.previousMenu
          player.previousMenu=temp

    def updateByName(self,name,player,screen):
        if name=="New Game":
            player.dgnIndex=-1
            player.currentX=0
            player.currentY=0
            player.nextDungeon()

            player.traversal=True
            player.mainMenu=False

            setImage(player)
            player.battlePlayer=Hero(player)
            player.currentRoomGroup.draw(screen)
            pygame.display.flip()

        elif name=="Close":
            sys.exit()

        elif name=="Tutorial":
            player.inTutorial=True
            player.mainMenu=False

        elif name=="Attack":
            seed()
            crit=randint(0,2)
            if crit==1:
              player.curBattle.critical(player)
            else:
              player.curBattle.attack(player.battlePlayer,"basic")
        elif name=="0" or name=="1"or name=="2" or name=="3" or name=="4" or name=="5" or name=="6" or name=="7"or name=="8"or name=="9":
          player.battlePlayer.currentInput+=name
        elif name=="Clear":
          player.battlePlayer.currentInput=""
        elif name=="Enter Answer":
          if not player.battlePlayer.currentInput =="":
            if player.battlePlayer.currentAnswer==int(player.battlePlayer.currentInput):
              player.curBattle.attack(player.battlePlayer,"critical")
            else:
              player.curBattle.attack(player.battlePlayer,"basic")
          else:
            player.curBattle.attack(player.battlePlayer,"basic")
        elif name=="Division":
          player.curBattle.divisionAttack()
        elif name=="1/2":
	  player.battlePlayer.fractionSum += .5
	  player.curBattle.checkFraction()
	elif name=="1/3":
	  player.battlePlayer.fractionSum += .33
	  player.curBattle.checkFraction()
	elif name=="1/4":
	  player.battlePlayer.fractionSum += .25
	  player.curBattle.checkFraction()
	elif name=="1/6":
	  player.battlePlayer.fractionSum += .166
	  player.curBattle.checkFraction()
        elif name=="Geometry":
          player.curBattle.magic(player)
        elif name=="Fire" or name=="Lightning" or name=="Heal" or name=="Missile":
          player.battlePlayer.currentProb1=""
          player.battlePlayer.currentProb2=""
          player.battlePlayer.currentInput=""
          player.curBattle.startGlyph(name)
	elif name=="Fire1" or name=="Fire2" or name=="Fire3" or name=="Fire4" or name=="Heal1" or name=="Heal2" or name=="Heal3" or name=="Heal4" or name=="Lightning1" or name=="Lightning2" or name=="Lightning3" or name=="Lightning4":
	  player.curBattle.checkGlyph(name)
        elif name=="Use Item":
          for i in player.battlePlayer.eqItem:
            if i.name=="":
              player.battlePlayer.eqItem.remove(i)
          player.currentMenu=player.curBattle.itemMenu
        elif name=="Item1" or name=="Item2" or name=="Item3" or name=="Item4":
          index=int(repr(name)[5])-1
          if index<len(player.battlePlayer.eqItem):
            player.curBattle.useItem(player.battlePlayer.eqItem[int(repr(name)[5])-1])
          else:
            player.currentMenu=player.curBattle.battleMenu
	  #if we decide to add puzzle/minigame items, here's where they'd go
        elif name=="Weapon" or name=="Armor" or name=="Accessory" or name=="ItemSlot1" or name=="ItemSlot2" or name=="ItemSlot3" or name=="ItemSlot4":
          self.createInventory(player,name)
          player.currentMenu=player.currentMenu=self.inventoryMenu
        elif name[0:9]=="Equipment":
          player.battlePlayer.equip(player.battlePlayer.inv_Ar[int(name[9:10])],self.target)
          player.currentMenu=player.statsMenu
	else:
	    sys.exit()
    def createInventory(self,player,name):
      invOptions=[]
      invImages=[]
      i=0
      for item in player.battlePlayer.inv_Ar:
        invOptions.append("Equipment"+repr(i))
        i+=1
        invImages.append(IMG_PATH+"BlankButton.gif")
      self.inventoryMenu=Menu(invOptions,player,IMG_PATH+"BlankButton.gif",invImages,"Inventory")
      self.inventoryMenu.sX=self.optionsImages[self.currentOption].rect.left+250
      self.inventoryMenu.sY=self.optionsImages[self.currentOption].rect.top
      self.inventoryMenu.target=name
      player.currentMenu=self.inventoryMenu

######################################################################
#Tutorial Class: stores image list, traverses through list
######################################################################
class Tutorial:
    def __init__(self,imageList,sX,sY):
        self.currentIndex = 0
        self.images=[]

        for image in imageList:
          spt=pygame.sprite.Sprite()
          spt.image=pygame.image.load(image)
          spt.rect=pygame.Rect(sX,sY,1290,700)
	  self.images.append(spt)

       	self.size=len(imageList)

    def next(self):
    	if  self.currentIndex < self.size - 1:
       	  self.currentIndex+=1

    	else:
          self.currentIndex=0
	  player.mainMenu = True
	  player.inTutorial = False

    def previous(self):
      if self.currentIndex > 0:
        self.currentIndex-=1

      else:
        self.currentIndex=0

    def draw(self,group,screen):
        group.empty()
        group.add(self.images[self.currentIndex])
        group.draw(screen)
        pygame.display.flip()

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
    
    self.initializeMenu()
    self.loadTutorial()
    self.loadImages()
    self.currentX=x
    self.currentY=y
    self.dgnIndex=-1
    self.dungeons=[("Dungeon.txt",4,5),("dungeon2.txt",5,5)]
    self.nextDungeon()
    self.battlePlayer=Hero(self)
    self.curBattle=BattleEngine(self.battlePlayer,[Enemy(self,'0')])

    #state variables
    self.inTutorial=False
    self.mainMenu=True
    self.traversal=False
    self.waiting=False
    self.battle=False
    #self.statMenu=False

    self.msg1=""
    self.msg2=""
    self.msg3=""
    self.msg4=""
    self.msg5=""

    #traversal variables
    self.currentX=x
    self.currentY=y

    self.playerFacing=SOUTH

    #sound
    self.doorEffect=pygame.mixer.Sound(IMG_PATH+"door.wav")

  def initializeMenu(self):
    mainMenuImages=[IMG_PATH+"TutorialButton.gif",IMG_PATH+"NewGameButton.gif",IMG_PATH+"CloseButton.gif"]
    self.MainMenu=Menu(["Tutorial","New Game","Close"],self,IMG_PATH+"TitleImage.gif",mainMenuImages,"Main Menu")
    
    statMenuOptions=["Weapon","Armor","Accessory","ItemSlot1","ItemSlot2","ItemSlot3","ItemSlot4"]
    statMenuImages=[IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif"]
    self.statsMenu=Menu(statMenuOptions,self,IMG_PATH+"battleMenubackground.gif",statMenuImages,"Stats")

    self.currentMenu=self.MainMenu
    self.previousMenu=self.MainMenu

 # def createInventoryMenu(self):
  #  inventoryMenuOptions=[]
  #  for item in self.battlePlayer.int_Ar:
    
  def loadTutorial(self):
    tutorialImages=[IMG_PATH+"t1.gif",IMG_PATH+"t2.gif",IMG_PATH+"t3.gif"]
    self.tutorial=Tutorial(tutorialImages,0,0)

  def loadImages(self):
    self.currentRoomSprite=pygame.sprite.Sprite()
    self.currentRoomSprite.image=pygame.image.load(IMG_PATH+"Black.gif")
    self.currentRoomSprite.rect=pygame.Rect(0,0,1200,700)

    self.Black=pygame.sprite.Sprite()
    self.Black.image=pygame.image.load(IMG_PATH+"Black.gif")
    self.Black.rect=pygame.Rect(0,0,1200,700)

    self.FLRSprite=pygame.sprite.Sprite()
    self.FLRSprite.image=pygame.image.load(IMG_PATH+"flr.gif")
    self.FLRSprite.rect=self.currentRoomSprite.rect

    self.FRSprite=pygame.sprite.Sprite()
    self.FRSprite.image=pygame.image.load(IMG_PATH+"fr.gif")
    self.FRSprite.rect=self.currentRoomSprite.rect

    self.FSprite=pygame.sprite.Sprite()
    self.FSprite.image=pygame.image.load(IMG_PATH+"f.gif")
    self.FSprite.rect=self.currentRoomSprite.rect

    self.FLSprite=pygame.sprite.Sprite()
    self.FLSprite.image=pygame.image.load(IMG_PATH+"fl.gif")
    self.FLSprite.rect=self.currentRoomSprite.rect

    self.LRSprite=pygame.sprite.Sprite()
    self.LRSprite.image=pygame.image.load(IMG_PATH+"lr.gif")
    self.LRSprite.rect=self.currentRoomSprite.rect

    self.LSprite=pygame.sprite.Sprite()
    self.LSprite.image=pygame.image.load(IMG_PATH+"l.gif")
    self.LSprite.rect=self.currentRoomSprite.rect

    self.NoSprite=pygame.sprite.Sprite()
    self.NoSprite.image=pygame.image.load(IMG_PATH+"_.gif")
    self.NoSprite.rect=self.currentRoomSprite.rect

    self.RSprite=pygame.sprite.Sprite()
    self.RSprite.image=pygame.image.load(IMG_PATH+"r.gif")
    self.RSprite.rect=self.currentRoomSprite.rect

    self.currentRoomGroup=pygame.sprite.Group(self.currentRoomSprite)

  def migrateMessages(self,msg):
    self.msg1=self.msg2
    self.msg2=self.msg3
    self.msg3=self.msg4
    self.msg4=self.msg5
    self.msg5=msg
  def nextDungeon(self):
    self.currentX=0
    self.currentY=0
    self.dgnIndex+=1
    dgnWidth=self.dungeons[self.dgnIndex][1]
    dgnHeight=self.dungeons[self.dgnIndex][2]
    self.dgn=Dungeon(dgnWidth,dgnHeight,IMG_PATH+self.dungeons[self.dgnIndex][0])
    self.dgn.fill()
    self.currentRoom=self.dgn.rooms.get((self.currentX,self.currentY))
    self.dgnMap=Map(self.dgn)
    self.currentRoom=self.dgn.rooms.get((self.currentX,self.currentY))

#################################################################################
#Item class: stores info about items
#################################################################################
class Item:
  def __init__(self,player,name,typ):
    self.name=name
    self.type=typ
    self.power=0
    
    if self.name=="Potion":
      self.power=20
    elif self.name=="Sword":
      self.power=25
    elif self.name=="Vest":
      self.power=10
    elif self.name=="Ring":
      self.power=5
#######################################################################

#Hero class - represents the player in battle and holds all of their data

##########################################################################
class Hero:
  def __init__(self,player):
#****property********value**********************description**********************#
	self.MHP 	= 40		#maximum health points (base HP)
	self.HP		= 40		#current health points
	self.BHP 	= 0		#bonus health points (from equipment)
	self.ATT 	= 10		#base attack power
	self.BAB	= 0		#bonus attack power (from battle timer)
	self.BAE	= 0		#bonus attack power (from equipment)
	self.DEF	= 1		#base defense power
	self.BDE	= 0		#bonus defense  power(from equipment)

	self.weapon=Item(player,"","")
	self.armor=Item(player,"","")
	self.accessory=Item(player,"","")
        self.eqItem=[]			#player can equip up to 4 usable items to use in battle
	self.inv_Ar 	= []		#inventory
	self.attacks_Ar = []		#associated array for attack string names and attack power values
        self.currentInput=""
        self.currentProb1=0
        self.currentProb2=0
        self.currentAnswer=0

        basicSword=Item(player,"Sword","Weapon")
        amulet=Item(player,"Amulet","Weapon")
        basicArmor=Item(player,"Vest","Armor")
        potion=Item(player,"Potion","Usable")
        grenade=Item(player,"Grenade","Usable")
        basicRing=Item(player,"Ring","Accessory")
        emptyItem=Item(player,"","Usable")
        self.eqItem=[emptyItem,emptyItem,emptyItem,emptyItem]
        self.inv_Ar=[basicSword,amulet,basicArmor,potion,basicRing,grenade,potion]

#****HERO ACCESSORS*********************************************#
  #returns player's maximum health
  def maxHealthPoints(self):
    return (self.HP + self.BHP)

  #returns player's current health
  def healthPoints(self):
    return (self.HP)

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
      return self.ATT*1.5
    elif name=="Missile":
      return 0

  #returns player's current defense power
  def defensePower(self):
    return (self.DEF + self.BDE)

  #returns player's equipped items
  def equipment(self):
    return self.eqItems_Ar	

  #returns player's current inventory
  def inventory(self):
    return self.inv_Ar

#****HERO MUTATORS************************************************#
  #sets player's current health
  def setHealth(self,_HP):
    self.HP = _HP

  #sets player's bonus health
  def setBonusHP(self,_BHP):
    self.BHP = _BHP

  #sets player's bonus attack power (from battle timer)
  def setBonusAP(self,_BAP):
    self.BAB = _BAP

  #sets player's bonus attack power (from equipment)
  def setBonusAE(self,_BAE):
    self.BAE = _BAE

  #sets player's bonus defense power (from equipment)
  def setBonusDE(self,_BDE):
    self.BDE = _BDE

  #increases player's current health by given amount
  def giveHealth(self,_inc):
    self.HP += _inc
    if healthPoints() > maxHealthPoints():
	setHealth(maxHealthPoints())

  #player is attacked by given damage
  def defendAttack(self,dmg):
    self.HP -= (dmg - self.defensePower())
    if self.HP<0:
      self.HP=0
#****BATTLE ACCESSORS***********************************************#
  #returns player's list of attacks that are currently available for use
  def availableAttacks(self):
    return self.attacks_Ar
      #returns the attack power of a given attack type

#****INVENTORY MUTATORS********************************************#
  #add item to equipment
  def equip(self,item,target):
    #add  _item to equipment
    if target=="Weapon" and item.type=="Weapon":
      if not self.weapon.name=="":
        self.inv_Ar.append(self.weapon)
      self.weapon=item
      self.inv_Ar.remove(item)
      self.BAE=item.power
    elif target=="Armor" and item.type=="Armor":
      if not self.armor.name=="":
        self.inv_Ar.append(self.armor)
      self.armor=item
      self.inv_Ar.remove(item)
      self.BDE=item.power
    elif target=="Accessory" and item.type=="Accessory":
      if not self.accessory.name=="":
        self.inv_Ar.append(self.accessory)
      self.accessory=item
      self.inv_Ar.remove(item)
      self.BHP=item.power
    elif target[0:8]=="ItemSlot" and item.type=="Usable":
      if len(self.eqItem)<4:
        self.eqItem.append(item)
      else:
        if not self.eqItem[int(target[8])-1].name=="":
          self.inv_Ar.append(self.eqItem[int(target[8])-1])
        self.inv_Ar.remove(item)
        self.eqItem[int(target[8])-1]=item




  #remove item from equipment
  def remEquipment(self,item):
    if item.type=="Weapon":
      self.weapon=0
      self.BAE=0
    elif item.type=="Armor":
      self.armor=0
      self.BDE=0
    elif item.type=="Accessory":
      self.accessory=0
      self.BHP=0
    else:
      if self.eqItem.has(item):
        self.eqItem.remove(item)
    #remove _item from equipment -- leave cell empty

  #add item to inventory
  def addInventory(self,item):
    self.inv_Ar.append(item)
    #add _item to end of inventory

  def remInventory(self,item):
    self.inv_Ar.remove(item)
    #remove _item from inventory
#end class Hero

##############################################################################		
#Enemy class - represents an enemy and holds all of its data
#############################################################
class Enemy:
  def __init__(self,player,name):
#****property********value**********************description**********************#
	self.MHP 	= 40				#maximum health points (base HP)
	self.HP		= 40				#cur print "Fire"rent health points
	self.BHP 	= 0				#bonus health points (from equipment)
	self.ATT 	= 10 				#base attack power
	self.BAE	= 0				#bonus attack power (from equipment)
	self.DEF	= 1				#base defense power
	self.BDE	= 0				#bonus defense  power(from equipment)
	self.eqItems_Ar	= []	#equipped items
	self.attacks_Ar = []	#associated array for attack string names and attack power values
	self.eqItem_Ar = []
	self.inv_Ar = []
	self.attacks_Ar = []
        self.sprite=pygame.sprite.Sprite()
        self.place=0
        #load image based on type later
        self.name=player.dgn.types[int(name)]
        print(self.name)
        if self.name=="Wizard":
          self.sprite.image=pygame.image.load(IMG_PATH+"concept_wizard.gif")
          self.HP=20
          self.ATT=40
        elif self.name=="Goblin":
          self.sprite.image=pygame.image.load(IMG_PATH+"concept_goblin.gif")
          self.HP=40
          self.ATT=10
        elif self.name=="Orc":
          self.sprite.image=pygame.image.load(IMG_PATH+"concept_orc.gif")
          self.HP=60
          self.ATT=35
        else:
          self.sprite.image=pygame.image.load(IMG_PATH+"FireGlyph.gif")
        self.sprite.rect=(200,200,50,300) 

#****ENEMY ACCESSORS*********************************************#
  #returns enemy's maximum health
  def maxHealthPoints(self):
    return (self.HP + self.BHP)	

  #returns enemy's current health
  def healthPoints(self):
    return (self.HP)

  #returns enemy's current attack power
  def attackPower(self):
    return (self.ATT+self.BAE)

  #returns enemy's current defense power
  def defensePower(self):
    return (self.DEF + self.BDE)

  #returns enemy's equipped items
  def equipment(self):
    return self.eqItems_Ar

  #returns enemy's current inventory
  def inventory(self):
    return self.inv_Ar

#****ENEMY MUTATORS************************************************#
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

  #increases enemy's current health by given amount
  def giveHealth(self,_inc):
    self.HP += _inc
    if healthPoints(self) > maxHealthPoints(self):
	setHealth(self,maxHealthPoints(self))

  #enemy is attacked by given damage
  def defendAttack(self,dmg):
    self.HP -= (dmg - self.defensePower())
    if self.HP<0:
      self.HP=0

#****BATTLE ACCESSORS***********************************************#
  #returns player's list of attacks that are currently available for use
  def availableAttacks(self):
    return self.attacks_Ar

#****INVENTORY MUTATORS********************************************#
  #add item to equipment
  def addEquipment(self,_item):
    print("add equip")
      #add  _item to equipment
      #if _item is weapon - add to first slot
      #if _item is armor - add to second slot
      #if _item is consumable - add to slots 3-6
      #remove item from equipment

  def remEquipment(self,_item):
    print("remove equip")
    #remove _item from equipment -- leave cell empty
#end class Enemy
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
        self.lightning1btn=IMG_PATH+"LigGlyph1btn.gif"
        self.lightning1=pygame.sprite.Sprite()
	self.lightning1.image=pygame.image.load(IMG_PATH+"LigGlyph1.gif")
        self.lightning2btn=IMG_PATH+"LigGlyph2btn.gif"
        self.lightning2=pygame.sprite.Sprite()
	self.lightning2.image=pygame.image.load(IMG_PATH+"LigGlyph2.gif")
        self.lightning3btn=IMG_PATH+"LigGlyph3btn.gif"
        self.lightning3=pygame.sprite.Sprite()
	self.lightning3.image=pygame.image.load(IMG_PATH+"LigGlyph3.gif")
        self.lightning4btn=IMG_PATH+"LigGlyph4btn.gif"
        self.lightning4=pygame.sprite.Sprite()
	self.lightning4.image=pygame.image.load(IMG_PATH+"LigGlyph4.gif")

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
        i=0
	for enemy in self.enemies:
          enemy.place=i
          i+=1
	self.player.msg5= "Enemies are present, prepare to fight."

  def initializeMenus(self,player):

    battleOptions=["Attack","Division","Geometry","Use Item"]
    battleBackground=IMG_PATH+"battleMenubackground.gif"
    battleOptImg=[IMG_PATH+"attackButton.gif",IMG_PATH+"DivPH.gif",IMG_PATH+"GeomPH.gif",IMG_PATH+"ItemPH.gif"]
    
    self.battleMenu=Menu(battleOptions,player,battleBackground,battleOptImg,"Battle")
    self.battleMenu.background.rect=(200,580,200,200)
    self.battleMenu.size=4

    numOptArr = ["1","2","3","4","5","6","7","8","9","0","Clear","Enter Answer"]
    numBG=IMG_PATH+"numPadbackground.gif"
    numOptImg=[IMG_PATH+"1.gif",IMG_PATH+"2.gif",IMG_PATH+"3.gif",IMG_PATH+"4.gif",IMG_PATH+"5.gif",IMG_PATH+"6.gif",IMG_PATH+"7.gif",IMG_PATH+"8.gif",IMG_PATH+"9.gif",IMG_PATH+"0.gif",IMG_PATH+"Clear.gif",IMG_PATH+"Enter.gif"]
    self.numPadMenu=Menu(numOptArr,player,numBG,numOptImg,"Number Pad")
    self.numPadMenu.background.rect=(800,500,200,200)
    self.numPadMenu.numPad=True

    magicOptions=["Fire","Lightning","Missile","Heal"]
    magicBackground=IMG_PATH+"battleMenubackground.gif"
    magicOptImg=[IMG_PATH+"1.gif",IMG_PATH+"2.gif",IMG_PATH+"3.gif",IMG_PATH+"4.gif"]
    self.magicMenu=Menu(magicOptions,player,magicBackground,magicOptImg,"Magic Menu")
    self.magicMenu.background.rect=(200,580,200,200)

    divisionOptions=["1/2","1/3","1/4","1/6"]
    divisionBackground=IMG_PATH+"battleMenubackground.gif"
    divisionOptImg=[IMG_PATH+"1.gif",IMG_PATH+"2.gif",IMG_PATH+"3.gif",IMG_PATH+"4.gif"]
    self.divisionMenu=Menu(divisionOptions,player,divisionBackground,divisionOptImg,"Division Menu")
    self.divisionMenu.background.rect=(200,580,200,200) 

    itemOptions=["Item1","Item2","Item3","Item4"]
    itemBackground=IMG_PATH+"battleMenubackground.gif"
    itemOptImg=[IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif",IMG_PATH+"BlankButton.gif"]
    
    self.itemMenu=Menu(itemOptions,player,itemBackground,itemOptImg,"Item")
    self.itemMenu.background.rect=(200,550,200,200)

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
        sel.image=pygame.image.load(IMG_PATH+"EnterAnswer.gif")
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
      player.currentMenu.draw(player,screen,200,500,45)
      if player.currentMenu.name=="Item":
        i=0
        for image in player.currentMenu.optionsImages:
          if i<len(player.battlePlayer.eqItem):
            font = pygame.font.Font(None, 36)
            t=font.render(player.battlePlayer.eqItem[i].name,True,(255,255,255))
            screen.blit(t,image.rect) 
            i+=1     
    else:
      player.currentMenu.draw(player,screen,700,500,40)
      if not player.battlePlayer.currentProb1=="":
        font = pygame.font.Font(None, 36)
        probText=font.render(repr(player.battlePlayer.currentProb1)+" X "+repr(player.battlePlayer.currentProb2),True,(255,255,255))
        inputText=font.render(player.battlePlayer.currentInput,True,(255,255,255))
        screen.blit(probText,pygame.Rect(700,450,200,30))
        screen.blit(inputText,pygame.Rect(700,480,200,30))
      
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
      player.migrateMessages("You heal "+repr(-1*int(attacker.attackPower(attackName)))+" HP")
    else:
      player.migrateMessages("You attack for "+repr(int(attacker.attackPower(attackName)))+" damage")
      player.migrateMessages("Enemy HP is "+repr(int(defender.HP)))

    defender.defendAttack(attacker.attackPower(attackName))
    self.playerTurn=False
    self.CheckEndBattle()
    player.currentMenu=self.battleMenu

  def critical(self,player):
    pygame.time.set_timer(USEREVENT+1,500)
    player.battlePlayer.currentInput=""
    player.currentMenu=self.numPadMenu
    prob1=randint(0,12)
    prob2=randint(0,12)
    player.battlePlayer.currentProb1=prob1
    player.battlePlayer.currentProb2=prob2
    player.battlePlayer.currentAnswer=prob1*prob2

  def magic(self,player):
    player.currentMenu=self.magicMenu
    pygame.time.set_timer(USEREVENT+1,500)
  def startGlyph(self,name):
    self.glyphGroup.empty()
    self.glyphOverlayGroup.empty()
    if name=="Fire":
      shuffle2D=[("Fire1",self.fire1btn),("Fire2",self.fire2btn),("Fire3",self.fire3btn),("Fire4",self.fire4btn),("Not",self.heal1btn),("Not",self.heal4btn),("Not",self.lightning3btn),("Not",self.lightning1btn),("Not",self.heal1btn)]
      shuffle(shuffle2D)
      glyphMenuOptions=[shuffle2D[0][0],shuffle2D[1][0],shuffle2D[2][0],shuffle2D[3][0],shuffle2D[4][0],shuffle2D[5][0],shuffle2D[6][0],shuffle2D[7][0],shuffle2D[8][0]]
      glyphMenuImages=[shuffle2D[0][1],shuffle2D[1][1],shuffle2D[2][1],shuffle2D[3][1],shuffle2D[4][1],shuffle2D[5][1],shuffle2D[6][1],shuffle2D[7][1],shuffle2D[8][1]]
      glyphMenu=Menu(glyphMenuOptions,self.player,IMG_PATH+"battleMenubackground.gif",glyphMenuImages,"Glyph Menu")
      glyphMenu.numPad=True
      glyphMenu.background.rect=(200,580,200,200)
      player.currentMenu=glyphMenu
      self.fire.rect=(self.enemies[self.selEnemyIndex].sprite.rect.left-40,self.enemies[self.selEnemyIndex].sprite.rect.top+40,300,300)
      self.glyphGroup.add(self.fire)
    elif name=="Lightning":
      shuffle2D=[("Lightning1",self.lightning1btn),("Lightning2",self.lightning2btn),("Lightning3",self.lightning3btn),("Lightning4",self.lightning4btn),("Not",self.heal1btn),("Not",self.heal2btn),("Not",self.fire3btn),("Not",self.fire1btn),("Not",self.fire1btn)]
      shuffle(shuffle2D)
      glyphMenuOptions=[shuffle2D[0][0],shuffle2D[1][0],shuffle2D[2][0],shuffle2D[3][0],shuffle2D[4][0],shuffle2D[5][0],shuffle2D[6][0],shuffle2D[7][0],shuffle2D[8][0]]
      glyphMenuImages=[shuffle2D[0][1],shuffle2D[1][1],shuffle2D[2][1],shuffle2D[3][1],shuffle2D[4][1],shuffle2D[5][1],shuffle2D[6][1],shuffle2D[7][1],shuffle2D[8][1]]
      glyphMenu=Menu(glyphMenuOptions,self.player,IMG_PATH+"battleMenubackground.gif",glyphMenuImages,"Glyph Menu")
      glyphMenu.numPad=True
      glyphMenu.background.rect=(200,580,200,200)
      player.currentMenu=glyphMenu
      self.lightning.rect=(self.enemies[self.selEnemyIndex].sprite.rect.left+40,self.enemies[self.selEnemyIndex].sprite.rect.top+40,300,300)
      self.glyphGroup.add(self.lightning)

    elif name=="Missile":
	self.attack(self.player.battlePlayer,"Missile")
    elif name=="Heal":
      shuffle2D=[("Heal1",self.heal1btn),("Heal2",self.heal2btn),("Heal3",self.heal3btn),("Heal4",self.heal4btn),("Not",self.fire1btn),("Not",self.fire4btn),("Not",self.lightning3btn),("Not",self.lightning2btn),("Not",self.fire1btn)]
      shuffle(shuffle2D)
      glyphMenuOptions=[shuffle2D[0][0],shuffle2D[1][0],shuffle2D[2][0],shuffle2D[3][0],shuffle2D[4][0],shuffle2D[5][0],shuffle2D[6][0],shuffle2D[7][0],shuffle2D[8][0]]
      glyphMenuImages=[shuffle2D[0][1],shuffle2D[1][1],shuffle2D[2][1],shuffle2D[3][1],shuffle2D[4][1],shuffle2D[5][1],shuffle2D[6][1],shuffle2D[7][1],shuffle2D[8][1]]
      glyphMenu=Menu(glyphMenuOptions,self.player,IMG_PATH+"battleMenubackground.gif",glyphMenuImages,"Glyph Menu")
      glyphMenu.numPad=True
      glyphMenu.background.rect=(200,580,200,200)
      player.currentMenu=glyphMenu
      self.heal.rect=(500,300,300,300)
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
    if item.name=="Potion":
      self.attack(self.player.battlePlayer,"Heal")
      
    elif item.name=="Grenade":
      self.attack(self.player.battlePlayer,"Fire")
    else:
      self.doNothing()
    self.player.battlePlayer.eqItem.remove(item)

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
    #AvalAttacks = ListAttacks(enemy)
    #TODO:  make ListAttacks(enemy) return an array of strings based on enemy.name
    #       create random int (max of len(listAttacks))
    #       change line 1093 to enemy.attackPower(listAttacks[randint])
    #        add statements in enemy.attackPower defining powers of various attacks
    defender=self.player.battlePlayer
    defender.defendAttack(enemy.attackPower())
    self.playerTurn=True

    player.migrateMessages("Enemy attacks for "+repr(enemy.attackPower())+" damage")
    player.migrateMessages("Your HP is "+repr(defender.HP))
    #Fill in AI logic here to pick an attack, for now Math.random
    #return AvalAttacks(random.randrange((len(AvalAttacks)-1)))

  ###
  #Called when battle is over and player wins
  ##
  def Victory(self):
    #self.player.winScreen(self)
    self.player.currentRoom.en1=0
    self.player.currentRoom.en2=0
    self.player.currentRoom.en3=0
    self.player.currentRoom.en4=0
    self.player.battle=False
    self.player.traversal=True
    self.player.msg5="You Win!"
    #self.player.winScreen=True
    #Return to travesal system

  ###
  #Called when battle is over and player loses
  ###
  def Defeat(self):
    #self.player.defeatScreen=True
    self.player.battle=False
    self.player.currentMenu=self.player.MainMenu
    self.player.currentMenu.select("up")
    self.player.mainMenu=True	
    #end the game
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
          if player.currentMenu.numPad==True:
            for i in range(3):
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
          if player.currentMenu.numPad==True:
            for i in range(3):
              player.currentMenu.select("up")
          else:
            player.currentMenu.select("up")

        elif newKey=='[3]' or newKey=='backspace':
          #X
          player.currentMenu.regress(player)

        elif newKey=='[1]' or newKey=='return':
          #Check
          player.currentMenu.progress(player,screen)

        elif newKey=='[7]':
          #Square
          msg5='square'

        elif newKey=='[9]':
          msg5='circle'

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

# we'll use 36 pixel high text
fsize = 36

# create the window and keep track of the surface
# for drawing into
screen = pygame.display.set_mode(size)

# create a Font object from a file, or use the default
# font if the file name is None. size param is height
# in pixels
font = pygame.font.Font(None, fsize)
player=Player(0,0)

#state variables
player.inTutorial=False
player.traversal=False
player.waiting=False
player.battle=False
player.mainMenu=True
#player.statMenu=False

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
    #player.traversal=False
    #setImage(player)
    return("You enter room at "+repr(player.currentX)+", "+repr(player.currentY))

def setImage(player):
    fileName=""
    NORTH=1
    SOUTH=3
    EAST=0
    WEST=2
    ###Set up string for testing
    if player.playerFacing==NORTH:
        if player.currentRoom.doorN:
            fileName+="F"

        if player.currentRoom.doorW:
            fileName+="L"

        if player.currentRoom.doorE:
            fileName+="R"

    elif player.playerFacing==SOUTH:
        if player.currentRoom.doorS:
            fileName+="F"

        if player.currentRoom.doorE:
            fileName+="L"

        if player.currentRoom.doorW:
            fileName+="R"

    elif player.playerFacing==EAST:
        if player.currentRoom.doorE:
            fileName+="F"

        if player.currentRoom.doorN:
            fileName+="L"

        if player.currentRoom.doorS:
            fileName+="R"

    elif player.playerFacing==WEST:
        if player.currentRoom.doorW:
            fileName+="F"

        if player.currentRoom.doorS:
            fileName+="L"

        if player.currentRoom.doorN:
            fileName+="R"

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

def checkDoor(direction,player,screen):
    NORTH=1
    SOUTH=3
    EAST=0
    WEST=2
    currentX=player.currentX
    currentY=player.currentY
    playerFacing=player.playerFacing
    currentRoom=player.currentRoom

    if direction=='down': 
         print("down pressed")

    elif direction=='up':
         if playerFacing==NORTH:
            if currentRoom.doorN:
                return(enterRoom('north',player,screen))

            else:
                return("There is no door in front of you")

         elif playerFacing==SOUTH:
            if currentRoom.doorS:
                return(enterRoom('south',player,screen))

            else:
                return("There is no door in front of you")

         elif playerFacing==EAST:
            if currentRoom.doorE:
                return(enterRoom('east',player,screen))

            else:
                return("There is no door in front of you")

         elif playerFacing==WEST:
            if currentRoom.doorW:
                return(enterRoom('west',player,screen))

            else:
                return("There is no door in front of you")

    elif direction=='left':
        if playerFacing==NORTH:
            player.playerFacing=WEST
            #setImage(player)
            return('You are now facing West')

        elif playerFacing==SOUTH:
            player.playerFacing=EAST
            #setImage(player)
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
        menu.progress(player,screen)

      elif newKey=='[2]' or newKey=='down':
        menu.select("down")

      elif newKey=='[3]' or newKey=='backspace':
        menu.regress(player)

      elif newKey=='[4]' or newKey=='left':
        print("left")
        if menu.name=="Stats":
          menu.inventoryUp=not menu.inventoryUp

      elif newKey=='[5]':
        print('check')

      elif newKey=='[6]':
        print('right')

      elif newKey=='[7]':
        print('square')

      elif newKey=='[8]' or newKey=='up':
        menu.select("up")

      elif newKey=='[9]':
        print('circle')

def updateTraversal(event,player,screen):
    if event.type == QUIT:
      sys.exit()

    elif event.type == KEYDOWN:
      newKey=pygame.key.name(event.key)
      if newKey=='escape':
        sys.exit()

      elif newKey=='[1]':
        ##square
        player.migrateMessages('not implemented')

      elif newKey=='[2]':
        player.migrateMessages(checkDoor('down',player,screen))

      elif newKey=='[3]' or newKey=='space':
        ##x
        player.traversal=False
        player.mainMenu=True
        player.currentMenu=player.statsMenu
        player.previousMenu=player.statsMenu

      elif newKey=='[4]' or newKey=='left':
        player.migrateMessages(checkDoor('left',player,screen))

      elif newKey=='[5]':
        player.migrateMessages('check')

      elif newKey=='[6]' or newKey=='right':
        player.migrateMessages(checkDoor('right',player,screen))

      elif newKey=='[7]':
        player.migrateMessages('square')

      elif newKey=='[8]' or newKey=='up':
        player.migrateMessages(checkDoor('up',player,screen))

      elif newKey=='[9]':
        player.migrateMessages('circle')

def updateTutorial(event,player):
    if event.type == QUIT:
      sys.exit()

    elif event.type == KEYDOWN:
      newKey=pygame.key.name(event.key)

      if newKey=='escape':
        sys.exit()

      elif newKey=='[1]' or newKey=='right':
        player.tutorial.next()

      elif newKey=='[2]':
        player.migrateMessages('down')

      elif newKey=='[3]' or newKey=='left':
        player.tutorial.previous()

      elif newKey=='[4]' or newKey=='backspace':
        player.tutorial.previous()

      elif newKey=='[5]':
        player.migrateMessages('check')

      elif newKey=='[6]' or newKey=='return':
        player.tutorial.next()

      elif newKey=='[7]':
        player.migrateMessages('square')

      elif newKey=='[8]':
        player.migrateMessages('up')

      elif newKey=='[9]':
        player.migrateMessages('circle')

def updateWaiting(event,player):
  pygame.time.set_timer(USEREVENT+2,500)
  enemyList=[]
  player.traversal=False
  player.waiting=False
  if  not int(player.currentRoom.en1)==0:
    en=Enemy(player,player.currentRoom.en1)
    en.place=0
    enemyList.append(en)
  if  not int(player.currentRoom.en2)==0:
    en=Enemy(player,player.currentRoom.en2)
    en.place=1
    enemyList.append(en)
  if  not int(player.currentRoom.en3)==0:
    en=Enemy(player,player.currentRoom.en3)
    en.place=2
    enemyList.append(en)
  if  not int(player.currentRoom.en4)==0:
    en=Enemy(player,player.currentRoom.en4)
    en.place=3
    enemyList.append(en)
  if len(enemyList)>0:   
    player.migrateMessages('initiating battle...')
    player.traversal=False
    player.curBattle=BattleEngine(player,enemyList)
  if player.currentRoom.transport==True:
    player.nextDungeon()
def updateBattle(event,player):
  player.curBattle.Run(event,screen)

###Draw methods###
def drawTraversal(player,screen):
  setImage(player)

def drawWaiting(player,screen):
  screen.fill(0,(0,0,1290,700),0)

setImage(player)

while pippy.pygame.next_frame():

  for event in pygame.event.get():
    if event.type==USEREVENT+2:
      pygame.time.set_timer(USEREVENT+2,0)
      player.waiting=False
      if player.msg5=='Enemies are present, prepare to fight.':
        player.battle=True
      if player.battle==False:
        player.traversal=True
      setImage(player)
    if event.type==QUIT:
      sys.exit()
    if player.traversal:
      if player.waiting==True:
        updateWaiting(event,player)
      else:
        #################UPDATE##############################
        updateTraversal(event,player,screen)

    #elif player.statMenu:
      ##stat menu processes
      #updateStatMenu
     # print(player.stat)

    elif player.battle:
      ##battle processes
      updateBattle(event,player)

    elif player.mainMenu:
      ## main menu processes
      updateMenu(event,player)
    elif player.inTutorial:
      updateTutorial(event,player)

  ###############DRAW#########################
  #draw based on state
  if player.mainMenu:
    if player.currentMenu.name=="Inventory":
      player.currentMenu.draw(player,screen,player.currentMenu.sX,player.currentMenu.sY,40)
    else:
      player.currentMenu.draw(player,screen,400,500,50)
  else:
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
    if player.traversal:
      if player.waiting:
        drawWaiting(player,screen)
      else:
        drawTraversal(player,screen)
    #elif player.statMenu:
    #  drawStatMenu(player,screen)
    elif player.battle:
      player.curBattle.draw(player,screen)
    elif player.inTutorial:
      player.tutorial.draw(player.currentRoomGroup,screen)
  if player.traversal:
    player.currentRoomGroup.draw(screen)
    pygame.display.flip()
  # update the display
