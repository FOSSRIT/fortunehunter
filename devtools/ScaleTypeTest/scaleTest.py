#! /usr/bin/env python
import pygame, time
pygame.init()

print "Scale Test - Authors Dave Silverman and Scott Mengel"
print "Set size to 600 x 400 px"
print "Running..."



#--------------------------------------------------------------
#CONSTANTS AND VARIABLES

make=input("How many images would you like to load? ")
trial=input("How many runs per trial? ")
img={}
ft="" #filetype
r=0 #frame refreshes
i=1 #cycles images
size = width, height = 600,400 #screen sizes
t=0 #trial number n
colorkey=(255, 152, 0)

ftArr=[ ["bmp","BMP16100/","100%"] , ["bmp","BMP16173/","57.8%"] , ["bmp","BMP16200/","50%"] , ["bmp","BMP16400/","25%"] ,["bmp","BMP24100/","100%"] , ["bmp","BMP24173/","57.8%"] , ["bmp","BMP24200/","50%"] , ["bmp","BMP24400/","25%"] , ["gif","GIF100/","100%"] , ["gif","GIF173/","57.8%"] ,  ["gif","GIF200/","50%"] ,  ["gif","GIF400/","25%"] , ["gif","GIFT100/","100%"] , ["gif","GIFT173/","57.8%"] ,  ["gif","GIFT200/","50%"] ,  ["gif","GIFT400/","25%"] , ["png","PNG100/","100%"] , ["png","PNG173/","57.8%"] , ["png","PNG200/","50%"] , ["png","PNG400/","25%"] , ["png","PNGT100/","100%"] , ["png","PNGT173/","57.8%"] , ["png","PNGT200/","50%"] , ["png","PNGT400/","25%"] ]

screen = pygame.display.set_mode(size) #Screen Set 600x400
background = 152, 251, 152 # pale green


#-------------------------------------------------------------
#The switch function

def chngImg():
    cnt=make
    while cnt>0:
        switcher = {
            1: pygame.image.load("%s2.%s"%(ft[1],ft[0])),
            2: pygame.image.load("%s3.%s"%(ft[1],ft[0])),
            3: pygame.image.load("%s4.%s"%(ft[1],ft[0])),
            4: pygame.image.load("%s5.%s"%(ft[1],ft[0])),
            5: pygame.image.load("%s6.%s"%(ft[1],ft[0])),
            6: pygame.image.load("%s7.%s"%(ft[1],ft[0])),
            7: pygame.image.load("%s8.%s"%(ft[1],ft[0])),
            8: pygame.image.load("%s9.%s"%(ft[1],ft[0])),
            9: pygame.image.load("%s1.%s"%(ft[1],ft[0]))
        }
        img[cnt,0]=switcher.get(i,pygame.image.load("%s1.%s"%(ft[1],ft[0])))
        img[cnt,0] = pygame.transform.scale(img[cnt,0],(40, 40))
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
    
#-----------------------------------------------------------------
    while trialthis>0:

    #-------------------------------------------------------------
        while cnt>0:
            img[cnt,0]= pygame.image.load("%s1.%s"%(ft[1],ft[0])) #image.load
            img[cnt,0] = pygame.transform.scale(img[cnt,0],(20, 20)) 
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
