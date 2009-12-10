#Meno class:  contains a list of options (which can be other menus)
#               has a background image as well as images for each option
###########################################################################
import pippy, pygame, sys, math
from player import *
from hero import * 
from enemy import *
from exFunctions import *
from battleEngine import *
from dungeon import *
from map import *
from room import *
from tutorial import *
from item import *
from pygame.locals import *
from random import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

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
        if self.numPad==False and not self.name=="Stats":
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
          att=font.render("Attack: "+repr(player.battlePlayer.ATT),True,(0,0,0))
          attRect=pygame.Rect(210,370,200,42)
          screen.blit(att,attRect)
          defense=font.render("Defense: "+repr(player.battlePlayer.DEF),True,(0,0,0))
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
          weapon=font.render(player.battlePlayer.weapon.name,True,(0,0,0))
          screen.blit(weapon,weaponRect)
          armor=font.render(player.battlePlayer.armor.name,True,(0,0,0))
          screen.blit(armor,armorRect)
          accessory=font.render(player.battlePlayer.accessory.name,True,(0,0,0))
          screen.blit(accessory,accessoryRect)
          item1=font.render(player.battlePlayer.eqItem[0].name,True,(0,0,0))
          screen.blit(item1,itemRect)
          item2=font.render(player.battlePlayer.eqItem[1].name,True,(0,0,0))
          screen.blit(item2,item2Rect)
          item3=font.render(player.battlePlayer.eqItem[2].name,True,(0,0,0))
          screen.blit(item3,item3Rect)
          item4=font.render(player.battlePlayer.eqItem[3].name,True,(0,0,0))
          screen.blit(item4,item4Rect)

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
            self.halfSprite.image=pygame.image.load(IMG_PATH+"12pie.gif")
            player.curBattle.divArray[0] = 1
            player.curBattle.checkFraction()
        elif name=="1/3":
          player.battlePlayer.fractionSum += .33
          self.thirdSprite.image=pygame.image.load(IMG_PATH+"13pie.gif")
          player.curBattle.divArray[1] = 1
          player.curBattle.checkFraction()
        elif name=="1/4":
          player.battlePlayer.fractionSum += .25
          self.quarterSprite.image=pygame.image.load(IMG_PATH+"14pie.gif")
          player.curBattle.divArray[2] = 1
          player.curBattle.checkFraction()
        elif name=="1/6":
          player.battlePlayer.fractionSum += .166
          self.sixthSprite.image=pygame.image.load(IMG_PATH+"16pie.gif")
          player.curBattle.divArray[3] = 1
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
            player.currentMenu=player.curBattle.itemMenu
        elif name=="Item1" or name=="Item2" or name=="Item3" or name=="Item4":
            index=int(repr(name)[5])-1
            if index<len(player.battlePlayer.eqItem):
                player.curBattle.useItem(player.battlePlayer.eqItem[int(repr(name)[5])-1])
            else:
                player.currentMenu=player.curBattle.battleMenu
	      #if we decide to add puzzle/minigame items, here's where they'd go
        elif name=="Weapon" or name=="Armor" or name=="Accessory" or name=="ItemSlot1" or name=="ItemSlot2" or name=="ItemSlot3" or name=="ItemSlot4":
            player.currentMenu=player.statsMenu
        else:
          sys.exit()

