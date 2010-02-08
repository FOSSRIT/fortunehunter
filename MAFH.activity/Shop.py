from Items import get_item
import pygame
from constants import MENU_PATH, CHAR_PATH

############################################################################
#Shop class
############################################################################
class Shop:
  def __init__(self,player):
    self.player=player
    self.itemList=[get_item('l'),get_item('m')]
    self.selItem=0
    self.numItem=[0,0]
    self.totalPrice=0
    self.selDigit=3
    self.enteredDigits=[0,0,0,0]
    self.buyScreen=False
    self.buyMode=True
    self.sellMode=False
    self.yes=True
    self.shopKeeperVariable=0
    self.message=[]
    if self.player.shopTutorial==False:
      self.message.append("Welcome.  You can view my")
      self.message.append("wares by using the arrow keys")
      self.message.append("If you want to switch between")
      self.message.append("buying and selling, just press")
      self.message.append("   (B) or    (S)")
    else:
      self.message.append("Got some rare things")
      self.message.append("on sale stranger")
  def finish(self):
    if self.buyMode:
      enteredNumber=1000*self.enteredDigits[0]+100*self.enteredDigits[1]+10*self.enteredDigits[2]+self.enteredDigits[3]
      if enteredNumber>=self.totalPrice and self.player.battlePlayer.akhal>=enteredNumber:
        self.player.buySell.play()
        if self.player.shopDifficulty==1:
          self.player.battlePlayer.akhal-=self.totalPrice
        else:
          self.player.battlePlayer.akhal-=enteredNumber
        if enteredNumber>self.totalPrice:
          if self.player.shopDifficulty==1:
            self.message=[]
            self.message.append("Here you are,")
            self.message.append("and your change")
          else:
            self.message=[]
            self.message.append("Hehe, with that generosity")
            self.message.append("you can come back")
            self.message.append("ANY time sir")
        else:
          self.message=[]
          self.message.append("Here you are")
        i=0

        for item in self.itemList:
          for k in range(self.numItem[i]):
            self.player.battlePlayer.inv_Ar.append(self.itemList[i])
          i+=1
      else:
        self.message=[]
        self.message.append("Not enough cash")
    elif self.sellMode:
      self.player.buySell.play()
      self.player.battlePlayer.akhal+=self.player.battlePlayer.inv_Ar[self.selItem].sellVal
      self.player.battlePlayer.inv_Ar.remove(self.player.battlePlayer.inv_Ar[self.selItem])
      self.selItem=0
      self.message=[]
    self.buyScreen=False
  def update(self,event,player):
    if event.type == QUIT:
      sys.exit()

    #handle key input
    elif event.type == KEYDOWN:
      newKey=pygame.key.name(event.key)
      if player.shopTutorial==False:
        self.message=[]
        self.message.append("If you want to leave")
        self.message.append("press    or backspace")
      if newKey=='escape':
        sys.exit()
      elif newKey=='[6]' or newKey=='right':
        #Right
        #increment numItems/selectedDigit
        if self.buyScreen:
          if self.sellMode:
            self.yes=False
          if self.selDigit<3:
            self.selDigit+=1
          else:
            self.selDigit=0
        else:
          if self.numItem[self.selItem]<9:
            self.numItem[self.selItem]+=1
          else:
            self.numItem[self.selItem]=0
      elif newKey=='[2]' or newKey=='down':
        #Down
        #decrement selected item/enteredDigits[selItem]
        if self.sellMode:
          if not self.buyScreen:
            if self.selItem<len(self.player.battlePlayer.inv_Ar)-1:
              self.selItem+=1
            else:
              self.selItem=0
        else:
          if self.buyScreen:
            if self.enteredDigits[self.selDigit]>0:
              self.enteredDigits[self.selDigit]-=1
            else:
              self.enteredDigits[self.selDigit]=9
          else:

            if self.selItem<len(self.itemList)-1:
              self.selItem+=1
            else:
              self.selItem=0
      elif newKey=='[4]' or newKey=='left':
        #Left
        #decrement numItems/selectedDigit
        if self.buyScreen:
          if self.sellMode:
            self.yes=True
          elif self.selDigit>0:
            self.selDigit-=1
          else:
            self.selDigit=3
        else:
          if self.numItem[self.selItem]>0:
            self.numItem[self.selItem]-=1
          else:
            self.numItem[self.selItem]=9
      elif newKey=='[8]' or newKey=='up':
        #Up
        #increment selected item/enteredDigits[selItem]
        if self.sellMode:
          if not self.buyScreen:
            if self.selItem>0:
              self.selItem-=1
            else:
              self.selItem=len(self.player.battlePlayer.inv_Ar)-1
        else:
          if self.buyScreen:
            if self.enteredDigits[self.selDigit]<9:
              self.enteredDigits[self.selDigit]+=1
            else:
              self.enteredDigits[self.selDigit]=0
          else:

            if self.selItem>0:
              self.selItem-=1
            else:
              self.selItem=len(self.itemList)-1
      elif newKey=='[1]' or newKey=='return':
        #Check
        #buy/finish
        if self.sellMode:
          if self.buyScreen:
            if self.yes:
              self.finish()
            else:
              self.buyScreen=False
          else:
            itName=self.player.battlePlayer.inv_Ar[self.selItem].name
            self.yes=False
            if itName=="Small Key" or itName=="Big Key" or itName=="Calculator" or itName=="Ancient Amulet":
              #have shop merchant say
              self.message=[]
              self.message.append("That looks important,")
              self.message.append("I wouldn't sell that if I were you")
            else:
              self.buyScreen=True
              if self.player.shopDifficulty==1:
                self.shopKeeperVariable=self.player.battlePlayer.inv_Ar[self.selItem].sellVal
              else:
                seed()
                self.shopKeeperVariable=randint(1,self.player.battlePlayer.inv_Ar[self.selItem].sellVal*2)

        elif self.buyMode:
          if self.buyScreen:
            self.finish()
          else:
            self.buyScreen=True
            i=0
            for item in self.itemList:
              self.totalPrice+=self.numItem[i]*self.itemList[i].buyVal
              i=i+1
      elif newKey=='[3]' or newKey=='backspace':
        if self.buyScreen:
          self.buyScreen=False
        else:
          self.player.shop=False
          self.player.traversal=True
          self.player.shopTutorial=True
      elif newKey=='[7]' or newKey=='s':
        #circle, switch to sell mode
        if self.buyScreen==False:
          self.buyMode=False
          self.sellMode=True
          self.selItem=0
          self.numItem=[0,0]
          #self.player.sellin.play()

      elif newKey=='[9]' or newKey=='b':
        #square, switch to buy mode
        if self.buyScreen==False:
          self.sellMode=False
          self.buyMode=True
          self.selItem=0
          self.numItem=[0,0]
          #self.player.buyin.play()

  def draw(self,screen,player):
    player.currentRoomGroup.draw(screen)
    font = pygame.font.Font(None, 36)
    merchantSprite=pygame.sprite.Sprite()
    bgSprite=pygame.sprite.Sprite()
    bgSprite.image=pygame.image.load(MENU_PATH+"ShopBG.gif")
    bgSprite.rect=(0,0,600,900)
    merchantSprite.image=pygame.transform.scale(pygame.image.load(CHAR_PATH+"Merchant.gif"),(550,550))
    merchantSprite.rect=pygame.Rect(640,160,200,200)
    merchantGroup=pygame.sprite.Group(merchantSprite)
    bgGroup=pygame.sprite.Group(bgSprite)
    bgGroup.draw(screen)
    screen.blit(font.render("Buy              Sell",True,(0,0,0)),(190,30,50,50))
    merchantGroup.draw(screen)
    screen.blit(pygame.image.load(MENU_PATH+"Speech.gif"),(550,0,400,400))
    if self.buyMode:

      i=0
      y=80
      for item in self.itemList:
        #from left to right: arrow, box w/#, arrow, item name

        if i==self.selItem:
          screen.fill((200,200,150),(150,y,400,40))
        screen.blit(pygame.image.load(MENU_PATH+"LArrow.gif"),(150,y,40,40))
        screen.fill((150,150,10),(190,y,40,40))
        screen.blit(font.render(repr(self.numItem[i]),True,(255,255,255)),(190,y,50,40))
        screen.blit(pygame.image.load(MENU_PATH+"RArrow.gif"),(230,y,40,40))
        screen.blit(font.render(item.name,True,(255,255,255)),(270,y,500,40))
        y+=40
        i+=1

      if self.buyScreen:
        i=0
        y=7
        for item in self.itemList:
          if not self.numItem[i] == 0:
            screen.blit(font.render(repr(self.numItem[i])+" "+self.itemList[i].name+" at "+repr(self.itemList[i].buyVal),True,(0,0,0)),(650,y,500,40))
            y+=40
          i+=1
        x=650
        i=0
        for digit in self.enteredDigits:
          if i==self.selDigit:
            screen.fill((150,150,200),(x,125,40,130))
          screen.blit(pygame.transform.rotate(pygame.image.load(MENU_PATH+"LArrow.gif"),-90),(x,125,40,40))
          screen.fill((50,100,100),(x,175,50,40))
          screen.blit(font.render(repr(digit),True,(255,255,255)),(x,175,40,40))
          screen.blit(pygame.transform.rotate(pygame.image.load(MENU_PATH+"RArrow.gif"),-90),(x,215,40,40))
          x+=50
          i+=1
      else:
        y=60
        for line in self.message:
          screen.blit(font.render(line,True,(0,0,0)),(575,y,500,40))
          y+=40
    elif self.sellMode:
      i=0
      y=80
      for item in self.player.battlePlayer.inv_Ar:
          font = pygame.font.Font(None, 36)
          if i==self.selItem:
            screen.fill((150,150,200),(150,y,375,40))
          screen.blit(font.render(item.name,True,(255,255,255)),(200,y,500,40))
          y+=40
          i+=1

      if self.buyScreen:
        screen.blit(font.render("For a "+self.player.battlePlayer.inv_Ar[self.selItem].name,True,(0,0,0)),(575,60,500,40))
        screen.blit(font.render(" I will give you "+repr(self.shopKeeperVariable),True,(0,0,0)),(575,100,500,40))
        screen.blit(font.render("OK?",True,(0,0,0)),(600,140,500,40))
        if self.yes:
          screen.fill((150,150,250),(660,180,60,40))
        else:
          screen.fill((150,150,250),(760,180,60,40))
        screen.blit(font.render("Yes",True,(0,0,0)),(660,180,100,40))
        screen.blit(font.render("No",True,(0,0,0)),(760,180,100,40))
      else:
        y=60
        for line in self.message:
          screen.blit(font.render(line,True,(0,0,0)),(575,y,500,40))
          y+=40
    pygame.display.flip()
