from AnimatedSprite import Spritesheet, AnimatedSprite
import sys, pygame, time
pygame.init()

print "Full Test - Authors Dave Silverman and Scott Mengel"
print "Set size to 600 x 400 px"
print "Running..."

#--------------------------------------------------------------
#CONSTANTS AND VARIABLES

make=input("How many instances of each animation would you like to load? ")
img={}
ft="" #filetype
r=0 #frame refreshes
i=1 #cycles images
size = width, height = 600,400 #screen sizes
t=0 #trial number

#These are arrays of file types and paths to the corresponding folders so that later I can just iterate through this array and grab 
#the path my images are in and the file type of the images in that folder. We have one array for each type of sprite sheet that we are testing.
AnimPerLineArr=[ ["bmp","AnimationPerLine/bmp16/"] , ["bmp","AnimationPerLine/bmp24/"] , ["gif","AnimationPerLine/gif/"] , ["gif","AnimationPerLine/gift/"] , ["png","AnimationPerLine/png/"] , ["png","AnimationPerLine/pngt/"] ]
OneSheetArr=[ ["bmp","OneSheetPerAnimation/bmp16/"] , ["bmp","OneSheetPerAnimation/bmp24/"] , ["gif","OneSheetPerAnimation/gif/"] , ["gif","OneSheetPerAnimation/gift/"] , ["png","OneSheetPerAnimation/png/"] , ["png","OneSheetPerAnimation/pngt/"] ]
IndivFrameArr=[ ["bmp","IndividualFrames/bmp16/"] , ["bmp","IndividualFrames/bmp24/"] , ["gif","IndividualFrames/gif/"] , ["gif","IndividualFrames/gift/"] , ["png","IndividualFrames/png/"] , ["png","IndividualFrames/pngt/"] ]

screen = pygame.display.set_mode(size) #Screen Set 600x400
backgroundR = 152
backgroundG = 0
backgroundB = 152
screen.fill((backgroundR, backgroundG, backgroundB))#setting the background color to purple.
#-----------------------------------------------------------------
#Reading Individual Frames

def readIndivFrames(fileType, path):
# This definition is used to read in the images that each only have one frame of animation on them and to display their animations

 #This list holds the frames for the first animation
 images1 = [
  [pygame.image.load("%sa1/1.%s"%(path,fileType))],
  [pygame.image.load("%sa1/2.%s"%(path,fileType))],
  [pygame.image.load("%sa1/3.%s"%(path,fileType))],
  [pygame.image.load("%sa1/4.%s"%(path,fileType))],
  [pygame.image.load("%sa1/5.%s"%(path,fileType))],
  [pygame.image.load("%sa1/6.%s"%(path,fileType))],
  [pygame.image.load("%sa1/7.%s"%(path,fileType))],
  [pygame.image.load("%sa1/8.%s"%(path,fileType))],
  [pygame.image.load("%sa1/9.%s"%(path,fileType))]
 ]

 #This list holds the frames for the second animation.
 images2 = [
  [pygame.image.load("%sa2/1.%s"%(path,fileType))],
  [pygame.image.load("%sa2/2.%s"%(path,fileType))],
  [pygame.image.load("%sa2/3.%s"%(path,fileType))],
  [pygame.image.load("%sa2/4.%s"%(path,fileType))],
  [pygame.image.load("%sa2/5.%s"%(path,fileType))],
  [pygame.image.load("%sa2/6.%s"%(path,fileType))],
  [pygame.image.load("%sa2/7.%s"%(path,fileType))],
  [pygame.image.load("%sa2/8.%s"%(path,fileType))],
  [pygame.image.load("%sa2/9.%s"%(path,fileType))]
 ]
 
 #instances is an array of all the instances of each of the two animations.
 instances = []

 #cnt represents how many times both animations need to be made
 cnt = make
 while cnt > 0:
  #animatedSprites is a list that hads two valuse in it. One for the first animation and one for the second animation.
  animatedSprites = []
  #Each position in animatedSprites contains a list that has an actual animatedSprite object, and a list that contains all of that animatedSprite
  #object's position and speed values
  animatedSprites.append([AnimatedSprite(images1,'',10),[(40*cnt),0,2,2]])

  animatedSprites.append([AnimatedSprite(images2,'',10),[(40*cnt),40,2,2]])

  #Adds the animatedSprites list to the instances list.
  instances.append(animatedSprites)

  #Increments the cnt object
  cnt = cnt - 1

 #trials represents the number of trials that is perfor,ed for each test.
 trials = 0
 while trials < 5:

  #This loop is used to go through to the deepest level of this list and modify the positions of each set of animations so that they
  #are not all directly on top of each other.
  groups = len(instances) - 1
  while groups >= 0:
   instances[groups][0][1][0] = 40 * groups
   instances[groups][0][1][1] = 0
   instances[groups][1][1][0] = 40 * groups
   instances[groups][1][1][1] = 40
   groups = groups - 1

  #changes is a variable that is used to track how many frames have rendered.
  changes = 0
  #start represents the time the test starts
  start = time.time()
  #This is the loop that goes through until 500 frames have passed
  while changes < 500:
   #This loop goes through the first level of the instances list so that every group of animations is updated
   groups = len(instances) - 1
   while groups >= 0:
    instances[groups][0][0].nextFrame()
    instances[groups][1][0].nextFrame()

    #These two ifs are used to check if the first animation is off screen and adjust its velocity if it is so that it will come back
    if instances[groups][0][1][0] < 0 or instances[groups][0][1][0] > width - 40:
       instances[groups][0][1][2] = instances[groups][0][1][2] * -1
       
    if instances[groups][0][1][1] < 0 or instances[groups][0][1][1] > height - 40:
       instances[groups][0][1][3] = instances[groups][0][1][3] * -1
       
    #These two ifs are used to check if the second animation is off screen and adjust its velocity if it is so that it will come back
    if instances[groups][1][1][0] < 0 or instances[groups][1][1][0] > width - 40:
       instances[groups][1][1][2] = instances[groups][1][1][2] * -1
       
    if instances[groups][1][1][1] < 0 or instances[groups][1][1][1] > height - 40:
       instances[groups][1][1][3] = instances[groups][1][1][3] * -1
     

    #These two statements update the position of the first animation based on its velocity
    instances[groups][0][1][0] += instances[groups][0][1][2]
    instances[groups][0][1][1] += instances[groups][0][1][3]

    #These two statements update the position of the second animation based on its velocity
    instances[groups][1][1][0] += instances[groups][1][1][2]
    instances[groups][1][1][1] += instances[groups][1][1][3]

    #blits the new position of both animations
    screen.blit(instances[groups][0][0].image[0], (instances[groups][0][0].image[0].get_rect().move(instances[groups][0][1][0], instances[groups][0][1][1])))
    screen.blit(instances[groups][1][0].image[0], (instances[groups][1][0].image[0].get_rect().move(instances[groups][1][1][0], instances[groups][1][1][1])))

    #iterates group object to next one to update
    groups = groups - 1
   #flips the display so that the new frames show up
   pygame.display.flip()
   #fills the screen with the background coor
   screen.fill((backgroundR,backgroundG,backgroundB))
   #iterates the changes object
   changes = changes + 1
  #iterates the trials object
  trials = trials + 1
  #prints what trial we are on and the frame rate.
  print(trials)
  print(1/((time.time() -start)/500))

#-----------------------------------------------------------------

def readPerLine(fileType, path):

 spriteSheet1 = Spritesheet(("%sButtons.%s"%(path,fileType)))

 instances= []

 cnt = make
 while cnt > 0:
  animatedSprites = []
  animatedSprites.append([AnimatedSprite(spriteSheet1.img_extract(9,2,40,40),("%stext.txt"%(path)),10),[(40*cnt),0,2,2]])

  animatedSprites.append([AnimatedSprite(spriteSheet1.img_extract(9,2,40,40),("%stext.txt"%(path)),10),[(40*cnt),40,2,2]])

  instances.append(animatedSprites)

  cnt = cnt - 1

 #trials represents the number of trials that is perfor,ed for each test.
 trials = 0
 while trials < 5:

  #This loop is used to go through to the deepest level of this list and modify the positions of each set of animations so that they
  #are not all directly on top of each other.
  groups = len(instances) - 1
  while groups >= 0:
   instances[groups][0][1][0] = 40 * groups
   instances[groups][0][1][1] = 0
   instances[groups][1][1][0] = 40 * groups
   instances[groups][1][1][1] = 40
   groups = groups - 1

  #changes is a variable that is used to track how many frames have rendered.
  changes = 0
  #start represents the time the test starts
  start = time.time()
  #This is the loop that goes through until 500 frames have passed
  while changes < 500:
   #This loop goes through the first level of the instances list so that every group of animations is updated
   groups = len(instances) - 1
   while groups >= 0:
    instances[groups][0][0].nextFrame()
    instances[groups][1][0].nextFrame()

    #These two ifs are used to check if the first animation is off screen and adjust its velocity if it is so that it will come back
    if instances[groups][0][1][0] < 0 or instances[groups][0][1][0] > width - 40:
       instances[groups][0][1][2] = instances[groups][0][1][2] * -1
       
    if instances[groups][0][1][1] < 0 or instances[groups][0][1][1] > height - 40:
       instances[groups][0][1][3] = instances[groups][0][1][3] * -1
       
    #These two ifs are used to check if the second animation is off screen and adjust its velocity if it is so that it will come back
    if instances[groups][1][1][0] < 0 or instances[groups][1][1][0] > width - 40:
       instances[groups][1][1][2] = instances[groups][1][1][2] * -1
       
    if instances[groups][1][1][1] < 0 or instances[groups][1][1][1] > height - 40:
       instances[groups][1][1][3] = instances[groups][1][1][3] * -1
     

    #These two statements update the position of the first animation based on its velocity
    instances[groups][0][1][0] += instances[groups][0][1][2]
    instances[groups][0][1][1] += instances[groups][0][1][3]

    #These two statements update the position of the second animation based on its velocity
    instances[groups][1][1][0] += instances[groups][1][1][2]
    instances[groups][1][1][1] += instances[groups][1][1][3]

    #blits the new position of both animations
    screen.blit(instances[groups][0][0].image, (instances[groups][0][0].image.get_rect().move(instances[groups][0][1][0], instances[groups][0][1][1])))
    screen.blit(instances[groups][1][0].image, (instances[groups][1][0].image.get_rect().move(instances[groups][1][1][0], instances[groups][1][1][1])))

    #iterates group object to next one to update
    groups = groups - 1
   #flips the display so that the new frames show up
   pygame.display.flip()
   #fills the screen with the background coor
   screen.fill((backgroundR,backgroundG,backgroundB))
   #iterates the changes object
   changes = changes + 1
  #iterates the trials object
  trials = trials + 1
  #prints what trial we are on and the frame rate.
  print(trials)
  print(1/((time.time() -start)/500))

#-----------------------------------------------------------------
def readIndivSheet(fileType, path):

 #creates instances of the spritesheet object witht he given sprite sheet images
 spriteSheet1 = Spritesheet(("%s1.%s"%(path,fileType)))
 spriteSheet2 = Spritesheet(("%s2.%s"%(path,fileType)))
 
 instances= []

 #Increments the cnt object
 cnt = make
 while cnt > 0:
  #animatedSprites is a list that hads two valuse in it. One for the first animation and one for the second animation.
  animatedSprites = []

  animatedSprites.append([AnimatedSprite(spriteSheet1.img_extract(9,1,40,40),("%stext.txt"%(path)),10),[(40*cnt),0,2,2]])
  animatedSprites[0][0].addImages(spriteSheet2.img_extract(9,1,40,40))

  animatedSprites.append([AnimatedSprite(spriteSheet1.img_extract(9,1,40,40),("%stext.txt"%(path)),10),[(40*cnt),40,2,2]])
  animatedSprites[1][0].addImages(spriteSheet2.img_extract(9,1,40,40))

  instances.append(animatedSprites)

  cnt = cnt - 1

 #trials represents the number of trials that is perfor,ed for each test.
 trials = 0
 while trials < 5:

  #This loop is used to go through to the deepest level of this list and modify the positions of each set of animations so that they
  #are not all directly on top of each other.
  groups = len(instances) - 1
  while groups >= 0:
   instances[groups][0][1][0] = 40 * groups
   instances[groups][0][1][1] = 0
   instances[groups][1][1][0] = 40 * groups
   instances[groups][1][1][1] = 40
   groups = groups - 1

  #changes is a variable that is used to track how many frames have rendered.
  changes = 0
  #start represents the time the test starts
  start = time.time()
  #This is the loop that goes through until 500 frames have passed
  while changes < 500:
   #This loop goes through the first level of the instances list so that every group of animations is updated
   groups = len(instances) - 1
   while groups >= 0:
    instances[groups][0][0].nextFrame()
    instances[groups][1][0].nextFrame()

    #These two ifs are used to check if the first animation is off screen and adjust its velocity if it is so that it will come back
    if instances[groups][0][1][0] < 0 or instances[groups][0][1][0] > width - 40:
       instances[groups][0][1][2] = instances[groups][0][1][2] * -1
       
    if instances[groups][0][1][1] < 0 or instances[groups][0][1][1] > height - 40:
       instances[groups][0][1][3] = instances[groups][0][1][3] * -1
       
    #These two ifs are used to check if the second animation is off screen and adjust its velocity if it is so that it will come back
    if instances[groups][1][1][0] < 0 or instances[groups][1][1][0] > width - 40:
       instances[groups][1][1][2] = instances[groups][1][1][2] * -1
       
    if instances[groups][1][1][1] < 0 or instances[groups][1][1][1] > height - 40:
       instances[groups][1][1][3] = instances[groups][1][1][3] * -1
     

    #These two statements update the position of the first animation based on its velocity
    instances[groups][0][1][0] += instances[groups][0][1][2]
    instances[groups][0][1][1] += instances[groups][0][1][3]

    #These two statements update the position of the second animation based on its velocity
    instances[groups][1][1][0] += instances[groups][1][1][2]
    instances[groups][1][1][1] += instances[groups][1][1][3]

    #blits the new position of both animations
    screen.blit(instances[groups][0][0].image, (instances[groups][0][0].image.get_rect().move(instances[groups][0][1][0], instances[groups][0][1][1])))
    screen.blit(instances[groups][1][0].image, (instances[groups][1][0].image.get_rect().move(instances[groups][1][1][0], instances[groups][1][1][1])))

    #iterates group object to next one to update
    groups = groups - 1
   #flips the display so that the new frames show up
   pygame.display.flip()
   #fills the screen with the background coor
   screen.fill((backgroundR,backgroundG,backgroundB))
   #iterates the changes object
   changes = changes + 1
  #iterates the trials object
  trials = trials + 1
  #prints what trial we are on and the frame rate.
  print(trials)
  print(1/((time.time() -start)/500))


#-----------------------------------------------------------------
iterator = 0
print""
print "Testing One Sheet Per Animation"
print "" 
while iterator < len(AnimPerLineArr):

 print""
 print OneSheetArr[iterator][1]
 readIndivSheet(OneSheetArr[iterator][0],OneSheetArr[iterator][1])
 iterator += 1

iterator = 0
print""
print "Testing One Animation Per Line"
print ""
while iterator < len(OneSheetArr):

 print ""
 print AnimPerLineArr[iterator][1]
 readPerLine(AnimPerLineArr[iterator][0],AnimPerLineArr[iterator][1])
 iterator += 1
 
iterator = 0
print ""
print "Testing Individual Frames"
print ""
while iterator < len(IndivFrameArr):

 print ""
 print IndivFrameArr[iterator][1]
 readIndivFrames(IndivFrameArr[iterator][0],IndivFrameArr[iterator][1])
 iterator += 1
