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

ftArr=[ ["bmp","BMP16100/"] , ["bmp","BMP16173/"] , ["bmp","BMP16200/"] , ["bmp","BMP16400/"] ,["bmp","BMP24100/"] , ["bmp","BMP24173/"] , ["bmp","BMP24200/"] , ["bmp","BMP24400/"] , ["gif","GIF100/"] , ["gif","GIF173/"] ,  ["gif","GIF200/"] ,  ["gif","GIF400/"] , ["gif","GIFT100/"] , ["gif","GIFT173/"] ,  ["gif","GIFT200/"] ,  ["gif","GIFT400/"] , ["png","PNG100/"] , ["png","PNG173/"] , ["png","PNG200/"] , ["png","PNG400/"] , ["png","PNGT100/"] , ["png","PNGT173/"] , ["png","PNGT200/"] , ["png","PNGT400/"] ]

screen = pygame.display.set_mode(size) #Screen Set 600x400
background = 152, 251, 152 # pale green


#-------------------------------------------------------------
#The switch function

def chngImg():
    cnt=make
    while cnt>0:
        """switcher = {
            1: pygame.transform.scale( pygame.image.load( "%s2.%s"%( ft[1],ft[0] ) ) ,(sizeTo[0],sizeTo[1] ),
            2: pygame.transform.scale( pygame.image.load("%s3.%s"%(ft[1],ft[0])),(sizeTo[0],sizeTo[1] ),
            3: pygame.transform.scale( pygame.image.load("%s4.%s"%(ft[1],ft[0])),(sizeTo[0],sizeTo[1] ),
            4: pygame.transform.scale( pygame.image.load("%s5.%s"%(ft[1],ft[0])),(sizeTo[0],sizeTo[1] ),
            5: pygame.transform.scale( pygame.image.load("%s6.%s"%(ft[1],ft[0])),(sizeTo[0],sizeTo[1] ),
            6: pygame.transform.scale( pygame.image.load("%s7.%s"%(ft[1],ft[0])),(sizeTo[0],sizeTo[1] ),
            7: pygame.transform.scale( pygame.image.load("%s8.%s"%(ft[1],ft[0])),(sizeTo[0],sizeTo[1] ),
            8: pygame.transform.scale( pygame.image.load("%s9.%s"%(ft[1],ft[0])),(sizeTo[0],sizeTo[1] ),
            9: pygame.transform.scale( pygame.image.load("%s1.%s"%(ft[1],ft[0])),(sizeTo[0],sizeTo[1] )
        }
        """
        img[cnt,0]=switcher.get(i,pygame.image.load("%s1.%s"%(ft[1],ft[0])))
#        img[cnt,0] = pygame.transform.scale(img[cnt,0],(sizeTo[0], sizeTo[1]))
        cnt=cnt-1

#-----------------------------------------------------------------
#- Collision detection -------------------------------------------

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
#- Number of dashed lined relates to loops -----------------------

while 1:
    cnt=make
    ft=ftArr[t]
    print "Testing: "+ft[1]+" extension "+ft[0]
    trialthis=trial
    start=time.time()
    switcher = {
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
    
#-----------------------------------------------------------------
    while trialthis>0:

    #-------------------------------------------------------------
        while cnt>0:
            img[cnt,0]= pygame.image.load("%s1.%s"%(ft[1],ft[0])) #image.load
            img[cnt,0]= pygame.transform.scale(img[cnt,0],(sizeTo[0], sizeTo[1])) 
            img[cnt,1]=  img[cnt,0].get_rect()
            img[cnt,2]= [2,2] #speed
            m=cnt*40 # named m cause i wanted some m&ms
            img[cnt,1]=img[cnt,1].move(m,m) #see? it wasn't as tastey though
            cnt=cnt-1

    #-------------------------------------------------------------
        r=0
        start=time.time()

    #-------------------------------------------------------------
        while 1:
            chngImg()
            i=i+1
            if i>9: i=1
            
            collision()
            screen.fill(background)
            
            r=r+1
            if r>500: break
         
    #-------------------------------------------------------------
        print 1/((time.time()-start)/r)
        trialthis=trialthis-1

#-----------------------------------------------------------------
    t=t+1
    print ""

#-----------------------------------------------------------------
#-----------------------------------------------------------------
