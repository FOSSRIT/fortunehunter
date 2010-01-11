import pippy, pygame, sys, math
from player import Player
from dungeon import Dungeon
from room import Room
from pygame.locals import *
import os.path

IMG_PATH = os.path.dirname(__file__) + "/images/"

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
                elif currentRoom.doorNFlag==LOCKED or currentRoom.doorNFlag==BOTH:
                  for item in player.battlePlayer.inv_Ar:
                    if item.name=="Small Key":
                      return("You use a SMALL KEY, "+enterRoom('north',player,screen))
                  return("This door is locked, you need a SMALL KEY")
                else:
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
                elif currentRoom.doorSFlag==LOCKED or currentRoom.doorSFlag==BOTH:
                  for item in player.battlePlayer.inv_Ar:
                    if item.name=="Small Key":
                      return("You use a SMALL KEY, "+enterRoom('south',player,screen))
                  return("This door is locked, you need a SMALL KEY")
                else:
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
                elif currentRoom.doorEFlag==LOCKED or currentRoom.doorEFlag==BOTH:
                  for item in player.battlePlayer.inv_Ar:
                    if item.name=="Small Key":
                      return("You use a SMALL KEY, "+enterRoom('east',player,screen))
                  return("This door is locked, you need a SMALL KEY")
                else:
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
                elif currentRoom.doorWFlag==LOCKED or currentRoom.doorWFlag==BOTH:
                  for item in player.battlePlayer.inv_Ar:
                    if item.name=="Small Key":
                      return("You use a SMALL KEY, "+enterRoom('west',player,screen))
                  return("This door is locked, you need a SMALL KEY")
                else:
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
        if menu.name=="Stats" or menu.name=="Inventory":
          menu.regress(player)
      elif newKey=='[4]' or newKey=='left':
        if menu.name=="Defeat":
          menu.select("up")
      elif newKey=='[5]':
        print('check')

      elif newKey=='[6]' or newKey=='right':
        if menu.name=="Defeat":
          menu.select("down")

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

      elif newKey=='[2]':
        player.migrateMessages(checkDoor('down',player,screen))

      elif newKey=='[3]' or newKey=='i':
        player.migrateMessages("")

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
  #################
  #check items in room
  #################
  if type(player.currentRoom.it1)==type(Item("","")) and player.currentRoom.it1.hidden==False and player.currentRoom.it1.battle==False:
    player.battlePlayer.inv_Ar.append(player.currentRoom.it1)
    player.migrateMessages(player.currentRoom.it1.name+" added to inventory")
    player.currentRoom.it1=0
  if type(player.currentRoom.it2)==type(Item("","")) and player.currentRoom.it2.hidden==False and player.currentRoom.it2.battle==False:
    player.battlePlayer.inv_Ar.append(player.currentRoom.it2)
    player.migrateMessages(player.currentRoom.it2.name+" added to inventory")
    player.currentRoom.it2=0
  if type(player.currentRoom.it3)==type(Item("","")) and player.currentRoom.it3.hidden==False and player.currentRoom.it3.battle==False:
    player.battlePlayer.inv_Ar.append(player.currentRoom.it3)
    player.migrateMessages(player.currentRoom.it3.name+" added to inventory")
    player.currentRoom.it3=0
  if type(player.currentRoom.it4)==type(Item("","")) and player.currentRoom.it4.hidden==False and player.currentRoom.it4.battle==False:
    player.battlePlayer.inv_Ar.append(player.currentRoom.it4)
    player.migrateMessages(player.currentRoom.it4.name+" added to inventory")
    player.currentRoom.it4=0
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

###Draw methods###
def drawTraversal(player,screen):
  setImage(player)

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

setImage(player)

while pippy.pygame.next_frame():

  for event in pygame.event.get():
    if event.type==USEREVENT+2:
      pygame.time.set_timer(USEREVENT+2,0)
      drawWaiting(player,screen)
      player.waiting=False
      if player.msg5=='Enemies are present, prepare to fight.':
        player.battle=True
      if player.battle==False:
####################################
###TEST FOR IN GAME TUTORIALS
####################################
        if player.currentX==0 and player.currentY==2 and player.battleTutorial==False:
          player.traversal=False
          player.battle=True
          player.curBattle=BattleEngine(player,[Enemy(player,3)])
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
    if player.traversal:
      if player.waiting==True:
        updateWaiting(event,player)
      else:
        #################UPDATE##############################
        updateTraversal(event,player,screen)

    elif player.battle:
      ##battle processes
      updateBattle(event,player)

    elif player.mainMenu:
      ## main menu processes
      updateMenu(event,player)
    elif player.inTutorial:
      updateTutorial(event,player)
    elif player.macroMap:
      updateMacroMap(event,player)

  ###############DRAW#########################
  #draw based on state
  if player.mainMenu==True:
    if player.currentMenu.name=="Inventory":
      player.currentMenu.draw(player,screen,player.currentMenu.sX,player.currentMenu.sY,40)
    elif player.currentMenu.name=="Stats":
      player.currentMenu.draw(player,screen,450,400,50)
      drawTextBox(player,screen)
    elif player.currentMenu.name=="Defeat":
      player.currentMenu.draw(player,screen,450,500,50)
      
    else:
      player.currentMenu.draw(player,screen,450,400,50)
  else:
    drawTextBox(player,screen)
    if player.traversal:
      if player.waiting:
        drawWaiting(player,screen)
      else:
        drawTraversal(player,screen)
    elif player.macroMap:
      player.dgnMap.drawMacro(player,screen)
    elif player.battle:
      player.curBattle.draw(player,screen)
    elif player.inTutorial:
      player.tutorial.draw(player.currentRoomGroup,screen)
  if player.traversal:
    player.currentRoomGroup.draw(screen)
    if player.movTutorial==False:
      player.initMovTutorial(screen)
    pygame.display.flip()
  # update the display


