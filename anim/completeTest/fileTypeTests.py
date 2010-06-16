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
file=open('./testresult.csv','a')
list=[imgSetup, spriteSetup, scaleSetup]
keyIn="temp val"

while True:
	keyIn=raw_input(">")
	try:
		temp = int(keyIn)
		list[temp - 1]()
	except:
		break

#print list+" and switching now..."
#
#for i in list:
#        call what's in list[i] somehow
#    print i
#    if i == keyInt 
#    list[int(i)]
#    switch.get( i , sys.exit("Goodbye!") )
#    print 'looped through'
