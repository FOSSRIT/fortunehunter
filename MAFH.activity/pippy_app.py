import pippy, pygame, sys, math
from pygame.locals import *
from sugar.activity import activity
from time import time
import simplejson
import os.path

from Items import get_item, Item
from Enemy import get_enemy, Enemy
from Dungeon import Dungeon
from Puzzle import PuzzlePiece, PuzzleMap
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

#################################################################################
  #Map class: stores information about the layout of the dungeon for easy display
###############################################################################
class Map:
  def __init__(self,dgn):
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
  def drawMacro(self,player,screen):
    player.currentRoomGroup.draw(screen)
    #DRAW LEGEND
    font=pygame.font.SysFont("cmr10",24,False,False)
    macroMap=pygame.transform.scale(self.totalSurface,(self.sizeX*100,self.sizeY*100))
    screen.fill((0,0,0),(200,0,800,700))
    legend=pygame.Surface((200,300))
    legend.fill((255,0,0),(0,0,40,15))
    legend.blit(font.render("LOCKED",True,(255,0,0)),(45,0,30,5))
    legend.fill((150,255,150),(0,25,40,15))
    legend.blit(font.render("OPEN",True,(150,255,150)),(45,25,30,5))
    legend.fill((255,0,255),(0,50,40,15))
    legend.blit(font.render("PUZZLE",True,(255,0,255)),(45,50,30,5))
    legend.fill((255,255,255),(0,75,40,15))
    legend.blit(font.render("EXIT",True,(255,255,255)),(45,75,30,5))
    legend.fill((50,50,50),(0,100,40,15))
    legend.blit(font.render("ENTRANCE",True,(50,50,50)),(45,100,30,5))
    screen.blit(legend,(800,0,300,300))
    screen.blit(macroMap,(200,0,800,700))
    pygame.display.flip()
  def updateMacro(self,player):
    NONE=-1
    PUZZLE=0
    LOCKED=1
    BOTH=2
    UNLOCKED=3
    EXIT=4
    ENTRANCE=5
    self.totalSurface.fill((0,255,0),(player.currentX*40,player.currentY*40,38,38))
    if player.currentRoom.doorN:
      if player.currentRoom.doorNFlag==LOCKED:
        self.totalSurface.fill((255,0,0),(player.currentX*40+5,player.currentY*40,30,5))
      elif player.currentRoom.doorNFlag==UNLOCKED or player.currentRoom.doorNFlag==NONE:
        self.totalSurface.fill((150,255,150),(player.currentX*40+5,player.currentY*40,30,5))
      elif player.currentRoom.doorNFlag==PUZZLE:
        self.totalSurface.fill((255,0,255),(player.currentX*40+5,player.currentY*40,30,5))
      elif player.currentRoom.doorNFlag==BOTH:
        self.totalSurface.fill((255,0,0),(player.currentX*40+5,player.currentY*40,30,5))
      elif player.currentRoom.doorNFlag==EXIT:
        self.totalSurface.fill((255,255,255),(player.currentX*40+5,player.currentY*40,30,5))
      elif player.currentRoom.doorNFlag==ENTRANCE:
        self.totalSurface.fill((0,0,0),(player.currentX*40+5,player.currentY*40,30,5))
    if player.currentRoom.doorS:
      if player.currentRoom.doorSFlag==LOCKED:
        self.totalSurface.fill((255,0,0),(player.currentX*40+5,player.currentY*40+35,30,5))
      elif player.currentRoom.doorSFlag==UNLOCKED or player.currentRoom.doorSFlag==NONE:
        self.totalSurface.fill((150,255,150),(player.currentX*40+5,player.currentY*40+35,30,5))
      elif player.currentRoom.doorSFlag==PUZZLE:
        self.totalSurface.fill((255,0,255),(player.currentX*40+5,player.currentY*40+35,30,5))
      elif player.currentRoom.doorSFlag==BOTH:
        self.totalSurface.fill((255,0,0),(player.currentX*40+5,player.currentY*40+35,30,5))
      elif player.currentRoom.doorSFlag==EXIT:
        self.totalSurface.fill((255,255,255),(player.currentX*40+5,player.currentY*40+35,30,5))
      elif player.currentRoom.doorSFlag==ENTRANCE:
        self.totalSurface.fill((0,0,0),(player.currentX*40+5,player.currentY*40+35,30,5))
    if player.currentRoom.doorE:
      if player.currentRoom.doorEFlag==LOCKED:
        self.totalSurface.fill((255,0,0),(player.currentX*40+35,player.currentY*40+5,5,30))
      elif player.currentRoom.doorEFlag==UNLOCKED or player.currentRoom.doorEFlag==NONE:
        self.totalSurface.fill((150,255,150),(player.currentX*40+35,player.currentY*40+5,5,30))
      elif player.currentRoom.doorEFlag==PUZZLE:
        self.totalSurface.fill((255,0,255),(player.currentX*40+35,player.currentY*40+5,5,30))
      elif player.currentRoom.doorEFlag==BOTH:
        self.totalSurface.fill((255,0,0),(player.currentX*40+35,player.currentY*40+5,5,30))
      elif player.currentRoom.doorEFlag==EXIT:
        self.totalSurface.fill((255,255,255),(player.currentX*40+35,player.currentY*40+5,5,30))
      elif player.currentRoom.doorEFlag==ENTRANCE:
        self.totalSurface.fill((0,0,0),(player.currentX*40+35,player.currentY*40+5,5,30))
    if player.currentRoom.doorW:
      if player.currentRoom.doorWFlag==LOCKED:
        self.totalSurface.fill((255,0,0),(player.currentX*40,player.currentY*40+5,5,30))
      elif player.currentRoom.doorWFlag==UNLOCKED or player.currentRoom.doorWFlag==NONE:
        self.totalSurface.fill((150,255,150),(player.currentX*40,player.currentY*40+5,5,30))
      elif player.currentRoom.doorWFlag==PUZZLE:
        self.totalSurface.fill((255,0,255),(player.currentX*40,player.currentY*40+5,5,30))
      elif player.currentRoom.doorWFlag==BOTH:
        self.totalSurface.fill((255,0,0),(player.currentX*40,player.currentY*40+5,5,30))
      elif player.currentRoom.doorWFlag==EXIT:
        self.totalSurface.fill((255,255,255),(player.currentX*40,player.currentY*40+5,5,30))
      elif player.currentRoom.doorWFlag==ENTRANCE:
        self.totalSurface.fill((0,0,0),(player.currentX*40,player.currentY*40+5,5,30))

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


    sideDifference=self.sizeX-self.sizeY
    angle=angle*(math.pi/180)
    curSect=pygame.Rect(0,700,200,200)
    curSect.top+=((player.currentX*40-81)*math.cos(angle))-((player.currentY*40-81)*math.sin(angle))
    curSect.left-=((player.currentX*40-81)*math.sin(angle))+((player.currentY*40-81)*math.cos(angle))
    if player.playerFacing==EAST:
      curSect.top+=sideDifference*(40-81)
    elif player.playerFacing==SOUTH:
      curSect.left+=sideDifference*(40-81)
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
        self.player=player
        self.sX=0
        self.xY=0
        i=0
        for name in optionImageFiles:
            sprite=pygame.sprite.Sprite()
            if self.name=="Glyph Menu":
              if player.geomDifficulty==2:
                rotate=90*randint(0,3)
                sprite.image=pygame.transform.rotate(pygame.image.load(name),rotate)
              elif player.geomDifficulty==3:
                rotate=90*randint(0,3)
                flip=randint(0,2)
                sprite.image=pygame.transform.flip(pygame.transform.rotate(pygame.image.load(name),rotate),flip==1,flip==2)
              else:
                sprite.image=pygame.image.load(name)
            else:
              sprite.image=pygame.image.load(name)
            sprite.rectangle=pygame.Rect(0,0,1290,60)
            self.optionsImages.append(sprite)
            i+=1

        self.size=i

    def draw(self,player,screen,xStart,yStart,height):
        menuGroup=pygame.sprite.Group()
        if self.name=="Pause Menu":
          self.background.image.fill((255,255,255),(0,0,1200,900))
          self.background.image.set_alpha(20)
	bgGroup=pygame.sprite.Group(self.background)
        self.startX=xStart
        self.startY=yStart
        self.height=height
        if not self.name=="Inventory" and not self.name=="Defeat":
          bgGroup.draw(screen)
        i=0
        sel=0
        font=pygame.font.SysFont("cmr10",24,False,False)
        if self.numPad==False and not self.name=="Stats" and not self.name=="Inventory" and not self.name=="Victory":
          for image in self.optionsImages:
            if self.name=="Defeat":
              if i==self.currentOption:
                x=10
              else:
                x=0
              image.rect=pygame.Rect(xStart+(i*250),yStart-x,1290,height)
              i+=1
              menuGroup.add(image)
            else:
              if i==self.currentOption:
                image.rect=pygame.Rect(xStart+30,yStart+(i*height),1290,height)

              else:
                image.rect=pygame.Rect(xStart,yStart+(i*height),1290,height)
              menuGroup.add(image)
              i+=1
        elif self.numPad==True:
          ea=0
          if self.name=="GeomTut3" or self.name=="Glyph Menu":
            k=2
          else:
            k=3
          for image in self.optionsImages:
            if i==k:
              i=0
              yStart+=height
            if self.options[sel]=="Enter Answer" or self.options[sel]=="Enter":
              yStart+=height
              i=0
            image.rect=pygame.Rect(xStart+(i*height),yStart+ea,height,height)
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
          self.bgSurface=pygame.Surface((1200,700))
          player.currentRoomGroup.draw(self.bgSurface)
          bgGroup.draw(self.bgSurface)
          hp=font.render("HP: "+repr(player.battlePlayer.HP),True,(0,0,0))
          hpRect=pygame.Rect(635,425,200,42)
          self.bgSurface.blit(hp,hpRect)

          player.akhalSprite.rect=(600,350,50,50)
          akhalGroup=pygame.sprite.Group(player.akhalSprite)
          akhalGroup.draw(self.bgSurface)
          akhal=font.render(repr(player.battlePlayer.akhal),True,(0,0,0))
          akhalRect=pygame.Rect(650,375,200,42)
          self.bgSurface.blit(akhal,akhalRect)
          att=font.render("ATK: "+repr(player.battlePlayer.attackPower("basic")),True,(0,0,0))
          attRect=pygame.Rect(635,445,200,42)
          self.bgSurface.blit(att,attRect)
          defense=font.render("DEF: "+repr(player.battlePlayer.defensePower()),True,(0,0,0))
          defenseRect=pygame.Rect(635,465,200,42)
          self.bgSurface.blit(defense,defenseRect)
          #define rectangles
          weaponRect=pygame.Rect(635,500,200,42)
          self.optionsImages[0].rect=weaponRect
          armorRect=pygame.Rect(635,535,200,42)
          self.optionsImages[1].rect=armorRect
          accessoryRect=pygame.Rect(635,570,200,42)
          self.optionsImages[2].rect=accessoryRect
          itemRect=pygame.Rect(508,435,200,42)
          self.optionsImages[3].rect=itemRect
          item2Rect=pygame.Rect(508,475,200,42)
          self.optionsImages[4].rect=item2Rect
          item3Rect=pygame.Rect(508,525,200,42)
          self.optionsImages[5].rect=item3Rect
          item4Rect=pygame.Rect(508,565,200,42)
          self.optionsImages[6].rect=item4Rect
          self.optionsImages[self.currentOption].rect.top-=5
          self.optionsImages[self.currentOption].rect.width=115
          self.optionsImages[self.currentOption].rect.height=33
          self.bgSurface.fill((125,125,255),self.optionsImages[self.currentOption].rect)
	  #draw dynamic text
          if player.battlePlayer.weapon==None:
            wp="Weapon"
          else:
            wp=player.battlePlayer.weapon.name
          if player.battlePlayer.armor==None:
            arm="Armor"
          else:
            arm=player.battlePlayer.armor.name
          if player.battlePlayer.accessory==None:
            acc="Accessory"
          else:
            acc=player.battlePlayer.accessory.name
          it1,it2,it3,it4="","","",""
          if player.battlePlayer.eqItem[0]==None:
            it1="Empty"
          else:
            it1=player.battlePlayer.eqItem[0].name
          if player.battlePlayer.eqItem[1]==None:
            it2="Empty"
          else:
            it2=player.battlePlayer.eqItem[1].name
          if player.battlePlayer.eqItem[2]==None:
            it3="Empty"
          else:
            it3=player.battlePlayer.eqItem[2].name
          if player.battlePlayer.eqItem[3]==None:
            it4="Empty"
          else:
            it4=player.battlePlayer.eqItem[3].name


          weapon=font.render(wp,True,(0,0,0))
          self.bgSurface.blit(weapon,weaponRect)
          armor=font.render(arm,True,(0,0,0))
          self.bgSurface.blit(armor,armorRect)
          accessory=font.render(acc,True,(0,0,0))
          self.bgSurface.blit(accessory,accessoryRect)
          item1=font.render(it1,True,(0,0,0))
          self.bgSurface.blit(item1,itemRect)
          item2=font.render(it2,True,(0,0,0))
          self.bgSurface.blit(item2,item2Rect)
          item3=font.render(it3,True,(0,0,0))
          self.bgSurface.blit(item3,item3Rect)
          item4=font.render(it4,True,(0,0,0))
          self.bgSurface.blit(item4,item4Rect)
          
          screen.blit(self.bgSurface,(0,0,0,0))

          if player.invTutorial==False:
            k=0
            screen.fill((255,255,255),(0,0,400,400))
            lines=["This is the statistics screen.","Here, you can view information","about your character,","and any items, you have equipped.","As  you can see, there are slots for","weapon,armor,and accessory","as well as 4 slots for items.","To equip an item, select which slot","you want to equip to","and press enter or "] #draw check
            screen.blit(pygame.image.load(TOUR_PATH+"button/"+"buttonV.gif"),(225,375,40,40))
            for message in lines:
              screen.blit(font.render(message,True,(0,200,0)),(20,20+k,200,300))
              k+=40
        if self.name=="Inventory":
            y=0
            sel=0
            screen.blit(self.bgSurface,(0,0,0,0))
            screen.fill((100,100,255,.5),pygame.Rect(xStart,yStart,200,40*len(player.battlePlayer.inv_Ar)))
            for item in player.battlePlayer.inv_Ar:
              if sel==self.currentOption:
                screen.fill((50,50,250),pygame.Rect(self.sX,self.sY+y,200,40))
              screen.blit(font.render(item.name,True,(0,0,0)),pygame.Rect(self.sX,self.sY+y,200,40))
              y+=40
              sel+=1
              if player.invTutorial==False:
                screen.fill((250,250,250),(900,300,800,400))
                k=0
                lines=["This list shows the items","you are carrying.  To equip","an item in the current slot,","select one with the arrow","keys, and press enter or","      If the item cannot","be equipped in that","slot, you will be taken back","to the stats screen"]
                
                for message in lines:
                  screen.blit(font.render(message,True,(0,200,0)),(900,300+k,200,300))
                  k+=40
                screen.blit(pygame.image.load(TOUR_PATH+"button/"+"buttonV.gif"),(1165,460,40,40))
        if self.name=="Victory":
          self.bgSurface=pygame.Surface((1200,700))
          player.currentRoomGroup.draw(self.bgSurface)
          bgGroup.draw(self.bgSurface)
          screen.blit(self.bgSurface,(0,0,0,0))
          screen.blit(font.render("You Win!",True,(0,15,0)),(530,230,0,0))
          player.akhalSprite.rect=(530,300,50,50)
          akhalGroup=pygame.sprite.Group(player.akhalSprite)
          akhalGroup.draw(screen)
          screen.blit(font.render(repr(self.player.curBattle.checkValue()),True,(0,15,0)),(580,325,0,0))
          k=0
          for message in player.curBattle.battleItems:
            screen.blit(font.render(message,True,(0,15,0)),(520,350+k,200,300))
            k+=40
          pygame.display.flip()
        elif self.name=="Defeat":
          alphaLayer=pygame.image.load(ENV_PATH+"Black.gif")
          alphaLayer.set_alpha(10)
          screen.blit(alphaLayer,(0,0,1200,900))
          menuGroup.draw(screen)
          font=pygame.font.SysFont("cmr10",40,False,False)
          screen.blit(font.render("You have been defeated",True,(150,0,0)),(450,400,0,0))
          font=pygame.font.SysFont("cmr10",24,False,False)
          screen.blit(font.render("Continue",True,(150,0,0)),(520,515,0,0))
          screen.blit(font.render("Exit",True,(150,0,0)),(760,515,0,0))
          #draw player stats
          screen.blit(font.render("Multiplication problems right/wrong:",True,(150,0,0)),(20,20,0,0))
          screen.blit(font.render("Easy: "+repr(player.multiplicationStats[0][0])+"/"+repr(player.multiplicationStats[0][1]),True,(150,0,0)),(100,50,0,0))
          screen.blit(font.render("Medium: "+repr(player.multiplicationStats[1][0])+"/"+repr(player.multiplicationStats[1][1]),True,(150,0,0)),(100,80,0,0))
          screen.blit(font.render("Hard: "+repr(player.multiplicationStats[2][0])+"/"+repr(player.multiplicationStats[2][1]),True,(150,0,0)),(100,110,0,0))
          screen.blit(font.render("Fraction problems right/wrong:",True,(150,0,0)),(450,20,0,0))
          screen.blit(font.render("Easy: "+repr(player.divisionStats[0][0])+"/"+repr(player.divisionStats[0][1]),True,(150,0,0)),(530,50,0,0))
          screen.blit(font.render("Medium: "+repr(player.divisionStats[1][0])+"/"+repr(player.divisionStats[1][1]),True,(150,0,0)),(530,80,0,0))
          screen.blit(font.render("Hard: "+repr(player.divisionStats[2][0])+"/"+repr(player.divisionStats[2][1]),True,(150,0,0)),(530,110,0,0))
          screen.blit(font.render("Geometry problems right/wrong:",True,(150,0,0)),(830,20,0,0))
          screen.blit(font.render("Easy: "+repr(player.geometryStats[0][0])+"/"+repr(player.geometryStats[0][1]),True,(150,0,0)),(910,50,0,0))
          screen.blit(font.render("Medium: "+repr(player.geometryStats[1][0])+"/"+repr(player.geometryStats[1][1]),True,(150,0,0)),(910,80,0,0))
          screen.blit(font.render("Hard: "+repr(player.geometryStats[2][0])+"/"+repr(player.geometryStats[2][1]),True,(150,0,0)),(910,110,0,0))
          screen.blit(font.render("Puzzles solved:"+repr(player.puzzlesSolved),True,(150,0,0)),(400,160,0,0))

          screen.blit(font.render("Levels Beaten:  "+repr(player.dgnIndex),True,(150,0,0)),(600,160,0,0))
       
        elif self.name=="Pause Menu":
          menuGroup.draw(screen)
          font=pygame.font.SysFont("cmr10",40,False,False)
          screen.blit(font.render("Paused",True,(50,150,50)),(550,350,0,0))
          font=pygame.font.SysFont("cmr10",24,False,False)
          screen.blit(font.render("Multiplication problems right/wrong:",True,(50,150,50)),(20,20,0,0))
          screen.blit(font.render("Easy: "+repr(player.multiplicationStats[0][0])+"/"+repr(player.multiplicationStats[0][1]),True,(50,50,200)),(100,50,0,0))
          screen.blit(font.render("Medium: "+repr(player.multiplicationStats[1][0])+"/"+repr(player.multiplicationStats[1][1]),True,(50,50,200)),(100,80,0,0))
          screen.blit(font.render("Hard: "+repr(player.multiplicationStats[2][0])+"/"+repr(player.multiplicationStats[2][1]),True,(50,50,200)),(100,110,0,0))
          screen.blit(font.render("Fraction problems right/wrong:",True,(50,150,50)),(450,20,0,0))
          screen.blit(font.render("Easy: "+repr(player.divisionStats[0][0])+"/"+repr(player.divisionStats[0][1]),True,(50,50,200)),(530,50,0,0))
          screen.blit(font.render("Medium: "+repr(player.divisionStats[1][0])+"/"+repr(player.divisionStats[1][1]),True,(50,50,200)),(530,80,0,0))
          screen.blit(font.render("Hard: "+repr(player.divisionStats[2][0])+"/"+repr(player.divisionStats[2][1]),True,(50,50,200)),(530,110,0,0))
          screen.blit(font.render("Geometry problems right/wrong:",True,(50,150,50)),(830,20,0,0))
          screen.blit(font.render("Easy: "+repr(player.geometryStats[0][0])+"/"+repr(player.geometryStats[0][1]),True,(50,50,200)),(910,50,0,0))
          screen.blit(font.render("Medium: "+repr(player.geometryStats[1][0])+"/"+repr(player.geometryStats[1][1]),True,(50,50,200)),(910,80,0,0))
          screen.blit(font.render("Hard: "+repr(player.geometryStats[2][0])+"/"+repr(player.geometryStats[2][1]),True,(50,50,200)),(910,110,0,0))
          screen.blit(font.render("Puzzles solved:",True,(50,150,50)),(500,160,0,0))
          screen.blit(font.render(repr(player.puzzlesSolved),True,(50,50,200)),(670,160,0,0))
          x1=0
          x2=0
          x3=0
          x4=0
          if self.currentOption==0:
            x1=30
          elif self.currentOption==1:
            x2=30
          elif self.currentOption==2:
            x3=30
          elif self.currentOption==3:
            x4=30
          screen.blit(font.render("Save Game",True,(20,20,100)),(460+x1,410,0,0))
          screen.blit(font.render("Exit Game",True,(20,20,100)),(460+x2,460,0,0))
          screen.blit(font.render("Main Menu",True,(20,20,100)),(460+x3,510,0,0))
          screen.blit(font.render("Return to Game",True,(20,20,100)),(460+x4,560,0,0))

        elif self.name=="Options Menu":
          menuGroup.draw(screen)
          screen.blit(font.render("Critical Attack",True,(150,0,0)),(450+40,400+3,0,0))
          screen.blit(font.render("Special Attack",True,(150,0,0)),(450+40,400+53,0,0))
          screen.blit(font.render("Magic Attack",True,(150,0,0)),(450+40,400+103,0,0))
          screen.blit(font.render("Shop",True,(150,0,0)),(450+40,400+153,0,0))
          screen.blit(font.render("Back",True,(150,0,0)),(450+40,400+203,0,0))
        elif self.name=="Difficulty Menu":
          menuGroup.add(player.previousMenu.optionsImages)
          menuGroup.draw(screen)
          screen.blit(font.render("Critical Attack",True,(150,0,0)),(450+40,400+3,0,0))
          screen.blit(font.render("Special Attack",True,(150,0,0)),(450+40,400+53,0,0))
          screen.blit(font.render("Magic Attack",True,(150,0,0)),(450+40,400+103,0,0))
          screen.blit(font.render("Shop",True,(150,0,0)),(450+40,400+153,0,0))
          screen.blit(font.render("Back",True,(150,0,0)),(450+40,400+203,0,0))
          screen.blit(font.render("Disabled",True,(150,0,0)),(player.currentMenu.sX+40,player.currentMenu.sY+3,0,0))
          screen.blit(font.render("Easy",True,(150,0,0)),(player.currentMenu.sX+40,player.currentMenu.sY+43,0,0))
          screen.blit(font.render("Medium",True,(150,0,0)),(player.currentMenu.sX+40,player.currentMenu.sY+83,0,0))
          screen.blit(font.render("Hard",True,(150,0,0)),(player.currentMenu.sX+40,player.currentMenu.sY+123,0,0))
      
        if self.name=="AtkTut":
          screen.fill((255,255,255),(600,400,400,300))
          lines=["To perform a basic attack","select the attack button"]
          y=0
          for message in lines:
            screen.blit(font.render(message,True,(0,200,0)),(600,400+y,400,300))
            y+=40
        elif self.name=="CritTut":
          screen.fill((255,255,255),(600,400,400,300))
          lines=["Sometimes, when performing a","basic attack, you will get","a critical hit!  When this happens,","you must solve a multiplication","problem before the green timer runs","out.  Press any key on the calculator","to continue"]
          y=0
          for message in lines:
            screen.blit(font.render(message,True,(0,200,0)),(600,400+y,400,300))
            y+=40
        elif self.name=="DivTut":
          screen.fill((255,255,255),(600,400,400,300))
          lines=["To perform a special attack,","select the special button"]
          y=0
          for message in lines:
            screen.blit(font.render(message,True,(0,200,0)),(600,400+y,400,300))
            y+=40
        elif self.name=="DivTut2":
          screen.fill((255,255,255),(700,400,400,300))
          lines=["In special attack, you","must power up your sword.","Select how much power","to add to your sword.","If the power is exactly 1","you will attack for 1.5X damage","Otherwise, it will miss"]
          y=0
          for message in lines:
            screen.blit(font.render(message,True,(0,200,0)),(700,400+y,400,300))
            y+=40
        elif self.name=="GeomTut":
          screen.fill((255,255,255),(600,400,400,300))
          lines=["To cast a magic spell,","select the magic button"]
          y=0
          for message in lines:
            screen.blit(font.render(message,True,(0,200,0)),(600,400+y,400,300))
            y+=40
        elif self.name=="GeomTut2":
          screen.fill((255,255,255),(600,400,400,300))
          lines=["Different spells have different","effects.  Try casting fire."]
          y=0
          for message in lines:
            screen.blit(font.render(message,True,(0,200,0)),(600,400+y,400,300))
            y+=40
        elif self.name=="GeomTut3":
          screen.fill((255,255,255),(800,400,400,300))
          glyphSprite=pygame.sprite.Sprite()
          glyphSprite.image=pygame.image.load(PUZZLE_PATH+"FireGlyph.gif")
          glyphSprite.rect=pygame.Rect(500,350,300,300)
          glyphGroup=pygame.sprite.Group(glyphSprite)
          glyphGroup.draw(screen)
          lines=["When casting magic,","you must select pieces","which match parts of the","glyph on screen.","Select one to continue"]
          y=0
          for message in lines:
            screen.blit(font.render(message,True,(0,200,0)),(800,400+y,400,300))
            y+=40
        elif self.name=="ItemTut":
          screen.fill((255,255,255),(600,400,400,300))
          lines=["You can equip certain items","to use in battle from the","inventory screen.  Items can be","used in many different ways.","Select Use Item to test your","skills in a real battle"]
          y=0
          for message in lines:
            screen.blit(font.render(message,True,(0,200,0)),(600,400+y,400,300))
            y+=40

        if not self.name=="Defeat" and not self.name=="Difficulty Menu" and not self.name=="Options Menu" and not self.name=="Pause Menu":
          menuGroup.draw(screen)
        if self.name=="Main Menu":
          screen.blit(font.render("Continue",True,(150,0,0)),(450+40,400+103,0,0))
          screen.blit(font.render("Options",True,(150,0,0)),(450+40,400+153,0,0))
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
            player.currentMenu.sX=player.previousMenu.startX+200
            player.currentMenu.sY=player.previousMenu.startY+player.previousMenu.currentOption*player.previousMenu.height
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
            player.playerFacing=1
            player.traversal=False
            player.mainMenu=False
            player.startComic(FMC_PATH+"FMC1/",None)
            player.inComic=True
            pygame.display.flip()

        elif name=="Close":
            sys.exit()
        elif name=="Save":
          dataList=player.toString()
          FILE=open(os.path.join(activity.get_activity_root(),"data/"+player.name+".txt"),"w")
          FILE.write(simplejson.dumps(dataList))
          FILE.close()
          #do save stuff
        elif name=="Main Menu":
          player.traversal=False
          player.currentMenu=player.MainMenu
          player.mainMenu=True
        elif name=="Return to Game":
          player.traversal=True
          player.mainMenu=False
        elif name=="Tutorial":
            player.inTutorial=True
            player.inComic=True
            player.mainMenu=False
            player.startComic(TOUR_PATH+"setup/",None)
        elif name=="Disabled":
          if player.previousMenu.currentOption==0:
            player.critDifficulty=0
          elif player.previousMenu.currentOption==1:
            player.divDifficulty=0
          elif player.previousMenu.currentOption==2:
            player.geomDifficulty=0
          elif player.previousMenu.currentOption==3:
            player.shopDifficulty=1
          player.currentMenu=player.previousMenu
        elif name=="Easy":
          if player.previousMenu.currentOption==0:
            player.critDifficulty=1
          elif player.previousMenu.currentOption==1:
            player.divDifficulty=1
          elif player.previousMenu.currentOption==2:
            player.geomDifficulty=1
          elif player.previousMenu.currentOption==3:
            player.shopDifficulty=1
          player.currentMenu=player.previousMenu
        elif name=="Medium":
          if player.previousMenu.currentOption==0:
            player.critDifficulty=2
          elif player.previousMenu.currentOption==1:
            player.divDifficulty=2
          elif player.previousMenu.currentOption==2:
            player.geomDifficulty=2
          elif player.previousMenu.currentOption==3:
            player.shopDifficulty=2
          player.currentMenu=player.previousMenu
        elif name=="Hard":
          if player.previousMenu.currentOption==0:
            player.critDifficulty=3
          elif player.previousMenu.currentOption==1:
            player.divDifficulty=3
          elif player.previousMenu.currentOption==2:
            player.geomDifficulty=3
          elif player.previousMenu.currentOption==3:
            player.shopDifficulty=2
          player.currentMenu=player.previousMenu
        elif name=="Load Game":
           FILE=open(os.path.join(activity.get_activity_root(),"data/"+player.name+".txt"),"r")
           data=simplejson.loads(FILE.read())
           print(data)
           player.fromData(data)
           
           player.dgnMap.updateMacro(player)
           player.traversal=True
           player.mainMenu=False
           setImage(player)
           player.currentRoomGroup.draw(screen)
           pygame.display.flip()

        elif name=="Return":
          player.currentMenu.currentOption=0
          player.currentMenu=player.MainMenu
        elif name=="Attack":
          if player.critDifficulty>0:
            seed()
            crit=randint(0,2)
            if crit==1:
              player.curBattle.critical(player)
            else:
              player.curBattle.attack(player.battlePlayer,"basic")
          else:
            player.curBattle.attack(player.battlePlayer,"basic")
        elif name=="0" or name=="1"or name=="2" or name=="3" or name=="4" or name=="5" or name=="6" or name=="7"or name=="8"or name=="9":
          if len(player.battlePlayer.currentInput)<7:
            player.battlePlayer.currentInput+=name
        elif name=="Clear":
          player.battlePlayer.currentInput=""
        elif name=="Enter Answer":
          if not player.battlePlayer.currentInput =="":
            if player.battlePlayer.currentAnswer==int(player.battlePlayer.currentInput):
              player.curBattle.attack(player.battlePlayer,"critical")
            else:
              tup=self.player.multiplicationStats[self.player.critDifficulty-1]
              tup=(tup[0],tup[1]+1)
              self.player.multiplicationStats[self.player.critDifficulty-1]=tup
              player.curBattle.attack(player.battlePlayer,"basic")
          else:
            tup=self.player.multiplicationStats[self.player.critDifficulty-1]
            tup=(tup[0],tup[1]+1)
            self.player.multiplicationStats[self.player.critDifficulty-1]=tup
            player.curBattle.attack(player.battlePlayer,"basic")
        elif name=="Division": 
          player.curBattle.divisionAttack()
        elif name[1:2]=="/":
	  player.battlePlayer.fractionSum += float(name[0])/float(name[2])
	  player.curBattle.checkFraction()
        elif name=="Geometry":
          player.curBattle.magic(player)
        elif name=="Fire" or name=="Lightning" or name=="Heal" or name=="Missile":
          player.battlePlayer.currentProb1=""
          player.battlePlayer.currentProb2=""
          player.battlePlayer.currentInput=""
          player.curBattle.startGlyph(name)
	elif name=="Fire1" or name=="Fire2" or name=="Fire3" or name=="Fire4" or name=="Heal1" or name=="Heal2" or name=="Heal3" or name=="Heal4" or name=="Lightning1" or name=="Lightning2" or name=="Lightning3" or name=="Lightning4" or name=="Missile1" or name=="Missile2" or name=="Missile3" or name=="Missile4":
	  player.curBattle.checkGlyph(name)
        elif name=="Scan":
          player.curBattle.scanEnemy()
        elif name=="Item1" or name=="Item2" or name=="Item3" or name=="Item4":
          index=int(repr(name)[5])-1
          if index<len(player.battlePlayer.eqItem):
            player.curBattle.useItem(player.battlePlayer.eqItem[index])
          else:
            player.currentMenu=player.curBattle.battleMenu
	  #if we decide to add puzzle/minigame items, here's where they'd go
        elif name=="Weapon" or name=="Armor" or name=="Accessory" or name=="ItemSlot1" or name=="ItemSlot2" or name=="ItemSlot3" or name=="ItemSlot4":
          self.createInventory(player,name)
          player.currentMenu=self.inventoryMenu
          player.currentRoomGroup.draw(screen)
        elif name[0:9]=="Equipment":
          player.battlePlayer.equip(player.battlePlayer.inv_Ar[int(name[9:10])],self.target)
          player.invTutorial=True
          player.currentMenu=player.statsMenu
          player.currentRoomGroup.draw(screen)
        elif name=="Wrong":
          print("Wrong choice")
        elif name=="Enter":
          player.currentMenu=player.divMenu
        elif name=="Not":
          player.migrateMessages("Incorrect glyph.  Spell fizzles")
          tup=self.player.divisionStats[self.player.divDifficulty-1]
          tup=(tup[0],tup[1]+1)
          self.player.divisionStats[self.player.divDifficulty-1]=tup
          player.curBattle.glyphGroup.empty()
          player.curBattle.glyphOverlayGroup.empty()
          player.curBattle.playerTurn=False
          player.currentMenu=player.curBattle.battleMenu
        elif name=="Continue":
          player.mainMenu=False
          player.traversal=True
          player.battlePlayer.akhal+=player.curBattle.enemyValue
        elif name=="LoseContinue":
            player.dgnIndex-=1
            player.currentX=0
            player.currentY=0
            player.playerFacing=1
            player.nextDungeon(True)
            player.dgnMap.updateMacro(player)
            player.traversal=True
            player.mainMenu=False
            setImage(player)
            player.battlePlayer.MHP-=2
            player.battlePlayer.HP=player.battlePlayer.MHP
            player.currentRoomGroup.draw(screen)
            pygame.display.flip()
        elif name=="LoseExit":
	    for i in range(6):
              player.migrateMessages("")
            player.__init__(0,0)
            player.traversal=False
            player.mainMenu=True
            player.currentMenu=player.MainMenu
            player.currentMenu.draw(player,screen,0,0,45)
            pygame.display.flip()
	else:
	    sys.exit()

    def createInventory(self,player,name):
      invOptions=[]
      invImages=[]
      i=0
      for item in player.battlePlayer.inv_Ar:
        invOptions.append("Equipment"+repr(i))
        i+=1
        invImages.append(MENU_PATH+"Blank.gif")
      self.inventoryMenu=Menu(invOptions,player,MENU_PATH+"PauseMenuBackground.gif",invImages,"Inventory")
      self.inventoryMenu.sX=self.optionsImages[self.currentOption].rect.left+50
      self.inventoryMenu.sY=self.optionsImages[self.currentOption].rect.top
      self.inventoryMenu.background.rect.top=10
      self.inventoryMenu.target=name
      self.inventoryMenu.bgSurface=self.bgSurface
      player.currentMenu=self.inventoryMenu

######################################################################
#Comic Class: stores an image list and possible BGM, traverses through list and tries to play BGM
######################################################################
class Comic:
    def __init__(self,Folder,BGM):
        self.currentIndex = 0
        self.images=[]
        #load images into sprites
        i=0
        for image in os.listdir(Folder):
          spt=pygame.sprite.Sprite()
          spt.image=pygame.image.load(Folder+image)
          spt.rect=pygame.Rect(0,0,1200,900)
	  self.images.append(spt)
          i+=1

       	self.size=i
        #try to load music
        if BGM != None:
          pygame.mixer.muxic.stop()
          pygame.mixer.music.load(SOUND_PATH+BGM)
          pygame.mixer.music.play(-1)

    def next(self,player):
    	if  self.currentIndex < self.size - 1:
       	  self.currentIndex+=1

    	else:
          player.stopComic()

    def previous(self):
      if self.currentIndex > 0:
        self.currentIndex-=1

      else:
        self.currentIndex=0

    def draw(self,screen):
        screen.blit(self.images[self.currentIndex].image,(0,0,1200,900))
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
    difficultyMenuImages=[MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif"]
    difficultyMenuOptions=["Disabled","Easy","Medium","Hard"]
    difficultyMenu=Menu(difficultyMenuOptions,self,MENU_PATH+"mafh_splash.gif",difficultyMenuImages,"Difficulty Menu")

    optionsMenuImages=[MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif"]
    optionsMenuOptions=[difficultyMenu,difficultyMenu,difficultyMenu,difficultyMenu,"Return"]
    optionsMenu=Menu(optionsMenuOptions,self,MENU_PATH+"mafh_splash.gif",optionsMenuImages,"Options Menu")

    mainMenuImages=[MENU_PATH+"TutorialButton.gif",MENU_PATH+"NewGameButton.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"CloseButton.gif"]
    self.MainMenu=Menu(["Tutorial","New Game","Load Game",optionsMenu,"Close"],self,MENU_PATH+"mafh_splash.gif",mainMenuImages,"Main Menu")
    
    statMenuOptions=["Weapon","Armor","Accessory","ItemSlot1","ItemSlot2","ItemSlot3","ItemSlot4"]
    statMenuImages=[MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif", MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif"]
    self.statsMenu=Menu(statMenuOptions,self,MENU_PATH+"PauseMenuBackground.gif",statMenuImages,"Stats")
    self.statsMenu.background.rect.top=10

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
        
        self.player=player
	self.weapon=None
	self.armor=None
	self.accessory=None
        self.eqItem=[]			#player can equip up to 4 usable items to use in battle
	self.inv_Ar 	= []		#inventory
	self.attacks_Ar = []		#associated array for attack string names and attack power values
        self.currentInput=""
        self.currentProb1=0
        self.currentProb2=0
        self.currentAnswer=0
        self.fractionSum=0
        self.akhal=0

        amulet=get_item('1')
        calculator=get_item('s')
        emptyItem=None
        self.eqItem=[emptyItem,emptyItem,emptyItem,emptyItem]
        self.inv_Ar=[amulet,calculator]

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
      return (self.ATT+self.BAE+self.BAB)*1.5
    elif name=="Missile":
      return self.ATT+self.BAB

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
    if self.HP>self.MHP:
      self.HP=self.MHP
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
      if not self.weapon==None:
        self.inv_Ar.append(self.weapon)
      self.weapon=item
      self.inv_Ar.remove(item)
      self.BAE=item.power
    elif target=="Armor" and item.type=="Armor":
      if not self.armor==None:
        self.inv_Ar.append(self.armor)
      self.armor=item
      self.inv_Ar.remove(item)
      self.BDE=item.power
    elif target=="Accessory" and item.type=="Accessory":
      if not self.accessory==None:
        self.inv_Ar.append(self.accessory)
      self.accessory=item
      self.inv_Ar.remove(item)
      self.BHP=item.power
    elif target[0:8]=="ItemSlot" and item.type=="Usable":
        for i in range(len(self.eqItem)-1,3):
          self.eqItem.append(None)
        if not self.eqItem[int(target[8])-1]==None:
          self.inv_Ar.append(self.eqItem[int(target[8])-1])
        self.inv_Ar.remove(item)
        self.eqItem[int(target[8])-1]=item


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
        divisionOptions=["1/"+repr(denom1),"1/"+repr(denom2),"1/"+repr(denom3),"1/"+repr(denom4)]
        divisionBackground=MENU_PATH+"battleMenubackground.gif"
        divisionOptImg=[MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif"]
        self.divisionMenu=Menu(divisionOptions,player,divisionBackground,divisionOptImg,"Division Menu")
        self.divisionMenu.background.rect=(0,300,200,200) 
      elif player.divDifficulty==3:
        denom1=randint(2,9)
        denom2=randint(2,9)
        denom3=randint(2,9)
        denom4=randint(2,9)
        num1=randint(1,4)
        num2=randint(1,4)
        num3=randint(1,4)
        num4=randint(1,4)
        divisionOptions=[repr(num1)+"/"+repr(denom1),repr(num2)+"/"+repr(denom2),repr(num3)+"/"+repr(denom3),repr(num4)+"/"+repr(denom4)]
        divisionBackground=MENU_PATH+"battleMenubackground.gif"
        divisionOptImg=[MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif"]
        self.divisionMenu=Menu(divisionOptions,player,divisionBackground,divisionOptImg,"Division Menu")
        self.divisionMenu.background.rect=(0,300,200,200) 

    itemOptions=["Item1","Item2","Item3","Item4"]
    itemBackground=MENU_PATH+"battleMenubackground.gif"
    itemOptImg=[MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif",MENU_PATH+"Blank.gif"]
    
    self.itemMenu=Menu(itemOptions,player,itemBackground,itemOptImg,"Item")
    self.itemMenu.background.rect=(0,300,200,200)

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
      player.currentMenu.draw(player,screen,235,450,45)
      if player.currentMenu.name=="Item":
        i=0
        for image in player.currentMenu.optionsImages:
          if i<len(player.battlePlayer.eqItem):
            font = pygame.font.Font(None, 36)
            if player.battlePlayer.eqItem[i]!=None:
              t=font.render(player.battlePlayer.eqItem[i].name,True,(255,255,255))
              screen.blit(t,image.rect) 
            i+=1     
      elif player.currentMenu.name=="Division Menu" or player.currentMenu.name=="DivTut2":
        screen.fill((0,0,0),(500,300,100,400))
        screen.fill((255,150,0),(500,(620-310*player.battlePlayer.fractionSum),137,310*player.battlePlayer.fractionSum))
        y=460
        font=pygame.font.SysFont("cmr10",24,False,False)
        if not player.currentMenu.name=="DivTut2":
          for item in player.currentMenu.options:
            screen.blit(font.render(item,True,(50,0,150)),(275,y,400,40))
            y+=45
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
      
      #screen.fill((50,250,50),pygame.Rect(200,50,self.timeBonus*500,50))
      if self.timeBonus>1:
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

    if temp < 6:
      defender.defendAttack(enemy.attackPower("critical"))
      player.migrateMessages("Enemy "+repr(enemy.name)+" "+repr(enemy.place)+" critical attacks for "+repr(enemy.attackPower("critical"))+" damage")
    elif temp > 90:
      defender.defendAttack(enemy.attackPower("special"))
      player.migrateMessages("Enemy "+repr(enemy.name)+" "+repr(enemy.place)+" critical attacks for "+repr(enemy.attackPower("critical"))+" damage")
    #print special message differently depending on name
    if enemy.name == "Wizard":
      defender.defendAttack(enemy.attackPower("critical"))
      player.migrateMessages("Wizard "+repr(enemy.place)+" casts Divide By Zero, and blasts you for "+repr(enemy.attackPower("special"))+" damage")
    elif enemy.name == "Goblin" or enemy.name == "Orc":
      defender.defendAttack(enemy.attackPower("critical"))
      player.migrateMessages("Goblin "+repr(enemy.place)+" head bonks you for "+repr(enemy.attackPower("special"))+" damage. Ouch!")
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
        menu.progress(player,screen)

      elif newKey=='[2]' or newKey=='down':
        menu.select("down")

      elif newKey=='[3]' or newKey=='backspace' or newKey=='i':
        if menu.name=="Stats" or menu.name=="Inventory":
          menu.regress(player)
        elif menu.name=="Pause Menu":
          player.traversal=True
          player.mainMenu=False
        

      elif newKey=='[4]' or newKey=='left':
        if menu.name=="Defeat":
          menu.select("up")
        elif menu.name=="Stats":
          for i in range(4):
            menu.select("down")
      elif newKey=='[5]':
        print('check')

      elif newKey=='[6]' or newKey=='right':
        if menu.name=="Defeat":
          menu.select("down")
        elif menu.name=="Stats":
          for i in range(4):
            menu.select("up")
      elif newKey=='[7]' or newKey=='e':
        #USE ITEM
        itemIndex=menu.currentOption
        if itemIndex>2 and itemIndex-3<len(player.battlePlayer.eqItem):
          item=player.battlePlayer.eqItem[itemIndex-3]
          if not item==None and item.type=="Usable":
            player.battlePlayer.HP+=int(player.battlePlayer.MHP*item.power)
            player.battlePlayer.eqItem[player.battlePlayer.eqItem.index(item)]=None
            if player.battlePlayer.HP>player.battlePlayer.MHP:
              player.battlePlayer.HP=player.battlePlayer.MHP
      elif newKey=='[8]' or newKey=='up':
        menu.select("up")

      elif newKey=='[9]' or newKey=='u':
        if menu.name=="Stats":
         #UNEQUIP ITEM
          itemIndex=menu.currentOption
          if itemIndex==0:
            player.battlePlayer.remEquipment(player.battlePlayer.weapon)
          elif itemIndex==1:
            player.battlePlayer.remEquipment(player.battlePlayer.armor)
          elif itemIndex==2:
            player.battlePlayer.remEquipment(player.battlePlayer.accessory)
          elif itemIndex-3<len(player.battlePlayer.eqItem):
            player.battlePlayer.remEquipment(player.battlePlayer.eqItem[itemIndex-3])
          player.currentMenu=player.statsMenu
          player.currentRoomGroup.draw(screen)

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
        if player.currentX==0 and player.currentY==2 and player.battleTutorial==False:
          player.traversal=False
          player.battle=True
          player.curBattle=BattleEngine(player,[get_enemy( '3' )])
          player.initInGameBattleTutorial(screen)
        elif player.currentX==1 and player.currentY==4 and player.movTutorial==False:
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
    if player.currentMenu.name=="Inventory":
      player.currentMenu.draw(player,screen,player.currentMenu.sX,player.currentMenu.sY,40)
    elif player.currentMenu.name=="Stats":
      player.currentMenu.draw(player,screen,450,400,50)
      drawTextBox(player,screen)
    elif player.currentMenu.name=="Difficulty Menu":
      player.currentMenu.draw(player,screen,player.currentMenu.sX,player.currentMenu.sY,40)
    elif player.currentMenu.name=="Defeat":
      player.currentMenu.draw(player,screen,500,500,50)
      
    else:
      player.currentMenu.draw(player,screen,450,400,50)
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




