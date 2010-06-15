#! /usr/bin/env python
import sys, pygame, time
pygame.init()

print "Full Test - Authors Dave Silverman and Scott Mengel"
print "Set size to 600 x 400 px"
print "Running..."

#--------------------------------------------------------------
#CONSTANTS AND VARIABLES

make=input("How many images would you like to load? ")
img={}
ft="" #filetype
r=0 #frame refreshes
i=1 #cycles images
size = width, height = 600,400 #screen sizes
t=0 #trial number n
colorkey=(255, 152, 0)

ftArr=[ ["bmp","BMPs 16-Bits/"] , ["bmp","BMPs 24-Bits/"] , ["bmp","BMPs 32-Bits/"] , ["gif","GIFs/"] , ["gif","GIFs Transparent/"] , ["jpg","JPGs 1Low/"] , ["jpg","JPGs 2Medium/"] , ["jpg","JPGs 3High/"] , ["jpg","JPGs 4Max/"] , ["png","PNGs Indexed/"] , ["png","PNGs Transparent/"] ]

screen = pygame.display.set_mode(size) #Screen Set 600x400
background = 152, 251, 152 # pale green

#The switch function
#-------------------------------------------------------------
def chngImg():
 cnt=make
 while cnt>0:
  switcher = {
   1: pygame.image.load("%s2 Button.%s"%(ft[1],ft[0])),
   2: pygame.image.load("%s3 Button.%s"%(ft[1],ft[0])),
   3: pygame.image.load("%s4 Button.%s"%(ft[1],ft[0])),
   4: pygame.image.load("%s5 Button.%s"%(ft[1],ft[0])),
   5: pygame.image.load("%s6 Button.%s"%(ft[1],ft[0])),
   6: pygame.image.load("%s7 Button.%s"%(ft[1],ft[0])),
   7: pygame.image.load("%s8 Button.%s"%(ft[1],ft[0])),
   8: pygame.image.load("%s9 Button.%s"%(ft[1],ft[0])),
   9: pygame.image.load("%s1 Button.%s"%(ft[1],ft[0]))
  }
  img[cnt,0]=switcher.get(i,pygame.image.load("%s1 Button.%s"%(ft[1],ft[0])))
  #img[cnt,0].set_colorkey(colorkey, pygame.RLEACCEL)
  cnt=cnt-1
#-----------------------------------------------------------------
#Collision detection

def collision():
 cnt=make
 while cnt>0:
  if img[cnt,1].left < 0 or img[cnt,1].right > width:
   img[cnt,2]=[ -img[cnt,2][0], img[cnt,2][1] ]
  if img[cnt,1].top < 0 or img[cnt,1].bottom > height:
   img[cnt,2]=[ img[cnt,2][0], -img[cnt,2][1] ]
  img[cnt,1] = img[cnt,1].move(img[cnt,2])
  screen.blit(img[cnt,0],img[cnt,1])
  cnt=cnt-1
 pygame.display.flip()
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#-----------------------------------------------------------------
while 1:
 cnt=make
 ft=ftArr[t]
 print "Testing "+ft[1]+"N Button."+ft[0]
 trial=5
 while trial>0:
  while cnt>0:
   img[cnt,0]= pygame.image.load("%s1 Button.%s"%(ft[1],ft[0])) #image.load
   img[cnt,1]=  img[cnt,0].get_rect()
   img[cnt,2]= [2,2] #speed
   m=cnt*40 # named m cause i wanted some m&ms
   img[cnt,1]=img[cnt,1].move(m,m) #see? it wasn't as tastey though
   cnt=cnt-1
  r=0
  start=time.time()
# ----------------------------------------------------------------- 
  while 1:
   chngImg()
   i=i+1
   if i>9: i=1
   
   for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
   
#   speed1=collision(ballrect1,speed1)
#   ballrect1 = ballrect1.move(speed1)
   
   collision()
   screen.fill(background)
   
#   cnt=make
#   while cnt>0:
#   screen.blit(ball1, ballrect1)
#    screen.blit(img[cnt,0],img[cnt,1])
#    cnt=cnt-1
#   
#   pygame.display.flip()
   
   r=r+1
   if r>500: break
   
# -----------------------------------------------------------------
# -----------------------------------------------------------------
  
  print 1/((time.time()-start)/r)
  trial=trial-1
 t=t+1
