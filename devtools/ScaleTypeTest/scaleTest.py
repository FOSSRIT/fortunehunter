#! /usr/bin/env python
import pygame, time
pygame.init()

print "Scale Test - Authors Dave Silverman and Scott Mengel"
print "Set size window to 600 x 400 px"
print "Running..."

#--------------------------------------------------------------
#CONSTANTS AND VARIABLES

make=input("How many images would you like to load?\n>")
trial=input("How many runs per trial?\n>")
sizeTo=input("What would you like to resize to? Seperate with a comma, eg: x,y\n>" )

img={}
ft="" #filetype
r=0 #frame refreshes
i=1 #cycles images
size = width, height = 600,400 #screen sizes
t=0 #trial number n
colorkey=(255, 152, 0)

ftArr=[ ["bmp","BMP16100/"] ,
    ["bmp","BMP16173/"] ,
    ["bmp","BMP16200/"] ,
    ["bmp","BMP16400/"] ,
    ["bmp","BMP24100/"] , 
    ["bmp","BMP24173/"] , 
    ["bmp","BMP24200/"] , 
    ["bmp","BMP24400/"] , 
    ["gif","GIF100/"] , 
    ["gif","GIF173/"] ,  
    ["gif","GIF200/"] ,  
    ["gif","GIF400/"] , 
    ["gif","GIFT100/"] , 
    ["gif","GIFT173/"] ,  
    ["gif","GIFT200/"] ,  
    ["gif","GIFT400/"] , 
    ["png","PNG100/"] , 
    ["png","PNG173/"] , 
    ["png","PNG200/"] , 
    ["png","PNG400/"] , 
    ["png","PNGT100/"] , 
    ["png","PNGT173/"] , 
    ["png","PNGT200/"] , 
    ["png","PNGT400/"] ]

screen = pygame.display.set_mode(size) #Screen Set 600x400
background = 152, 251, 152 # pale green

#23456789123456789212345678931234567894123456789512345678961234567897123456789*

# This is the beginning of the actual test loops; this program is a very rough 
# learning exercise which we desire to polish to such a state that it can be 
# used to accurately benchmark the XO laptop's speed capabilities
while 1:
    cnt=make
    ft=ftArr[t]
    print "Testing: "+ft[1]+" extension "+ft[0]
    trialthis=trial
    start=time.time() 
# This timer will reflect the time taken to load and resize images in memory
    switcher = {
# This is also where we need advise regarding implementing convert()
        1: pygame.transform.scale( pygame.image.load("%s2.%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
        2: pygame.transform.scale( pygame.image.load("%s3.%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
        3: pygame.transform.scale( pygame.image.load("%s4.%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
        4: pygame.transform.scale( pygame.image.load("%s5.%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
        5: pygame.transform.scale( pygame.image.load("%s6.%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
        6: pygame.transform.scale( pygame.image.load("%s7.%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
        7: pygame.transform.scale( pygame.image.load("%s8.%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
        8: pygame.transform.scale( pygame.image.load("%s9.%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
        9: pygame.transform.scale( pygame.image.load("%s1.%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] ))
    }
    print "Time taken to load this test at ",
    print sizeTo
    print " pixels was "
    print time.time()-start
# Here ends the loading section, and hereafter we jump into the main loop
    while trialthis>0:
        while cnt>0: 
# establish the initial state for the images of the next trial
            img[cnt,0]= pygame.image.load("%s1.%s"%(ft[1],ft[0]))
            img[cnt,0]= pygame.transform.scale(img[cnt,0],(sizeTo[0], sizeTo[1])) 
            img[cnt,1]=  img[cnt,0].get_rect()
            img[cnt,2]= [2,2] #speed
            m=cnt*40
# Here I move images to avoid indistinguishable stacks of image rectangles
            img[cnt,1]=img[cnt,1].move(m,m) 
            cnt=cnt-1
        r=0
        start=time.time()

        while 1:
# This loop is the 'main event' so to speak, as it is the section that is
# measured in terms of frames per second

            cnt=make # For each 'ball' icon loaded
            while cnt>0: # Cycle and check if the 'ball' should bounce off the wall
                print cnt
                img[cnt,0]=switcher.get(i,None)
                if img[cnt,1].left < 0 or img[cnt,1].right > width:
                    img[cnt,2]=[ -img[cnt,2][0], img[cnt,2][1] ]
                if img[cnt,1].top < 0 or img[cnt,1].bottom > height:
                    img[cnt,2]=[ img[cnt,2][0], -img[cnt,2][1] ]
                img[cnt,1] = img[cnt,1].move(img[cnt,2]) 
# Move the 'ball' image accordingly, plot the change
                screen.blit(img[cnt,0],img[cnt,1])
                cnt=cnt-1 
            pygame.display.flip()
# "Make it so, number two," on those changes above
            i=i+1
            if i>9: i=1
            screen.fill(background)
            r=r+1
            if r>500: break
# After 500 frames, we print the average frame rate to the terminal
        print 1/((time.time()-start)/r)
        trialthis=trialthis-1
    t=t+1
