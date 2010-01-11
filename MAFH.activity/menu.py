import pippy, pygame, sys, math
from player import *
from exFunctions import *
from item import *
from pygame.locals import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

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
            sprite.image=pygame.image.load(name)
            sprite.rectangle=pygame.Rect(0,0,1290,60)
            self.optionsImages.append(sprite)
            i+=1

        self.size=i

    def draw(self,player,screen,xStart,yStart,height):
        menuGroup=pygame.sprite.Group()
	bgGroup=pygame.sprite.Group(self.background)
        if not self.name=="Inventory":
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
          if player.battlePlayer.weapon.name=="":
            wp="Weapon"
          else:
            wp=player.battlePlayer.weapon.name
          if player.battlePlayer.armor.name=="":
            arm="Armor"
          else:
            arm=player.battlePlayer.armor.name
          if player.battlePlayer.accessory.name=="":
            acc="Accessory"
          else:
            acc=player.battlePlayer.accessory.name
          it1,it2,it3,it4="","","",""
          if len(player.battlePlayer.eqItem)>0:
            it1=player.battlePlayer.eqItem[0].name
          if len(player.battlePlayer.eqItem)>1:
            it2=player.battlePlayer.eqItem[1].name
          if len(player.battlePlayer.eqItem)>2:
            it3=player.battlePlayer.eqItem[2].name
          if len(player.battlePlayer.eqItem)==4:
            if player.battlePlayer.eqItem[0].name=="":
              it1="Item 1"
            else:
              it1=player.battlePlayer.eqItem[0].name
            if player.battlePlayer.eqItem[1].name=="":
              it2="Item 2"
            else:
              it2=player.battlePlayer.eqItem[1].name
            if player.battlePlayer.eqItem[2].name=="":
              it3="Item 3"
            else:
              it3=player.battlePlayer.eqItem[2].name
            if player.battlePlayer.eqItem[3].name=="":
              it4="Item 4"
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
            lines=["This is the statistics screen.","Here, you can view information","about your character,","and any items, you have equipped.","As  you can see, there are slots for","weapon,armor,and accessory","as well as 4 slots for items.","To equip an item, select which slot","you want to equip to","and press enter or check"]
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
                lines=["This list shows the items","you are carrying.  To equip","an item in the current slot,","select one with the arrow","keys, and press enter or","check.  If the item cannot","be equipped in that","slot, you will be taken back","to the stats screen"]
                for message in lines:
                  screen.blit(font.render(message,True,(0,200,0)),(900,300+k,200,300))
                  k+=40
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
          screen.fill((0,0,0),(0,0,1200,900))
          menuGroup.draw(screen)
          screen.blit(font.render("You have been defeated",True,(150,0,0)),(400,400,0,0))
          screen.blit(font.render("Continue",True,(150,0,0)),(470,515,0,0))
          screen.blit(font.render("Exit",True,(150,0,0)),(710,515,0,0))
          #draw continue/exit text
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
          glyphSprite.image=pygame.image.load(IMG_PATH+"FireGlyph.gif")
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
        if not self.name=="Defeat":
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
            player.playerFacing=1
            player.nextDungeon()
            player.dgnMap.updateMacro(player)
            player.traversal=True
            player.mainMenu=False
            setImage(player)
            player.battlePlayer=Hero(player)
            player.currentRoomGroup.draw(screen)
            player.initMovTutorial(screen)
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
            player.curBattle.useItem(player.battlePlayer.eqItem[index])
          else:
            player.currentMenu=player.curBattle.battleMenu
	  #if we decide to add puzzle/minigame items, here's where they'd go
        elif name=="Weapon" or name=="Armor" or name=="Accessory" or name=="ItemSlot1" or name=="ItemSlot2" or name=="ItemSlot3" or name=="ItemSlot4":
          self.createInventory(player,name)
          player.currentMenu=player.currentMenu=self.inventoryMenu
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
            player.nextDungeon()
            player.dgnMap.updateMacro(player)
            player.traversal=True
            player.mainMenu=False
            setImage(player)
            player.battlePlayer=Hero(player)
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
        invImages.append(IMG_PATH+"Blank.gif")
      self.inventoryMenu=Menu(invOptions,player,IMG_PATH+"PauseMenuBackground.gif",invImages,"Inventory")
      self.inventoryMenu.sX=self.optionsImages[self.currentOption].rect.left+50
      self.inventoryMenu.sY=self.optionsImages[self.currentOption].rect.top
      self.inventoryMenu.background.rect.top=10
      self.inventoryMenu.target=name
      self.inventoryMenu.bgSurface=self.bgSurface
      player.currentMenu=self.inventoryMenu

