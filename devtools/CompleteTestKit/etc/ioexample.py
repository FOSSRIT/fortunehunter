#! /usr/bin/env python
#
print "\nWelcome to the master File Type Tester Interface"
print "Authors: Scott 'JT' Mengel and Dave Silverman"
print "\nPlease select the test(s) you want to run, in the order you want to run them, seperated by commas.\n"
print "1. Simple File Type Variety Test, as images"
print "2. Simple File Type variety Test, as sprites"
print "3. Selected Scalability Test"
file=open('./localfile','a')
keyIn=0

while 1:
    try:
        keyIn = int(raw_input(">"))
        print "You have selected %i"%keyIn
        file.seek(5)
        file.write("File Accessed!%s"%str(keyIn))
        break
    except ValueError:
        print "Error: out of bounds."
