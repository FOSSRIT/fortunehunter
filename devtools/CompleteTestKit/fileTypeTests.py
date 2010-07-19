#! /usr/bin/env python
from datetime import datetime
import sys,time,pygame,re
print "\n\nLoading..."
pygame.init()

'''
The file type array will be iterated through as the test progresses to tell the program what extension and path to use for the images

Current issue is the fact that the attributes declared in the upper method is not being seen or involved in the inner methods
ergo, I must manually pass the details to and from the getValues(keyIn) to the other method objects. I will probably do this
in-line, if it allows me, as I call the other objects.  This should get interesting. Actually, that would call the getValues as many
times as I have requested a test, defeating the purpose of having a module that collects data pertenent to these tests once before
the tests are run; so i will run the getVal() return the data in an array which is then passed onto all def's thereafter.

preferences[0] - All Tests -
    [0][0] - screenWidth
    [0][1] - screenHeight
    [0][2] - images
    [0][3] - trials
    [0][9] - file to write to...
preferences[1] - speedTest Specific
    None currenlty inplimented
preferences[2] - scaleTest Specific
    [2][0] - scale x
    [2][1] - scale y
'''
def getValues(keyIn):
#trialSize=None
    preferences={}

    print "\nTest Details\nFor default values, please leave the field blank"
    preferences[0]={}
    try:
        print "\nSet size, formatted as '>width,height':"
        print "Default value is '600,400'."
        screenSize  = str(raw_input('>>>'))
        screenSize  = screenSize.split(',')
        preferences[0][0] = int(screenSize[0])
        preferences[0][1] = int(screenSize[1])

    except:
        print "Value was erroneous/blank, Default set..."
        preferences[0][0]=600
        preferences[0][1]=400
    try:
        print "\nHow many images would you like to draw?"
        print "Default value is 5 images."
        preferences[0][2]=int(raw_input('>>>'))
    except:
        print "Value was erroneous/blank, Default set..."
        preferences[0][2]=5
    try:
        print "\nHow many trials would you like to run?"
        print "Default value is 5 trials."
        preferences[0][3]=int(raw_input('>>>'))
    except:
        print "Value was erroneous/blank, Default set..."
        preferences[0][3]=5
    if '2' in keyIn:
        preferences[2]={}
        try:
            print "\nWhat would you like to scale the images to in the scalability test? (format as '>width,height', in pixels)"
            print "NOTE: Scalability test is built to resize from 160x160, 80x80, 69x69 and 40x40 pixel sizes"
            sizeTo = raw_input(">>>").split(',')
            preferences[2][0] = int(sizeTo[0])
            preferences[2][1] = int(sizeTo[1])
        except:
            print "Value was erroneous/blank, Default set..."
            preferences[2][0] = 40
            preferences[2][1] = 40

    print "END OF INFO GATHERING - Testing beginning now...\n"
    return preferences

'''Image() Animation Test 
This test will simply load the image(s) to screen, and move them around to
create a CPU stressful environment.  The performance of the CPU in this 
environment is measured in the average frame rate demonstrated in a sample of
500 frames.  Once this test is completed and written to file, the test is rerun
using surface.convert() to see if converting all of the different file types
will consequentially even out the framerates between tests.
'''
def imgTest(preferences):
    ftArr=[
        [".bmp","./art/BMP16/"], [".bmp","./art/BMP24/"] , [".bmp","./art/BMP32/"],
        [".gif","./art/GIF/" ] , [".gif","./art/GIFT/" ] , [ ".jpg","./art/JPG1/"],
        [".jpg","./art/JPG2/"] , [".jpg","./art/JPG3/" ] , [ ".jpg","./art/JPG4/"],
        [".png","./art/PNGI/"] , [".png","./art/PNGT/" ]
    ]
    screenWidth = preferences[0][0]
    screenHeight = preferences[0][1]
    numImages = preferences[0][2]
    maxTrial = preferences[0][3]
    try:
        f=preferences[0][9]
    except:
        f=preferences[0][9]=open('./logs/Test Results - %s.csv'%str(datetime.now()),'a')
    f.write("\n\nSpeed Test - "+str(datetime.now()))
    f.write(",Width (pixels)"+','+"Height (pixels)"+','+"Trial Runs"+','+"Image Objects Drawn")
    f.write("\n,"+str(screenWidth)+','+str(screenHeight)+','+str(maxTrial)+','+str(numImages))
    f.write("\nFile Type"+','+"Time taken to load images to memory"+','+"Trials (frames per second)")
    ft="" #filetype
    img={}
    r=0 #frame refreshes
    i=1 #cycles images
    t=0 #trial number n
    print "width,height",
    print screenWidth,
    print ",",
    print screenHeight
    screen = pygame.display.set_mode( [int(screenWidth),int(screenHeight)] ) #Screen Set 600x400
    background = 152, 251, 152 # pale green

    while 1:
        cnt=numImages
        try:ft=ftArr[t]
        except: 
            print "\nTest Complete\n"
            break
        f.seek(0,2)
        f.write(str('\n'+ft[1]+' Speed Test'))
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
        f.write(',')
        f.write(str(time.time()-start))
        #print time.time()-start()
        print "Speed Test: "+ft[1]+" extension "+ft[0]
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
                cnt=numImages
                while cnt>0:
                    print cnt
                    img[cnt,0]=imgSwitch.get(i,None)
                    if img[cnt,1].left < 0 or img[cnt,1].right > screenWidth:
                        img[cnt,2]=[ -img[cnt,2][0], img[cnt,2][1] ]
                    if img[cnt,1].top < 0 or img[cnt,1].bottom > screenHeight:
                        img[cnt,2]=[ img[cnt,2][0], -img[cnt,2][1] ]
                    img[cnt,1] = img[cnt,1].move(img[cnt,2])
                    screen.blit(img[cnt,0],img[cnt,1])
                    cnt=cnt-1
                pygame.display.flip()
                i=i+1
                if i>8: i=1
                screen.fill(background)
                r=r+1
                if r>500: break
                
            print 1/((time.time()-start)/r)
            f.seek(0,2)
            f.write(','+str(1/((time.time()-start)/r)))
            trial=trial-1
        t=t+1

    ft="" #filetype
    img={}
    r=0 #frame refreshes
    i=1 #cycles images
    t=0 #trial number n    
    
    f.write("\n\nNow using .convert()")
    f.write("\nFile Type"+','+"Time taken to load images to memory"+','+"Trials (frames per second)")
    ft="" #filetype
    img={}
    r=0 #frame refreshes
    i=1 #cycles images
    t=0 #trial number n

    screen = pygame.display.set_mode( [screenWidth,screenHeight] ) #Screen Set 600x400
    background = 152, 251, 152 # pale green

    while 1:
        cnt=numImages
        try:ft=ftArr[t]
        except: 
            print "\nTest Complete\n"
            break
        f.seek(0,2)
        f.write(str('\n'+ft[1]+' Speed convert() Test'))
        f.seek(0,2)
        start=time.time()
        imgSwitch={
            1: pygame.image.load("%s2%s"%(ft[1],ft[0])).convert(),
            2: pygame.image.load("%s3%s"%(ft[1],ft[0])).convert(),
            3: pygame.image.load("%s4%s"%(ft[1],ft[0])).convert(),
            4: pygame.image.load("%s5%s"%(ft[1],ft[0])).convert(),
            5: pygame.image.load("%s6%s"%(ft[1],ft[0])).convert(),
            6: pygame.image.load("%s7%s"%(ft[1],ft[0])).convert(),
            7: pygame.image.load("%s8%s"%(ft[1],ft[0])).convert(),
            8: pygame.image.load("%s9%s"%(ft[1],ft[0])).convert(),
        }
        f.write(',')
        f.write( str(time.time()-start) )
        print "Convert Test: "+ft[1]+" extension "+ft[0]
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
                cnt=numImages
                while cnt>0:
                    img[cnt,0]=imgSwitch.get(i,None)
                    if img[cnt,1].left < 0 or img[cnt,1].right > screenWidth:
                        img[cnt,2]=[ -img[cnt,2][0], img[cnt,2][1] ]
                    if img[cnt,1].top < 0 or img[cnt,1].bottom > screenHeight:
                        img[cnt,2]=[ img[cnt,2][0], -img[cnt,2][1] ]
                    img[cnt,1] = img[cnt,1].move(img[cnt,2])
                    screen.blit(img[cnt,0],img[cnt,1])
                    cnt=cnt-1
                pygame.display.flip()
                i=i+1
                if i>8: i=1
                screen.fill(background)
                r=r+1
                if r>500: break
                
            print 1/((time.time()-start)/r)
            f.seek(0,2)
            f.write(','+str(1/((time.time()-start)/r)))
            trial=trial-1

        t=t+1

'''Scalability Test 
The scalability test is still very much hard coded and not very elegant, but
this is a theme with all our code.

The pseudo-code goes as follows:
Gather in varaibles such as how many trials, images to draw on screen, and what
to resize the 160, 80, 69, and 40 pixel square images to.

Then the code will generate the lists reflecting which directories to access 
and their associated filetypes and finally there are loops to cycle through
trials where 500 frames of n moving images are placed onto the screen after
they are transform.scale()'d and convert()'d

Last step, information is printed to the terminal and, once implemented, to
a .csv file in the logs directory.
'''
def scaleTest(preferences):

# delete these 3 lines when tests have proven program functional
#make=input("How many images would you like to load?\n>") numImages
#trial=input("How many runs per trial?\n>")
#sizeTo=input("What would you like to resize to? Seperate with a comma, eg: x,y\n>" )

    sizeTo = [ preferences[2][0],preferences[2][1] ]
    screenWidth = preferences[0][0]
    screenHeight = preferences[0][1]
    numImages = preferences[0][2]
    maxTrial = preferences[0][3]
    try:
        f=preferences[0][9]
    except:
        f=preferences[0][9]=open('./logs/Test Results - %s.csv'%str(datetime.now()),'a')
    
    img={}
    ft="" #filetype
    r=0 #frame refreshes
    i=1 #cycles images
    size = screenWidth,screenHeight
    t=0 #trial number n
    colorkey=(255, 152, 0)
    
# paths to and extensions for image files to be turned into surfaces
    ftArr=[ 
        [".bmp","art/BMP16/BMP16100/"] ,
        [".bmp","art/BMP16/BMP16173/"] ,
        [".bmp","art/BMP16/BMP16200/"] ,
        [".bmp","art/BMP16/BMP16400/"] ,
        [".bmp","art/BMP24/BMP24100/"] , 
        [".bmp","art/BMP24/BMP24173/"] , 
        [".bmp","art/BMP24/BMP24200/"] , 
        [".bmp","art/BMP24/BMP24400/"] , 
        [".gif","art/GIF/GIF100/"] , 
        [".gif","art/GIF/GIF173/"] ,  
        [".gif","art/GIF/GIF200/"] ,  
        [".gif","art/GIF/GIF400/"] , 
        [".gif","art/GIFT/GIFT100/"] , 
        [".gif","art/GIFT/GIFT173/"] ,  
        [".gif","art/GIFT/GIFT200/"] ,  
        [".gif","art/GIFT/GIFT400/"] , 
        [".png","art/PNGI/PNG100/"] , 
        [".png","art/PNGI/PNG173/"] , 
        [".png","art/PNGI/PNG200/"] , 
        [".png","art/PNGI/PNG400/"] , 
        [".png","art/PNGT/PNGT100/"] , 
        [".png","art/PNGT/PNGT173/"] , 
        [".png","art/PNGT/PNGT200/"] , 
        [".png","art/PNGT/PNGT400/"] ]
    
    f.write("\n\nScaling Test"+str(datetime.now()))
    f.write(",Width (pixels)"+','+"Height (pixels)"+','+"Trial Runs"+','+"Image Objects Drawn")
    f.write("\n,"+str(screenWidth)+','+str(screenHeight)+','+str(maxTrial)+','+str(numImages))
    f.write("\nFile Type"+','+"Time taken to load images to memory"+','+"Trials (frames per second)")
    
    screen = pygame.display.set_mode(size)
    background = 152, 251, 152 # pale green

    #23456789123456789212345678931234567894123456789512345678961234567897123456789*

    # This is the beginning of the actual test loops; this program is a very rough 
    # learning exercise which we desire to polish to such a state that it can be 
    # used to accurately benchmark the XO laptop's speed capabilities
    while 1:
        cnt=numImages
        try:ft=ftArr[t]
        except: 
            print "\nTest Complete\n"
            break
        print "Scale Test: "+ft[1]+" extension "+ft[0]
        trialthis=maxTrial
        f.seek(0,2)
        f.write(str('\n'+ft[1]+' Scale Test'))
        f.seek(0,2)
        start=time.time()
    # This timer will reflect the time taken to load and resize images in memory
        switcher = {
    # This is also where we need advise regarding implementing convert()
            1: pygame.transform.scale( pygame.image.load("%s2%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            2: pygame.transform.scale( pygame.image.load("%s3%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            3: pygame.transform.scale( pygame.image.load("%s4%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            4: pygame.transform.scale( pygame.image.load("%s5%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            5: pygame.transform.scale( pygame.image.load("%s6%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            6: pygame.transform.scale( pygame.image.load("%s7%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            7: pygame.transform.scale( pygame.image.load("%s8%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            8: pygame.transform.scale( pygame.image.load("%s9%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            9: pygame.transform.scale( pygame.image.load("%s1%s"%(ft[1],ft[0])).convert(),(sizeTo[0],sizeTo[1] ))
        }
        f.write(',')
        f.write( str(time.time()-start) )
    # Here ends the loading section, and hereafter we jump into the main loop
        while trialthis>0:
            while cnt>0: 
    # establish the initial state for the images of the next trial
                img[cnt,0]= pygame.image.load("%s1%s"%(ft[1],ft[0]))
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

                cnt=numImages # For each 'ball' icon loaded
                while cnt>0: # Cycle and check if the 'ball' should bounce off the wall
                    img[cnt,0]=switcher.get(i,None)
                    if img[cnt,1].left < 0 or img[cnt,1].right > screenWidth:
                        img[cnt,2]=[ -img[cnt,2][0], img[cnt,2][1] ]
                    if img[cnt,1].top < 0 or img[cnt,1].bottom > screenHeight:
                        img[cnt,2]=[ img[cnt,2][0], -img[cnt,2][1] ]
                    img[cnt,1] = img[cnt,1].move(img[cnt,2]) 
    # Move the 'ball' image accordingly, plot the change
                    screen.blit(img[cnt,0],img[cnt,1])
                    cnt=cnt-1 
                pygame.display.flip()
    # "Make it so, number two," on those changes above
                i=i+1
                if i>8: i=1
                screen.fill(background)
                r=r+1
                if r>500: break
    # After 500 frames, we print the average frame rate to the terminal
            print 1/((time.time()-start)/r)
            f.seek(0,2)
            f.write(','+str(1/((time.time()-start)/r)))
            trialthis=trialthis-1
            preferences[0][9]=f
        t=t+1

def rotateTest():
    pass
    
    
    
    
#2345678911234567892123456789312345678941234567895123456789612345678971234567898
while 1:
    print "\n\nWelcome to the master File Type Tester Interface"
    print "Authors: Scott 'JT' Mengel and Dave Silverman"
    print "\nPlease select the test(s) you want to run in the order you want to run them (Do not seperate them with any characters)."
    print "Please Note: The logs for the tests you are running will automatically be placed in the 'logs/' directory in the test folder as a .csv file. \n"
    print "1. image.load() surface speed test (with and without surface.convert() testing)"
    print "2. transform.scale() surface Selected Scalability Test"
    print "3. transform.rotate() tests"
    print "Other menu options to come!\n"

    acceptible='^[1-3]$'
    list={ 1:imgTest,
        2:scaleTest,
        3:rotateTest }
    keyIn="temp val"

    while 1:
        keyIn=str(raw_input(">>>"))
        if keyin.
        for i in keyIn:
            if not re.search(acceptible,i): break
            else:
                preferences=dict(getValues(keyIn))
                for i in keyIn:
                    list.get(int(i))(preferences)
                break
        break

#ILY GEOFF A

"""
CANVAS_SIZE=(600,400)
BLACK=(0,0,0)

screen=pygame.display.set_mode(CANVAS_SIZE)
run=0

while 1:
    pygame.display.set_caption("Test 1 : %s (Referred)" %(ftArr[run][2]) )
    # myimage[0] is the convert()'ed image surface, to remain untouched
    myimage = [
        pygame.Surface.convert(pygame.image.load( "%s%s" %(  ftArr[run][1],ftArr[run][0]  )  )) ,
        pygame.Surface.convert(pygame.image.load( "%s%s" %(  ftArr[run][1],ftArr[run][0]  )  )),
        pygame.Surface.convert(pygame.image.load( "%s%s" %(  ftArr[run][1],ftArr[run][0]  )  )).get_rect() ,
        0
        ]
        
    iterate=0
    print "\nTest 1 : Same image referred evey time (original image not edited).\n"
    while iterate<36:
    
        time.sleep(.5)
        start=time.time()
        myimage[3]= int( myimage[3] ) + 10
        myimage[1]=pygame.transform.rotate(myimage[0],myimage[3])
        myimage[2]=myimage[1].get_rect()
        screen.fill(BLACK)
        screen.blit( myimage[1] ,
            ( -( myimage[1].get_width() - myimage[0].get_width() )/2 ,
              -( myimage[1].get_height()-myimage[0].get_height() )/2 ) )
        
        pygame.display.flip()
"""

