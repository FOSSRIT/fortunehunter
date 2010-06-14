import sys, pygame, time
pygame.init()

ft="bmp"
r=0
i=1
size = width, height = 600,400

print "Nightmare test - Authors Dave Silverman and Scott Mengel"
print "Set size to 600 x 400 px"
print "Running..."
speed1=speed2=speed3=speed4=[2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball1=ball2=ball3=ball4=pygame.image.load("1 Button.%s"%ft)

ballrect1 = ball1.get_rect()
ballrect1 = ballrect1.move( 200, 0)

ballrect2 = ball2.get_rect()
ballrect2 = ballrect2.move( 0, 200)

ballrect3 = ball3.get_rect()
ballrect3 = ballrect3.move( 200, 200)

ballrect4 = ball4.get_rect()
ballrect4 = ballrect4.move( 0, 0)

# ballrect = ballrect.move( 0, 0)

print "Ball Loaded, collision detection ready, Initiating Loop:"

start=time.time()

#-----------------------------------------------------------------

def chngImg(thisBall):
 switcher = {
  1: pygame.image.load("2 Button.%s"%ft),
  2: pygame.image.load("3 Button.%s"%ft),
  3: pygame.image.load("4 Button.%s"%ft),
  4: pygame.image.load("5 Button.%s"%ft),
  3: pygame.image.load("4 Button.%s"%ft),
  3: pygame.image.load("4 Button.%s"%ft),
  5: pygame.image.load("6 Button.%s"%ft),
  6: pygame.image.load("7 Button.%s"%ft),
  7: pygame.image.load("8 Button.%s"%ft),
  8: pygame.image.load("9 Button.%s"%ft),
  9: pygame.image.load("1 Button.%s"%ft)
 }
 return switcher.get(i,pygame.image.load("1 Button.%s"%ft))

#-----------------------------------------------------------------

def collision(thisBallRect,thisSpeed):
 if thisBallRect.left < 0 or thisBallRect.right > width:
  return -thisSpeed[0],thisSpeed[1]
 if thisBallRect.top < 0 or thisBallRect.bottom > height:
  return thisSpeed[0],-thisSpeed[1]
 else: return thisSpeed
#-----------------------------------------------------------------

while 1:
 ball1 = chngImg(ball1)
 ball2 = chngImg(ball2)
 ball3 = chngImg(ball3)
 ball4 = chngImg(ball4)

 i=i+1 
 if i>9: i=1

 for event in pygame.event.get():
  if event.type == pygame.QUIT: sys.exit()
 
 speed1=collision(ballrect1,speed1)
 ballrect1 = ballrect1.move(speed1)
 
 speed2=collision(ballrect2,speed2)
 ballrect2 = ballrect2.move(speed2)
 
 speed3=collision(ballrect3,speed3)
 ballrect3 = ballrect3.move(speed3)
 
 speed4=collision(ballrect4,speed4)
 ballrect4 = ballrect4.move(speed4)
 
 screen.fill(black)
 screen.blit(ball1, ballrect1)
 screen.blit(ball2, ballrect2)
 screen.blit(ball3, ballrect3)
 screen.blit(ball4, ballrect4)

 pygame.display.flip()
 
 r=r+1
 
 if r>500: break

#-----------------------------------------------------------------

print 1/((time.time()-start)/r)
