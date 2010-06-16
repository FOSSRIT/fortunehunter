#! /usr/bin/env python
#import sys

#= .image() Animation Test ========
#- set up -------------------------

def imgSetup():
    print "imgSetup"

def imgTest():
    print "imgTest"

#= .sprite() Animation Test =======
#- set up -------------------------

def spriteSetup():
    print "spriteSetup"

def spriteTest():
    print "spriteTest"


#= Scalability Test ===============
#- set up -------------------------

def scaleSetup():
    print "scaleSetup"

def scaleTest():
    print "scaleTest"


print "\n\nWelcome to the master File Type Tester Interface"
print "Authors: Scott 'JT' Mengel and Dave Silverman"
print "\nPlease select the test(s) you want to run in the order you want to run them."
print "Enter 'Exit' into the prompt to close the program. (NOTE: not working yet)\n"
print "1. Simple File Type Variety Test, as images (NOTE: not working yet)"
print "2. Simple File Type variety Test, as sprites (NOTE: not working yet)"
print "3. Selected Scalability Test (NOTE: not working yet)"
i=int(1)
file=open('./testresult.csv','a')

testOrder
keyIn

while 1:
    keyIn=int(raw_input(i+">"))
    if keyIn is not "done":
        testOrder[i]=keyIn
        int=int(int+1)
    else: break
