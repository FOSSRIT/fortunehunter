import sys, pygame, time
pygame.init()

size = width, height = 600,400
print "\n\n ---- ---- ---- ---- ---- ---- \nFiltype test - Authors Dave Silverman and Scott Mengel"
print "Set size to 1200 x 900 px"
speed = [2, 2]
black = 255, 255, 255

screen = pygame.display.set_mode(size)

ball = pygame.image.load("1 Button.png")
ballrect = ball.get_rect()
i=1
print "Ball Loaded, collision detection ready, Initiating Loop:"

# R is the Renewed time
# init is the time started
# tt is the test time, gathered by adding the previous test time with
#the new elapsed time which is test.time()'s difference from init

r=0

start = time.time()

while 1:
 # Homemade switcher for the purpose of selecting which img to load
 switcher = {
  1: pygame.image.load("2 Button.png"),
  2: pygame.image.load("3 Button.png"),
  3: pygame.image.load("4 Button.png"),
  4: pygame.image.load("5 Button.png"),
  5: pygame.image.load("6 Button.png"),
  6: pygame.image.load("7 Button.png"),
  7: pygame.image.load("8 Button.png"),
  8: pygame.image.load("9 Button.png"),
  9: pygame.image.load("1 Button.png")
 }
 ball = switcher.get(i,pygame.image.load("1 Button.png"))
 
 i=i+1
 
 if i>9: i=1
 
 for event in pygame.event.get():
  if event.type == pygame.QUIT: sys.exit()
 
 ballrect = ballrect.move(speed)
 
 if ballrect.left < 0 or ballrect.right > width:
  speed[0] = -speed[0]
 if ballrect.top < 0 or ballrect.bottom > height:
  speed[1] = -speed[1]
 
 screen.fill(black)
 screen.blit(ball, ballrect)
 pygame.display.flip()
 
 r=r+1

 val=1/((time.time()-start)/r)
 print val
 print r
 if r > 500:
  sys.exit(0)
