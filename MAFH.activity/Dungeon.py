import os.path

from Room import Room
from constants import MAP_PATH
from JournalIntegration import do_load, load_dungeon_by_id

 ########################################################################
 #Dungeon class:  stores a 2d array of rooms representing the dungeon
 #                reads/parses a text file containing the data for a dungeon
 #######################################################################


class Dungeon:
  def __init__(self,fileName):
    self.fileName=fileName
    self.start=[0,0]
    self.index=0

    ###INITALIZE DICTIONARY, TUPLE:ROOM PAIRINGS
    self.rooms={}

    currentX=0
    currentY=0
    ###ENUM###
    NONE=-1
    PUZZLE=0
    LOCKED=1
    BOTH=2
    UNLOCKED=3
    EXIT=4
    ENTRANCE=5
    SHOP=6
    PUZZLEROOM=7
    HIDDEN=8

    if os.path.exists( MAP_PATH + self.fileName ):
        dgnFile=open( MAP_PATH + self.fileName,'r')
        d_dict = do_load( dgnFile )
        dgnFile.close()
    else:
        d_dict = load_dungeon_by_id( fileName )

    self.sizeX = d_dict['x']
    self.sizeY = d_dict['y']
    self.theme = d_dict['theme']
    self.name = d_dict['name']
    self.id = d_dict['d_id']
    self.next = d_dict['next']

    for line in d_dict['roomstr']:
      ###initialize room variables###
      doorN=False
      doorNFlag=NONE
      doorS=False
      doorSFlag=NONE
      doorE=False
      doorEFlag=NONE
      doorW=False
      doorWFlag=NONE
      roomFlag=NONE
      en1=0
      en2=0
      en3=0
      en4=0
      it1=0
      it2=0
      it3=0
      it4=0
      ###check characters in current line, set variables accordingly###
      ###KEY:1st character=door to north
      ###    2nd=door to south
      ###    3rd=door to east
      ###    4th=door to west
      ###    5th=if the room is a shop
      ###    6-9=enemy number in each slot (0 for no enemy)

      if line[0]=='N':
        doorN=True
        if line[1]=='l':
          doorNFlag=LOCKED
        elif line[1]=='p':
          doorNFlag=PUZZLE
        elif line[1]=='b':
          doorNFlag=BOTH
        elif line[1]=='u':
          doorNFlag=UNLOCKED
        elif line[1]=='e':
          doorNFlag=ENTRANCE
        elif line[1]=='x':
          doorNFlag=EXIT

      if line[2]=='S':
        doorS=True
        if line[3]=='l':
          doorSFlag=LOCKED
        elif line[3]=='p':
          doorSFlag=PUZZLE
        elif line[3]=='b':
          doorSFlag=BOTH
        elif line[3]=='u':
          doorSFlag=UNLOCKED
        elif line[3]=='e':
          doorSFlag=ENTRANCE
        elif line[3]=='x':
          doorSFlag=EXIT

      if line[4]=='W':
        doorW=True
        if line[5]=='l':
          doorWFlag=LOCKED
        elif line[5]=='p':
          doorWFlag=PUZZLE
        elif line[5]=='b':
          doorWFlag=BOTH
        elif line[5]=='u':
          doorWFlag=UNLOCKED
        elif line[5]=='e':
          doorWFlag=ENTRANCE
        elif line[5]=='x':
          doorWFlag=EXIT

      if line[6]=='E':
        doorE=True
        if line[7]=='l':
          doorEFlag=LOCKED
        elif line[7]=='p':
          doorEFlag=PUZZLE
        elif line[7]=='b':
          doorEFlag=BOTH
        elif line[7]=='u':
          doorEFlag=UNLOCKED
        elif line[7]=='e':
          doorEFlag=ENTRANCE
        elif line[7]=='x':
          doorEFlag=EXIT

      if line[8]=='S':
        roomFlag=SHOP
      elif line[8]=='P':
        roomFlag=PUZZLE
      else:
        event=int(line[8])

      rm=Room(doorN,doorNFlag,doorS,doorSFlag,doorE,doorEFlag,doorW,doorWFlag,roomFlag,line[9],line[10],line[11],line[12],line[13],line[15],line[17],line[19])

      #check hidden items
      if line[14]=='h':
        rm.it1.hidden=True
      elif line[14]=='v':
        rm.it1.hidden=False
      if line[16]=='h':
        rm.it2.hidden=True
      elif line[16]=='v':
        rm.it2.hidden=False
      if line[18]=='h':
        rm.it3.hidden=True
      elif line[18]=='v':
        rm.it3.hidden=False
      if line[20]=='h':
        rm.it4.hidden=True
      elif line[20]=='v':
        rm.it4.hidden=False

      #check battle items
      if line[14]=='b':
        rm.it1.battle=True
      if line[16]=='b':
        rm.it2.battle=True
      if line[18]=='b':
        rm.it3.battle=True
      if line[20]=='b':
        rm.it4.battle=True

      if doorSFlag==ENTRANCE or doorNFlag==ENTRANCE or doorWFlag==ENTRANCE or doorEFlag==ENTRANCE:
        self.start=(currentX,currentY)

      #start=[1,4]

      self.rooms[(currentX,currentY)]=rm
      ###update position in array###
      currentX+=1

      if currentX==self.sizeX:
        currentY+=1
        currentX=0

      if currentY>self.sizeY:
        break
