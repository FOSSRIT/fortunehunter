#Player Class: stores info about the player ie. current position in dungeon etc

#########################################################################
import pippy, pygame, sys, math
from enemy import *
from hero import *
from battleEngine import *
from menu import *
from dungeon import *
from map import *
from room import *
from tutorial import *
from item import *
from pygame.locals import *
from random import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

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
    self.tutorial=Tutorial(tutorialImages)

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

