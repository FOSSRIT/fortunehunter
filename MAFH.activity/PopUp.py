import pygame

class PopUp:
  def __init__(self,x,y,messages):
    self.x=x
    self.y=y
    self.messages=messages

    #Make a black background with yellow border
    self.background=pygame.Surface((510,(len(messages)*25)+10))
    self.background.fill((200,200,50),(0,0,510,(len(messages)*25)+10))
    self.background.fill((0,0,0),(5,5,500,len(messages)*25))
     
    #Draw messages on that background
    font=pygame.font.SysFont("cmr10",30,False,False)
    y=0
    for line in messages:
      self.background.blit(font.render(line,True,(255,255,255)),(x+5,y+5,0,0))
      y+=25
  def draw(self,screen):
    screen.blit(self.background,(self.x,self.y,500,200))
