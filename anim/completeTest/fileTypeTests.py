#! /usr/bin/env python
#import sys


print "\n\nWelcome to the master File Type Tester Interface"
print "Authors: Scott 'JT' Mengel and Dave Silverman"
print "\nPlease select the test(s) you want to run in the order you want to run them."
print "Enter 'Exit' into the prompt to close the program. (NOTE: not working yet)\n"
print "0. Run all tests"
print "1. Simple File Type Variety Test, as images (NOTE: not working yet)"
print "2. Simple File Type variety Test, as sprites (NOTE: not working yet)"
print "3. Selected Scalability Test (NOTE: not working yet)"

file=open('./testresult.csv','a')
i=int(1)
keyIn="temp val"


#= .image() Animation Test ========
#- test ---------------------------
def imgTest():
    print "imgTest"


#= .sprite() Animation Test =======
#- test ---------------------------
def spriteTest():
    print "spriteTest"


#= Scalability Test ===============
#- test ---------------------------
def scaleTest():
    print "scaleTest"


#= Super (every) Test =============
#- test ---------------------------
def superTest():
    print "superTest"

list=[superTest,imgTest, spriteTest, scaleTest]

while True:
	keyIn=raw_input(">")

	try:
		temp = int(keyIn)
		list[temp]()
	except:
		break
