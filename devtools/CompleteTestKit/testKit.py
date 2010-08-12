#! /usr/bin/env python
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# testKit - a testing kit run in terminal for pygame benchmarking pygame methods
#
# Authors: Scott JT Mengel & Dave Silverman
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
print "\n\nLoading..."
from datetime import datetime
import sys
import time
import pygame
import re
import os
from animObj.Scene import Scene
from animObj.DrawableObject import DrawableObject
from animObj.DynamicDrawableObject import DynamicDrawableObject

os.system("clear")

"""The file type array will be iterated through as the test progresses to tell 
the program what extension and path to use for the images

preferences[0] - Multiple Tests -
    [0][0] - screenWidth
    [0][1] - screenHeight
    [0][2] - images
    [0][3] - trials
    [0][9] - file to write to...
preferences[1] - speedTest Specific -
    None currenlty inplimented
preferences[2] - scaleTest Specific -
    [2][0] - scale x
    [2][1] - scale y
preferences[3] - rotateTest Specific -
    [3][0] - Degree to rotate image to
    [3][1] - how many rotational steps to take
preferences[4] - Drawable Object Specific

@param keyIn:   The user's selected tests from the main() menu
"""
def getValues(keyIn):
    preferences={}
    print "\nTest Details\nFor default values, please leave the field blank"
    preferences[0]={}

    try:
        print "\nSet size, formatted as '>width,height':"
        print "Default value is '1200,700'."
        screenSize  = str(raw_input('>>>'))
        screenSize  = screenSize.split(',')
        preferences[0][0] = int(screenSize[0])
        preferences[0][1] = int(screenSize[1])
    except:
        print "Value was erroneous/blank, Default set..."
        preferences[0][0]=1200
        preferences[0][1]=700

    if '1' in keyIn or '2' in keyIn or '4' in keyIn:
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
        try:
            print "\nHow many frames per trial would you like to run?"
            print "(The average framerate is taken from this value.)"
            print "Default value is 500 frames."
            preferences[0][4]=int(raw_input('>>>'))
        except:         
            print "Value was erroneous/blank, Default set..."
            preferences[0][4]=500

    if '2' in keyIn:
        preferences[2]={}
        try:
            print "\nWhat would you like to scale the images to in the ",
            print "scalability test? (format as '>width,height', in pixels)"
            print "NOTE: Scalability test is built to resize from 160x160, ",
            print "80x80, 69x69 and 40x40 pixel sizes"
            sizeTo = raw_input(">>>").split(',')
            preferences[2][0] = int(sizeTo[0])
            preferences[2][1] = int(sizeTo[1])
        except:
            print "Value was erroneous/blank, Default set..."
            preferences[2][0] = 40
            preferences[2][1] = 40

    if '3' in keyIn:
        preferences[3]={}
        try:
            print "\nTo what degree would you like to rotate (in degrees)?"
            print "Default value is 90 degrees."
            preferences[3][0] = int(raw_input('>>>'))
        except:
            print "Value was erroneous/blank, Default set..."
            preferences[3][0] = 90
        try:
            print "\nHow many steps would you like to take?"
            print "Default value is 18 steps."
            preferences[3][1] = int(raw_input('>>>'))
        except:
            print "Value was erroneous/blank, Default set..."
            preferences[3][1] = 18

    print "END OF INFO GATHERING - Testing beginning now...\n"
    return preferences



"""Image() Animation Test 
This test will simply load the image(s) to screen, and move them around to
create a CPU stressful environment.  The performance of the CPU in this 
environment is measured in the average frame rate demonstrated in a sample of
500 frames.  Once this test is completed and written to file, the test is rerun
using surface.convert() to see if converting all of the different file types
will consequentially even out the framerates between tests.

@param preferences: user-made 2D list of preferences to be shared across tests
"""
def imgTest(preferences):
    pygame.init()
    # Create the list that will direct each test to its respective filetype
    ftArr=[
        [".bmp","./art/BMP16/"], [".bmp","./art/BMP24/"], 
        [".bmp","./art/BMP32/"], [".gif","./art/GIF/" ] , 
        [".gif","./art/GIFT/" ], [ ".jpg","./art/JPG1/"],
        [".jpg","./art/JPG2/"] , [".jpg","./art/JPG3/" ], 
        [ ".jpg","./art/JPG4/"], [".png","./art/PNGI/"] ,
        [".png","./art/PNGT/" ]
    ]
    
    # Load preferences into human-readable variables
    screenWidth = preferences[0][0]
    screenHeight = preferences[0][1]
    maxImage = preferences[0][2]
    maxTrial = preferences[0][3]
    maxFrame = preferences[0][4]

    ft=""   #filetype
    img={}
    i=1   #cycles images

    # Attempt to load previously accessed .csv file & create a new one if fails
    try:
        f=preferences[0][9]
        f.write("\n\n")
    except:
        f=preferences[0][9]=\
            open('./logs/Test Results - %s- %s.csv'\
                %(str( os.system("uname -vr") ),str( datetime.now() )),'a')

    # Format the header of the .csv for this test's data
    f.write("Speed Test - "+str(datetime.now()))
    f.write(",Width (pixels),Height (pixels),Frames per Trial,Image Objects"+
        " Drawn")
    f.write("\n,"+str(screenWidth)+','+str(screenHeight)+','+
        str(maxFrame)+','+str(maxImage))
    f.write("\nFile Type"+','+"Time taken to load images to memory (seconds)")
    for trial in range(maxTrial): 
        f.write(",Trial "+str(trial+1)+" (frames per second)")

    # Create the display screen for these tests
    screen = pygame.display.set_mode( [int(screenWidth),int(screenHeight)] )
    BACKGROUND = pygame.image.load("./art/GIF/Room.gif").convert()
    pygame.display.set_caption("Speed Test Window")
    screen.blit( BACKGROUND,(0,0) )
    pygame.display.flip()

    for trialType in range( len(ftArr) ):
        # set ft as the current test's filetype 
        ft=ftArr[trialType]
        f.write(str('\n'+ft[1]+' Speed Test'))

        start=time.time() # time how long it takes to load surfaces
        imgSwitch={
            1: pygame.image.load("%s2%s"%(ft[1],ft[0])),
            2: pygame.image.load("%s3%s"%(ft[1],ft[0])),
            3: pygame.image.load("%s4%s"%(ft[1],ft[0])),
            4: pygame.image.load("%s5%s"%(ft[1],ft[0])),
            5: pygame.image.load("%s6%s"%(ft[1],ft[0])),
            6: pygame.image.load("%s7%s"%(ft[1],ft[0])),
            7: pygame.image.load("%s8%s"%(ft[1],ft[0])),
            8: pygame.image.load("%s9%s"%(ft[1],ft[0])),}

        f.write(',' + str(time.time()-start) )
        print "Speed Test: "+ft[1]+" extension "+ft[0]

        for aTrial in range(maxTrial):
            for eachImage in range(maxImage):

                # Load the img dictionary with the image, rectangle, & velocity
                img[eachImage , 0] = pygame.image.load("%s1%s" %(ft[1],ft[0]))
                img[eachImage , 1] = img[eachImage , 0].get_rect()
                img[eachImage , 2] = [ 2 , 2 ] # velocity of image(s)
                displace = eachImage*40
                img[ eachImage,1 ] = img[ eachImage,1 ].move(displace,displace)

            start=time.time()

            for frame in range(maxFrame):
                for image in range(maxImage):
                    # Change surfaces, effectively animating the image
                    img[image,0]=imgSwitch.get(i,None)

                    # Collision detection 
                    if img[image,1].left < 0 or img[image,1].right >screenWidth:
                        img[image,2]=[ -img[image,2][0], img[image,2][1] ]
                    if img[image,1].top < 0 or img[image,1].bottom>screenHeight:
                        img[image,2]=[ img[image,2][0], -img[image,2][1] ]
                    
                    # movement
                    img[image,1] = img[image,1].move(img[image,2])
                    screen.blit(img[image,0],img[image,1])

                # print screen's current state to the display
                pygame.display.flip()
                i+=1
                if i>8: i=1

                screen.blit(BACKGROUND,(0,0))
            # Results are shown in the terminal and saved in the .csv file
            print 1/((time.time()-start)/maxFrame)
            f.write(','+str(1/((time.time()-start)/maxFrame)))

    ft="" #filetype
    img={}
    i=1 #cycles images

    f.write("\n\nUsing .convert()")
    f.write("\nFile Type"+','+"Time taken to load images to memory (seconds)")
    for trial in range(maxTrial): f.write(",Trial "+str(trial+1)+
        " (frames per second)")

    # display screen created
    screen = pygame.display.set_mode( [screenWidth,screenHeight] )
    pygame.display.set_caption("Speed convert() Test Window")
    screen.blit( BACKGROUND,(0,0) )
    pygame.display.flip()

    # Loop through all the filetypes queued up for the test
    for trialType in range( len(ftArr) ):
        # determine this test's filetype
        ft=ftArr[trialType]
        f.write(str('\n'+ft[1]+' Speed convert() Test'))

        # take the time it takes to load all the converted images - This will 
        # take longer since the surfaces are now being loaded and rendered into 
        # a 'raw' format - However, this improves future performance.
        start=time.time() 
        imgSwitch={
            1: pygame.image.load("%s2%s"%(ft[1],ft[0])).convert(),
            2: pygame.image.load("%s3%s"%(ft[1],ft[0])).convert(),
            3: pygame.image.load("%s4%s"%(ft[1],ft[0])).convert(),
            4: pygame.image.load("%s5%s"%(ft[1],ft[0])).convert(),
            5: pygame.image.load("%s6%s"%(ft[1],ft[0])).convert(),
            6: pygame.image.load("%s7%s"%(ft[1],ft[0])).convert(),
            7: pygame.image.load("%s8%s"%(ft[1],ft[0])).convert(),
            8: pygame.image.load("%s9%s"%(ft[1],ft[0])).convert(),}

        f.write(',' + str(time.time()-start) )
        print "Convert Test: "+ft[1]+" extension "+ft[0]

        # execute the trial run
        for trial in range(maxTrial):
            # store image information in img{}
            for image in range(maxImage):
                img[image,0]= pygame.image.load("%s1%s"%(ft[1],ft[0]))
                img[image,1]=  img[image,0].get_rect()
                img[image,2]= [2,2] #speed
                displace = image * 40 # stagger images so they don't overlap
                img[image,1]=img[image,1].move( displace,displace )
            start=time.time()

            for frame in range(maxFrame):
                for image in range(maxImage):
                    img[image,0]=imgSwitch.get(i,None)
                    if img[image,1].left < 0 or img[image,1].right >screenWidth:
                        img[image,2]=[ -img[image,2][0], img[image,2][1] ]

                    if img[image,1].top < 0 or img[image,1].bottom>screenHeight:
                        img[image,2]=[ img[image,2][0], -img[image,2][1] ]

                    img[image,1] = img[image,1].move(img[image,2])
                    screen.blit(img[image,0],img[image,1])

                pygame.display.flip()
                i=i+1
                if i>8: i=1
                screen.blit(BACKGROUND,(0,0))

            print 1/((time.time()-start)/maxFrame)
            f.seek(0,2)
            f.write(','+str(1/((time.time()-start)/maxFrame)))
    preferences[0][9]=f




"""Scalability Test 
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

@param preferences: user-made 2D list of preferences to be shared across tests
"""
def scaleTest(preferences):
    pygame.init()
    sizeTo = [ preferences[2][0],preferences[2][1] ]
    screenWidth = preferences[0][0]
    screenHeight = preferences[0][1]
    maxImage = preferences[0][2]
    maxTrial = preferences[0][3]
    maxFrame = preferences[0][4]

    try:
        f=preferences[0][9]
        f.write("\n\n")
    except:
        f=preferences[0][9]=\
            open('./logs/Test Results - %s- %s.csv'\
                %(str( os.system("uname -vr") ),str( datetime.now() )),'a')

    img={}
    ft="" #filetype
    r=0 #frame refreshes
    i=1 #cycles images
    size = screenWidth,screenHeight
    t=0 #trial number n
    colorkey=(255, 152, 0)

# paths to and extensions for image files to be turned into surfaces
    ftArr=[ 
        [".bmp","art/BMP16/BMP16100/"],[".bmp","art/BMP16/BMP16173/"],
        [".bmp","art/BMP16/BMP16200/"],[".bmp","art/BMP16/BMP16400/"],
        [".bmp","art/BMP24/BMP24100/"],[".bmp","art/BMP24/BMP24173/"],
        [".bmp","art/BMP24/BMP24200/"],[".bmp","art/BMP24/BMP24400/"],
        [".gif","art/GIF/GIF100/"]    ,[".gif","art/GIF/GIF173/"],
        [".gif","art/GIF/GIF200/"]    ,[".gif","art/GIF/GIF400/"],
        [".gif","art/GIFT/GIFT100/"]  ,[".gif","art/GIFT/GIFT173/"], 
        [".gif","art/GIFT/GIFT200/"]  ,[".gif","art/GIFT/GIFT400/"],
        [".png","art/PNGI/PNG100/"]   ,[".png","art/PNGI/PNG173/"],
        [".png","art/PNGI/PNG200/"]   ,[".png","art/PNGI/PNG400/"],
        [".png","art/PNGT/PNGT100/"]  ,[".png","art/PNGT/PNGT173/"],
        [".png","art/PNGT/PNGT200/"]  ,[".png","art/PNGT/PNGT400/"] ]

    f.write("Scaling Test"+str(datetime.now()))
    f.write(",Width (pixels)"+','+"Height (pixels)"+','+
        "Trial Runs"+','+"Image Objects Drawn")
    f.write("\n,"+str(screenWidth)+','+str(screenHeight)+
        ','+str(maxTrial)+','+str(maxImage))
    f.write("\nFile Type"+','+"Time taken to load images to memory (seconds)")    
    for trial in range(maxTrial): f.write(",Trial "+str(trial+1)+
        " (frames per second)")

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Scaling Test Window")
    BACKGROUND = pygame.image.load("./art/GIF/Room.gif").convert()
    screen.blit( BACKGROUND,(0,0) )
    pygame.display.flip()

    for trialType in range( len(ftArr) ):
        ft=ftArr[trialType]

        print "Scale Test: "+ft[1]+" extension "+ft[0]
        trialthis=maxTrial
        f.seek(0,2)
        f.write(str('\n'+ft[1]+' Scale Test'))
        f.seek(0,2)
        start=time.time()
# This timer will reflect the time taken to load and resize images in memory
# This is also where we need advise regarding implementing convert()   
        switcher = {
            1: pygame.transform.scale( pygame.image.load("%s2%s"%(ft[1],
                ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            2: pygame.transform.scale( pygame.image.load("%s3%s"%(ft[1],
                ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            3: pygame.transform.scale( pygame.image.load("%s4%s"%(ft[1],
                ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            4: pygame.transform.scale( pygame.image.load("%s5%s"%(ft[1],
                ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            5: pygame.transform.scale( pygame.image.load("%s6%s"%(ft[1],
                ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            6: pygame.transform.scale( pygame.image.load("%s7%s"%(ft[1],
                ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            7: pygame.transform.scale( pygame.image.load("%s8%s"%(ft[1],
                ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            8: pygame.transform.scale( pygame.image.load("%s9%s"%(ft[1],
                ft[0])).convert(),(sizeTo[0],sizeTo[1] )),
            9: pygame.transform.scale( pygame.image.load("%s1%s"%(ft[1],
                ft[0])).convert(),(sizeTo[0],sizeTo[1] ))
        }

        f.write(',')
        f.write( str(time.time()-start) )
# Here ends the loading section, and hereafter we jump into the main loop

        for trial in range(maxTrial):
            for image in range(maxImage):
# establish the initial state for the images of the next trial
                img[image,0]= pygame.image.load("%s1%s"%(ft[1],ft[0]))
                img[image,0]= pygame.transform.scale(img[image,0], \
                    (sizeTo[0], sizeTo[1])) 
                img[image,1]=  img[image,0].get_rect()
                img[image,2]= [2,2] #speed
                displace=image*40

    # Here I move images to avoid indistinguishable stacks of image rectangles
                img[image,1]=img[image,1].move(displace,displace)
            start=time.time()

            for frame in range(maxFrame):
    # This loop is the 'main event' so to speak, as it is the section that is
    # measured in terms of frames per second
                screen.blit(BACKGROUND,(0,0))
                for image in range(maxImage):
                    img[image,0]=switcher.get(i,None)
                    if img[image,1].left < 0 or img[image,1].right >screenWidth:
                        img[image,2]=[ -img[image,2][0], img[image,2][1] ]

                    if img[image,1].top < 0 or img[image,1].bottom>screenHeight:
                        img[image,2]=[ img[image,2][0], -img[image,2][1] ]

                    img[image,1] = img[image,1].move(img[image,2]) 
    # Move the 'ball' image accordingly, plot the change
                    screen.blit(img[image,0],img[image,1])

                pygame.display.flip()
    # "Make it so, number two", on those changes above
                i=i+1
                if i>8: i=1

            print 1/((time.time()-start)/maxFrame)
            f.seek(0,2)
            f.write(','+str(1/((time.time()-start)/maxFrame)))        
    preferences[0][9]=f




"""rotateTest is a test that will move a selected image by way of a select 
variety of methods, with the controlled variables being the method, the number
of steps, the screen's dimensions, the number of trials, and the rotation (in 
degrees) for each step.  The static variables include the image itself.

@param preferences: user-made 2D list of preferences to be shared across tests
"""
def rotateTest(preferences):
    pygame.init()
    # Same functionality as above: loading in preferences into human-readable
    # variable names below
    screenWidth = preferences[0][0]
    screenHeight = preferences[0][1]
    maxRotate = preferences[3][0]
    degreeRotate = preferences[3][0] / preferences[3][1]

    # Make or reopen the file being used by the program
    try:
        f=preferences[0][9]
        f.write("\n\n")
    except:
        f=preferences[0][9]=\
            open('./logs/Test Results - %s- %s.csv'\
                %(str( os.system("uname -vr") ),str( datetime.now() )),'a')

    # Create the display screen for the program
    screen=pygame.display.set_mode((screenWidth,screenHeight))
    BACKGROUND = pygame.image.load("./art/GIF/Room.gif").convert()
    pygame.display.set_caption("Rotate Test Window")
    screen.blit( BACKGROUND,(0,0) )
    pygame.display.flip()

    # List of details: Original image, active image, rectangle of image and the
    # degrees of seperation from the initial orientation.
    # In hindsight, we had pretty much created a Sprite object by saving this 
    # data in an object with the surface itself.
    myImage=[ pygame.Surface.convert( pygame.image.load("art/GIF/1.gif") ) ,
        pygame.Surface.convert( pygame.image.load("art/GIF/1.gif") ),
        pygame.Surface.convert( pygame.image.load("art/GIF/1.gif")).get_rect() ,
        0 ]

    # Write the header/column names for this test in the .csv file
    f.write("Rotation Testing,"+str(datetime.now())+",Total Rotation,"+
        "Rotational Steps,Degrees per Step,Original Image Surface")
    f.write("\n,,"+str(preferences[3][0])+','+str(preferences[3][1])+','+
        str(degreeRotate)+','+str( myImage[0] ))
    f.write("\nTest type,Time of test,Screen capture location,"+
        "Final image surface info")

    # The loop for the test - totalTime is so that we could measure how long all
    # rotation calculations took in sum. Note that we do not write to the list
    # value myImage[0] because that is the location of the original image
    print "\nTest 1 : Same image called evey time, original image not edited.\n"
    totalTime=0
    for step in range(preferences[3][1]):
        stepStart=time.time()
        myImage[3]= int( myImage[3] ) + degreeRotate
        myImage[1]=pygame.transform.rotate(myImage[0],myImage[3])
        myImage[2]=myImage[1].get_rect()
        screen.blit(BACKGROUND,(0,0))

        screen.blit( myImage[1] ,
            (((screenWidth/2) - (myImage[1].get_width()/2)) ,
            ((screenHeight/2) - (myImage[1].get_height()/2))) )
        pygame.display.flip()

        stepEnd=time.time()

        totalTime+=(float(stepEnd)-float(stepStart))

        print "\n%35s%35s" %("Rotation #"     , str(step+1) )
        print "%35s%35s" %( "Degrees from 0"  , str(myImage[3]) )
        print "%35s%35s" %( "Time: Calc. Rot.", str(stepEnd-stepStart) )
        print "%35s%35s" %( "Orig. Img Info" , str(myImage[0]) )
        print "%35s%35s" %( "Rot. Img. Rect.", str(myImage[2]) )
        print "%35s%35s" %( "Rot. Img. Info" , str(myImage[1]) )

    screenPath = './logs/screencaps/reference-'+ str(datetime.now()) +'.bmp'
    pygame.image.save(screen,screenPath) # Save a screen capture for records
    f.write("\nReference Image Saved,"+str(totalTime)+','+str(screenPath)+','+
        str(myImage[1]))

    # simple continuous rotate test
    # Test practices are similar to the above test above, however in this test 
    # we ignor myImage[0] and merely continuously rotate the same image, causing
    # severe warping of the surface as it attempts to average pixel color values
    # This issue is a symptom of rotating a rendered image - with a vector-based
    # image this issue would not come up (assuming that you are not rotating a 
    # rendered surface of a .svg file, which would be again subject to warping)
    myImage=[ pygame.Surface.convert( pygame.image.load("art/GIF/1.gif") ) ,
        pygame.Surface.convert( pygame.image.load("art/GIF/1.gif") ),
        pygame.Surface.convert( pygame.image.load("art/GIF/1.gif")).get_rect(),
        0 ]
    totalTime=0

    for step in range(preferences[3][1]):
        stepStart=time.time()
        myImage[1]=pygame.transform.rotate(myImage[1],degreeRotate)
        myImage[2]=myImage[1].get_rect()
        screen.blit( myImage[1] ,
            (((screenWidth/2) - (myImage[1].get_width()/2)) ,
            ((screenHeight/2) - (myImage[1].get_height()/2))) )
        pygame.display.flip()
        stepStop=time.time()

        totalTime+=float(stepStop)-float(stepStart)
        myImage[3]+=degreeRotate

        print "\n%35s%35s" %("Rotation #"     , str(step+1) )
        print "%35s%35s" %( "Degrees from 0"  , str(myImage[3]) )
        print "%35s%35s" %( "Time: Calc. Rot.", str(stepEnd-stepStart) )
        print "%35s%35s" %( "Orig. Img Info" , str(myImage[0]) )
        print "%35s%35s" %( "Rot. Img. Rect.", str(myImage[2]) )
        print "%35s%35s" %( "Rot. Img. Info" , str(myImage[1]) )

    screenPath = './logs/screencaps/Continuous-'+ str(datetime.now()) +'.bmp'
    pygame.image.save(screen,screenPath) # Save a screen capture for records
    f.write("\nContinuous Rotate,"+str(totalTime)+','+str(screenPath)+','+
        str(myImage[1]))

    preferences[0][9]=f #Store the log file information back in preferences





"""
Drawable Object testing will attempt to recreate the earlier tests to 
demonstrate the benefits of using of sprite objects instead of directly 
handling surface objects.  While it is known that, through very specific and 
delicate programming methods, directly controlling the surfaces can result in
higher frame rates than using sprite objects, such programming is above the 
skill level of a common programmer and would require every program to program
their own very specific animation handler, which costs a development team time
that could be otherwise spent on the specifics of their program.  Our solution 
is an object that encapsulates all that we need it to do in a simple and easy to
access heirarchy of objects (Scenes hold multiple Drawable Objects, which in 
turn can be the most specific Dynamic Drawable Objects).

@param preferences: user-made 2D list of preferences to be shared across tests
"""
def drawableObjectTest(preferences):
    pygame.init()
    #preferences are loaded in and placed in human-readable variables
    screenWidth = preferences[0][0]
    screenHeight = preferences[0][1]
    maxImage = preferences[0][2]
    maxFrame = preferences[0][4]
    maxTrial = preferences[0][3]

    # try to open the previously used file, 'f', or create a new file
    try:
        f=preferences[0][9]
        f.write("\n\n")
    except:
        f=preferences[0][9]=\
            open('./logs/Test Results - %s- %s.csv'\
                %(str( os.system("uname -vr") ),str( datetime.now() )),'a')

    # Append to the file the header information for this test's data
    f.write("Dynamic Drawable Object Testing - "+str(datetime.now())+"," )
    f.write("Width (pixels),Height (pixels),Number of Images,Frames per Trial")
    f.write("\n,"+str(screenWidth)+","+str(screenHeight)+","+str(maxImage)+","+
        str(maxFrame)+"\nType of Test,Time to load myScene" )

    for trial in range(maxTrial):f.write(",Trial "+str(trial+1)+
        " (frames per second)")

    # 'Constants' that would otherwise be passed in declared ^^ 
    # Begin creating test variables

    screen = pygame.display.set_mode( (screenWidth,screenHeight) )
    BACKGROUND = pygame.image.load("./art/GIF/Room.gif").convert()
    clock=pygame.time.Clock()

    # Make the screen and the background image
    pygame.display.set_caption("Sprite Speed Test Window")
    screen.blit( BACKGROUND,(0,0) )
    pygame.display.flip()
    
    # DDO Speed Test Below
    # For this test we decided to use the .gif format, due to its economic size
    # Here begins the loading process and associated timer
    start=time.time()
    surfaceList = [
            pygame.image.load("./art/GIF/1.gif").convert(),
            pygame.image.load("./art/GIF/2.gif").convert(),
            pygame.image.load("./art/GIF/3.gif").convert(),
            pygame.image.load("./art/GIF/4.gif").convert(),
            pygame.image.load("./art/GIF/5.gif").convert(),
            pygame.image.load("./art/GIF/6.gif").convert(),
            pygame.image.load("./art/GIF/7.gif").convert(),
            pygame.image.load("./art/GIF/8.gif").convert(),
            pygame.image.load("./art/GIF/9.gif").convert()]

    # DDO is a list, populated here, containing all the Dynamic Drawable Objects
    DDO = [DynamicDrawableObject( surfaceList, '',   0,   0, False,  1, 2, 2 ),]
    for img in range(maxImage)[1:]:
        DDO.append(  DynamicDrawableObject( surfaceList, '', (img*40) ,(img*40), 
            False, 72, 2, 2 )  )
    myScene = Scene( DDO[0] )
    myScene.addObjects( DDO[1:] )
    f.write( "\nDDO Speed Test,"+str(time.time()-start)  ) # time taken, flushed

    # Trial loops DDO Speed test
    for trial in range(maxTrial):
        for img in range(maxImage):
            myScene.getObject(img).setPosition( (40*img),(40*img) )
        print "Trial ",str(trial+1)
        clock.tick()
        start = time.time()

        # Loop through every frame's refreshes 
        for frame in range(maxFrame):
            myScene.moveObjects()

            # Collision detection in the for loop
            for img in range(maxImage):
                if myScene.getObject(img).getYPos() > screenHeight or \
                myScene.getObject(img).getYPos() < 0:
                    myScene.getObject(img).setSpeed(
                        None,-(myScene.getObject(img).getYSpeed()))

                if myScene.getObject(img).getXPos() > screenWidth or \
                myScene.getObject(img).getXPos() < 0:
                    myScene.getObject(img).setSpeed(
                        -(myScene.getObject(img).getXSpeed()),None)

            # call updates to change positions, clear to remove old pixels
            # update the screen to look like what we've just calculated above
            # by passing a list of 'dirty' pixels to the update, we ensure that
            # pixels that have not changed in any way will not be needlessly
            # redrawn
            myScene.update( clock.get_time() )
            myScene.clear(screen,BACKGROUND)
            pygame.display.update( myScene.draw(screen) )
            clock.tick()
        print maxFrame/(time.time()-start)
        f.write( "," + str(maxFrame/(time.time()-start) ) )






    # Mixed DO and DDO test
    # Reinitalize the screen
    screen = pygame.display.set_mode( (screenWidth,screenHeight) )
    BACKGROUND = pygame.image.load("./art/GIF/Room.gif").convert()
    clock=pygame.time.Clock()

    # Make the screen and the background image
    pygame.display.set_caption("Sprite Speed Test Window")
    screen.blit( BACKGROUND,(0,0) )
    pygame.display.flip()

    # Here begins the loading process and associated timer
    start=time.time()
    surfaceList = [
            pygame.image.load("./art/GIF/1.gif").convert(),
            pygame.image.load("./art/GIF/2.gif").convert(),
            pygame.image.load("./art/GIF/3.gif").convert(),
            pygame.image.load("./art/GIF/4.gif").convert(),
            pygame.image.load("./art/GIF/5.gif").convert(),
            pygame.image.load("./art/GIF/6.gif").convert(),
            pygame.image.load("./art/GIF/7.gif").convert(),
            pygame.image.load("./art/GIF/8.gif").convert(),
            pygame.image.load("./art/GIF/9.gif").convert(),]

    # mixedDO is a list containing a Drawable Object as well as DDOs
    mixedDO = [ DrawableObject( surfaceList, '', 0, 0, False ) ]
    for img in range(maxImage)[1:]:
        mixedDO.append( DynamicDrawableObject( surfaceList,'',(img*40),(img*40), 
            False, 72, 2, 2 ) )
    myScene = Scene( mixedDO[0] )
    myScene.addObjects( mixedDO[1:] )

    # time taken, flushed
    f.write( "\nMixed DO and DDO Speed Test,"+str(time.time()-start)  )

    # By here, myScene is set and we should only interface with myScene
    for trial in range(maxTrial):
        for img in range(maxImage):
            myScene.getObject(img).setPosition( (40*img),(40*img) )
        print "Trial ",str(trial+1)
        clock.tick()
        start = time.time()
        for frame in range(maxFrame):
            dirtyList = []
            myScene.moveObjects()
            
            # Collision detection in the for loop below
            for img in range(maxImage):
                if myScene.getObject(img).getYPos() > screenHeight or \
                myScene.getObject(img).getYPos() < 0:
                    myScene.getObject(img).setSpeed(
                        None,-(myScene.getObject(img).getYSpeed()) )

                if myScene.getObject(img).getXPos() > screenWidth or \
                myScene.getObject(img).getXPos() < 0:
                    myScene.getObject(img).setSpeed(
                        -(myScene.getObject(img).getXSpeed()),None)

            # call updates to change positions, clear to remove old pixels
            # update the screen to look like what we've just calculated above
            # by passing a list of 'dirty' pixels to the update, we ensure that
            # pixels that have not changed in any way will not be needlessly
            # redrawn
            myScene.update( clock.get_time() )
            myScene.clear(screen,BACKGROUND)
            pygame.display.update( myScene.draw(screen) )
            clock.tick()
        print maxFrame/(time.time()-start)
        f.write( "," + str(maxFrame/(time.time()-start) ) )





"""
The main section of the code
"""
def main():
    while 1:
        pygame.display.quit()
        try:preferences[0][9].close()
        except: pass
        print """
 Welcome to the Master Test Interface
    
 Authors: Scott 'JT' Mengel and Dave Silverman

 Please select the test(s) you want to run in the order you want to run them
 Do not seperate them with any characters, for example type '>>>134'
 Please Note: The logs for the tests you are running will be automatically 
 placed in the 'logs/' directory in the test folder as a .csv file.

     1. The pygame.image.load() surface speed test 
        (with and without pygame.surface.convert() testing)
     2. The pygame.transform.scale() surface scalability test
     3. The pygame.transform.rotate() tests
     4. The (developed in-house object) DrawableObject tests.
    
 Enter 'Exit' to return to the terminal and other menu options to come!
 """

        acceptible='^[1-4]$'
        menuItems={ 1:imgTest,
            2:scaleTest,
            3:rotateTest,
            4:drawableObjectTest}
        keyIn="temp val"

        while True:
            keyIn=str(raw_input(">>> "))
            if 'exit' in keyIn or 'Exit' in keyIn: 
                print "\nClosing...\n"
                sys.exit()
            for i in keyIn:
                if not re.search(acceptible,i): break
                else:
                    preferences=dict( getValues(keyIn) )
                    for i in keyIn:
                        menuItems.get(int(i))(preferences)
                    break
            break

if __name__ == "__main__":
    main()
#ILY GEOFF A
