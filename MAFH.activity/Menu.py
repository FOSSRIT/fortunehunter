import pygame, sys
from constants import FMC_PATH, MENU_PATH, TOUR_PATH, ENV_PATH, PUZZLE_PATH
import os.path
from random import *
from sugar.activity import activity
import simplejson
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
       # if name=="Pause Menu" or name=="Stats" or name=="Math Stats" or name=="Inventory":
        self.LArrow=pygame.image.load(MENU_PATH+"LArrow.gif")
        self.XButton=pygame.image.load(TOUR_PATH+"button/buttonX.gif")
        self.RArrow=pygame.image.load(MENU_PATH+"RArrow.gif")
        self.LButton=pygame.image.load(TOUR_PATH+"button/buttonL.gif")

    def draw(self,player,screen,xStart,yStart,height):
        menuGroup=pygame.sprite.Group()
        if self.name=="Inventory":
          self.background.rect=(0,self.sY,1200,900)
	bgGroup=pygame.sprite.Group(self.background)
        self.startX=xStart
        self.startY=yStart
        self.height=height
        if not self.name=="Defeat":
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

          weapon=font.render(wp,True,(0,0,0))
          self.bgSurface.blit(weapon,weaponRect)
          armor=font.render(arm,True,(0,0,0))
          self.bgSurface.blit(armor,armorRect)
          accessory=font.render(acc,True,(0,0,0))
          self.bgSurface.blit(accessory,accessoryRect)
          self.bgSurface.fill((255,150,150),(502,417,123,98))
          self.bgSurface.fill((150,255,150),(502,511,123,99))
          self.bgSurface.blit(self.LArrow,(504,450,20,20))
          self.bgSurface.blit(pygame.transform.scale(self.XButton,(50,50)),(550,450,20,20))
          self.bgSurface.blit(self.RArrow,(575,550,20,20)) 
          self.bgSurface.blit(pygame.transform.scale(self.LButton,(50,50)),(520,540,20,20))
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
            y=140
            sel=0
            self.bgSurface=pygame.Surface((1200,700))
            player.currentRoomGroup.draw(self.bgSurface)
            bgGroup.draw(self.bgSurface)
            screen.blit(self.bgSurface,(0,0,1200,900))
            screen.blit(font.render("Inventory:",True,(0,0,0)),(self.sX+80,self.sY+100,200,40))
            for item in player.battlePlayer.inv_Ar:
              if sel==self.currentOption:
                screen.fill((50,50,250),pygame.Rect(self.sX+40,self.sY+y,200,40))
              screen.blit(font.render(item.name,True,(0,0,0)),pygame.Rect(self.sX+40,self.sY+y,200,40))
              y+=40
              sel+=1
              if y==400:
                y=0
                x+=200
            screen.fill((255,150,150),(500,555,125,50))
            screen.fill((150,255,150),(625,555,127,50))
            screen.blit(self.LArrow,(504,560,20,20))
            screen.blit(pygame.transform.scale(self.XButton,(40,40)),(550,560,20,20))
            screen.blit(self.RArrow,(710,560,20,20))
            screen.blit(pygame.transform.scale(self.LButton,(40,40)),(675,560,20,20))

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
          self.bgSurface=pygame.Surface((1200,700))
          player.currentRoomGroup.draw(self.bgSurface)
          bgGroup.draw(self.bgSurface)

          menuGroup.draw(screen)
          font=pygame.font.SysFont("cmr10",40,False,False)
          screen.blit(font.render("Options",True,(0,0,0)),(525,200,0,0))
          font=pygame.font.SysFont("cmr10",24,False,False)
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
          screen.blit(font.render("Save Game",True,(20,20,100)),(550+x1,250,0,0))
          screen.blit(font.render("Exit Game",True,(20,20,100)),(550+x2,300,0,0))
          screen.blit(font.render("Main Menu",True,(20,20,100)),(550+x3,350,0,0))
          screen.blit(font.render("Return to Game",True,(20,20,100)),(550+x4,400,0,0))
          screen.fill((255,150,150),(500,555,125,50))
          screen.fill((150,255,150),(625,555,127,50))
          screen.blit(self.LArrow,(504,560,20,20))
          screen.blit(pygame.transform.scale(self.XButton,(40,40)),(550,560,20,20))
          screen.blit(self.RArrow,(710,560,20,20))
          screen.blit(pygame.transform.scale(self.LButton,(40,40)),(675,560,20,20))

        elif self.name=="Math Stats":
          font=pygame.font.SysFont("cmr10",40,False,False)
          screen.blit(font.render("Math Stats",True,(0,0,0)),(525,120,0,0))
          font=pygame.font.SysFont("cmr10",24,False,False)
          screen.blit(font.render("Multiplication problems:",True,(0,0,50)),(510,160,0,0))
          screen.blit(font.render("Easy: "+repr(player.multiplicationStats[0][0])+"/"+repr(player.multiplicationStats[0][1]),True,(0,50,0)),(550,200,0,0))
          screen.blit(font.render("Medium: "+repr(player.multiplicationStats[1][0])+"/"+repr(player.multiplicationStats[1][1]),True,(0,50,0)),(550,225,0,0))
          screen.blit(font.render("Hard: "+repr(player.multiplicationStats[2][0])+"/"+repr(player.multiplicationStats[2][1]),True,(0,50,0)),(550,250,0,0))
          screen.blit(font.render("Fraction problems:",True,(0,0,50)),(510,300,0,0))
          screen.blit(font.render("Easy: "+repr(player.divisionStats[0][0])+"/"+repr(player.divisionStats[0][1]),True,(0,50,0)),(550,340,0,0))
          screen.blit(font.render("Medium: "+repr(player.divisionStats[1][0])+"/"+repr(player.divisionStats[1][1]),True,(0,50,0)),(550,365,0,0))
          screen.blit(font.render("Hard: "+repr(player.divisionStats[2][0])+"/"+repr(player.divisionStats[2][1]),True,(0,50,0)),(550,390,0,0))
          screen.blit(font.render("Geometry problems:",True,(0,0,50)),(510,420,0,0))
          screen.blit(font.render("Easy: "+repr(player.geometryStats[0][0])+"/"+repr(player.geometryStats[0][1]),True,(0,50,0)),(550,455,0,0))
          screen.blit(font.render("Medium: "+repr(player.geometryStats[1][0])+"/"+repr(player.geometryStats[1][1]),True,(0,50,0)),(550,480,0,0))
          screen.blit(font.render("Hard: "+repr(player.geometryStats[2][0])+"/"+repr(player.geometryStats[2][1]),True,(0,50,0)),(550,505,0,0))
          screen.blit(font.render("Puzzles solved:",True,(0,0,50)),(510,535,0,0))
          screen.blit(font.render(repr(player.puzzlesSolved),True,(0,50,0)),(670,535,0,0))
          screen.fill((255,150,150),(500,555,125,50))
          screen.fill((150,255,150),(625,555,127,50))
          screen.blit(self.LArrow,(504,560,20,20))
          screen.blit(pygame.transform.scale(self.XButton,(40,40)),(550,560,20,20))
          screen.blit(self.RArrow,(710,560,20,20))
          screen.blit(pygame.transform.scale(self.LButton,(40,40)),(675,560,20,20))

        elif self.name=="Adventure Play":
          screen.blit(font.render("Continue",True,(150,0,0)),(450+40,400+3,0,0))
          screen.blit(font.render("Load Game",True,(150,0,0)),(450+40,400+53,0,0))
          screen.blit(font.render("New Game",True,(150,0,0)),(450+40,400+103,0,0))
		  
        elif self.name=="Creative Play":
          screen.blit(font.render("Play Custom Map",True,(150,0,0)),(450+40,400+3,0,0))
          screen.blit(font.render("New Custom Map",True,(150,0,0)),(450+40,400+53,0,0))
          screen.blit(font.render("Share Maps",True,(150,0,0)),(450+40,400+103,0,0))
		  
        elif self.name=="Network Play":
          screen.blit(font.render("Local Cooperative Play",True,(150,0,0)),(450+40,400+3,0,0))
          screen.blit(font.render("Local Treasure Trekkers Play",True,(150,0,0)),(450+40,400+53,0,0))
          screen.blit(font.render("View Scoreboards",True,(150,0,0)),(450+40,400+103,0,0))
		  
        elif self.name=="Extras":
          screen.blit(font.render("View Awards",True,(150,0,0)),(450+40,400+3,0,0))
          screen.blit(font.render("View Statistics",True,(150,0,0)),(450+40,400+53,0,0))
		  
        elif self.name=="Difficulty Menu":
          menuGroup.add(player.previousMenu.optionsImages)
          menuGroup.draw(screen)
          screen.blit(font.render("Critical Attack",True,(150,0,0)),(450+40,400+3,0,0))
          screen.blit(font.render("Special Attack",True,(150,0,0)),(450+40,400+53,0,0))
          screen.blit(font.render("Magic Attack",True,(150,0,0)),(450+40,400+103,0,0))
          screen.blit(font.render("Shop",True,(150,0,0)),(450+40,400+153,0,0))
          screen.blit(font.render("Back",True,(150,0,0)),(450+40,400+203,0,0))
		  
          screen.blit(font.render("ON",True,(150,0,0)),(player.currentMenu.sX+40,player.currentMenu.sY+3,0,0))
          screen.blit(font.render("OFF",True,(150,0,0)),(player.currentMenu.sX+40,player.currentMenu.sY+43,0,0))	
		  
        elif self.name=="Options Menu":
          menuGroup.draw(screen)
          screen.blit(font.render("Critical Attack",True,(150,0,0)),(450+40,400+3,0,0))
          screen.blit(font.render("Special Attack",True,(150,0,0)),(450+40,400+53,0,0))
          screen.blit(font.render("Magic Attack",True,(150,0,0)),(450+40,400+103,0,0))
          screen.blit(font.render("Shop",True,(150,0,0)),(450+40,400+153,0,0))
          screen.blit(font.render("Back",True,(150,0,0)),(450+40,400+203,0,0))
        
      
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

        elif name=="Exit Game":
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
		  
        elif name=="Controls":
            player.inTutorial=True
            player.inComic=True
            player.mainMenu=False
            player.startComic(TOUR_PATH+"setup/",None)
			
        elif name=="OFF":  #was disable
          if player.previousMenu.currentOption==0:
            player.critDifficulty=0
          elif player.previousMenu.currentOption==1:
            player.divDifficulty=0
          elif player.previousMenu.currentOption==2:
            player.geomDifficulty=0
          elif player.previousMenu.currentOption==3:
            player.shopDifficulty=1
          player.currentMenu=player.previousMenu
        elif name=="ON":   #was easy
          if player.previousMenu.currentOption==0:
            player.critDifficulty=1
          elif player.previousMenu.currentOption==1:
            player.divDifficulty=1
          elif player.previousMenu.currentOption==2:
            player.geomDifficulty=1
          elif player.previousMenu.currentOption==3:
            player.shopDifficulty=1
          player.currentMenu=player.previousMenu
#remove following code til the next #------------------------
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
#-------------------------------------------------------------------------------

#Load game - we want to load the profile, but not start a level. Continue will actually start the level
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
        elif name=="Weapon" or name=="Armor" or name=="Accessory":
          self.createInventory(player)
  
        elif name[0:9]=="Equipment":
          player.battlePlayer.equip(player.battlePlayer.inv_Ar[int(name[9:len(name)])])
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

    def createInventory(self,player):
      invOptions=[]
      invImages=[]
      ##Create a 10X2 menu of all items in player's inventory
      ##TODO: make scrollable
      x=0
      y=0
      i=0
      for item in player.battlePlayer.inv_Ar:
        invOptions.append("Equipment"+repr(i))
        i+=1
        invImages.append(MENU_PATH+"Blank.gif")
      player.inventoryMenu=Menu(invOptions,player,MENU_PATH+"VictoryScreen.gif",invImages,"Inventory")
     
      player.inventoryMenu.sX=485
      player.inventoryMenu.sY=11
     # self.inventoryMenu.bgSurface=self.bgSurface
      player.currentMenu=player.inventoryMenu

