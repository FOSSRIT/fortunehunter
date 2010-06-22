#! /usr/bin/env python
from datetime import datetime
import sys,time,pygame,re
print "\n\nLoading..."
pygame.init()

# Scroll below the def () for the initial code for this program

#= .image() Animation Test ================================================================================

def imgTest():
    sizeIn=make=maxTrial=''

    while 1:
        print "\nImage Load Test Details\nFor default values, please leave the field blank"
        try:        
            print "\nSet size, formatted as '>height,width':"
            sizeIn=str(raw_input('>'))
            sizeIn.split(',')
            height=int(sizeIn[0])
            width=int(sizeIn[1])
        except:
            width=600
            height=400
        try:
            print "How many images would you like to draw?"
            make=int(raw_input('>'))
        except:
            make=5
        try:
            print "How many trials would you like to run?"
            maxTrial=int(raw_input('>'))
            break
        except:
            maxTrial=5
            break
    dateTime=str(datetime.now())
    f=open('./logs/Test Result - Image Animation - %s.csv'%dateTime,'a')
    f.write("Height (pixels)"+','+"Width (pixels)"+','+"Trial Runs"+','+"Image Objects Drawn")
    f.write("\n"+str(height)+','+str(width)+','+str(maxTrial)+','+str(make))
    f.write("\nFile Type"+','+"Time taken to load images to memory"+','+"Trials")
    ft="" #filetype
    img={}
    r=0 #frame refreshes
    i=1 #cycles images
    size = width, height
    t=0 #trial number n
    colorkey=(255, 152, 0)
    
    #the file type array will be iterated through as the test progresses to tell the program what extension and path to use for the images
    ftArr=[ [".bmp","./art/BMP16/"] , [".bmp","./art/BMP24/"] , [".bmp","./art/BMP32/"] , [".gif","./art/GIF/"] , [".gif","./art/GIFT/"] , [".jpg","./art/JPG1/"] , [".jpg","./art/JPG2/"] , [".jpg","./art/JPG3/"] , [".jpg","./art/JPG4/"] , [".png","./art/PNGI/"] , [".png","./art/PNGT/"] ]

    screen = pygame.display.set_mode(size) #Screen Set 600x400
    background = 152, 251, 152 # pale green

    def chngImg():
        cnt=make
        while cnt>0:
            img[cnt,0]=imgSwitch.get(i,pygame.image.load("%s1%s"%(ft[1],ft[0])))
            cnt=cnt-1
    
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

    while 1:
        cnt=make
        try:ft=ftArr[t]
        except:sys.exit("Test Complete")
        f.seek(0,2)
        f.write(str('\n'+ft[1]+' Test'))
        f.seek(0,2)
        start=time.time()
        imgSwitch={
            1: pygame.image.load("%s2%s"%(ft[1],ft[0])),
            2: pygame.image.load("%s3%s"%(ft[1],ft[0])),
            3: pygame.image.load("%s4%s"%(ft[1],ft[0])),
            4: pygame.image.load("%s5%s"%(ft[1],ft[0])),
            5: pygame.image.load("%s6%s"%(ft[1],ft[0])),
            6: pygame.image.load("%s7%s"%(ft[1],ft[0])),
            7: pygame.image.load("%s8%s"%(ft[1],ft[0])),
            8: pygame.image.load("%s9%s"%(ft[1],ft[0])),
        }        
        f.write(','+str(time.time()-start))

        print "Testing "+ft[1]
        trial=maxTrial
        
        while trial>0:
            while cnt>0:
                img[cnt,0]= pygame.image.load("%s1%s"%(ft[1],ft[0]))
                img[cnt,1]=  img[cnt,0].get_rect()
                img[cnt,2]= [2,2] #speed
                m=cnt*40 # named m cause i wanted some m&ms
                img[cnt,1]=img[cnt,1].move(m,m) #see? (it wasn't as tasty though)
                cnt=cnt-1
            
            r=0
            start=time.time()
            while 1:
                chngImg()
                i=i+1
                if i>9: i=1
                collision()
                screen.fill(background)
                r=r+1
                if r>500: break
                
            print 1/((time.time()-start)/r)
            f.seek(0,2)
            f.write(','+str(1/((time.time()-start)/r)))
            trial=trial-1

        t=t+1
    f.close()

#= .sprite() Animation Test ===============================================================================
def spriteTest():
    print "spriteTest called"
    dateTime=str(datetime.now())
    file=open('./logs/testresult - %s.csv'%dateTime,'a')

#= Scalability Test =======================================================================================
def scaleTest():
    dateTime=str(datetime.now())
    print "scaleTest called"
    file=open('./logs/testresult - %s.csv'%dateTime,'a')

while 1:
    print "\n\nWelcome to the master File Type Tester Interface"
    print "Authors: Scott 'JT' Mengel and Dave Silverman"
    print "\nPlease select the test(s) you want to run in the order you want to run them (Do not seperate them with any characters)."
    print "Please Note: The logs for the tests you are running will automatically be placed in the logs/ directory in the test folder as a .csv file. \n"
    print "1. Simple File Type Variety Test, as images (NOTE: In development)"
    print "2. Simple File Type variety Test, as sprites (NOTE: not working yet)"
    print "3. Selected Scalability Test (NOTE: not working yet)"

    dateTime=str(datetime.now())
    acceptible='^[1-3]$'
    list={ 1:imgTest,
        2:spriteTest,
        3:scaleTest }
    keyIn="temp val"

    while 1:
        keyIn=str(raw_input(">"))
        for i in keyIn:
            try: 
                if re.search(acceptible,i): list.get(int(i))()
            except BaseException: print sys.exc_info()[0]
        break

#ILY GEOFF A

