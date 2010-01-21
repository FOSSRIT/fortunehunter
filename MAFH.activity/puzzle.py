from random import *
from time import time

class PuzzlePiece:
    """ Class that holds current and absolute coordinates & image file
        The x and y coords are 0 based. """
        
    def __init__ (self, absx, absy, curx, cury, filename):
        self.cury = cury
        self.curx = curx
        self.absy = min(absy, 1)
        self.absx = min(absx, 2)
        self.filename = filename
        self.isHole=False

    def __eq__ (self, other):
        if isinstance(other, PuzzlePiece):
            return self.curx == other.curx and self.cury == other.cury and self.absx == other.absx and self.absy == other.absy and self.filename == other.filename
        return False

    def __ne__ (self, other):
        return not self.__eq__ (other)


    def move (self, direction):
        """ Moving direction is actually the opposite of what is passed.
        We are moving the hole position, so if you slice a piece down into the hole,
        that hole is actually moving up."""
        if direction == SLIDE_UP and self.cury < 1:
            self.cury += 1
            return True
        elif direction == SLIDE_DOWN and self.cury > 0:
            self.cury -= 1
            return True
        elif direction == SLIDE_LEFT and self.curx < 2:
            self.curx += 1
            return True
        elif direction == SLIDE_RIGHT and self.curx > 0:
            self.curx -= 1
            return True
        return False
        
    def clone(self):
        return PuzzlePiece(self.absx, self.absy, self.curx, self.cury, self.filename)
            

class PuzzleMap (object):

    """ This class holds the game logic.
    The current pieces position is held in self.pieces_map[YROW][XROW]."""
    

    def __init__ (self, pieceMap):
        self.pieceMap = pieceMap
        self.solved = False
        self.holePos = pieceMap[2][1]

        self.holePos.isHole=True

    def reset (self):
        for x in range(2):
            for y in range(1):
                self.pieceMap[x][y].cury = self.pieceMap[x][y].absy
                self.pieceMap[x][y].curx = self.pieceMap[x][y].absx

        self.solved = True
        
    def randomize (self):
        """ To make sure the randomization is solvable, we don't simply shuffle the numbers.
        We move the hole in random directions through a finite number of iterations. """
        iterations = 2 * 3 * (int(100*random())+1)
        t = time()
        for i in range(iterations):
            self.do_move(int(4*random())+1)
        t = time() - t


        # Now move the hole to the bottom right
        for x in range(3-self.holePos.curx-1):
            self.do_move(SLIDE_LEFT)
        for y in range(2-self.holePos.cury-1):
            self.do_move(SLIDE_UP)

    def do_move (self, slide_direction):
        # What piece are we going to move?
        oldHolePos = self.holePos.clone()
        
        if self.holePos.move(slide_direction):
            # Move was a success, now swap pieces in map
            temp=self.pieceMap[self.holePos.curx][self.holePos.cury]
            self.pieceMap[self.holePos.curx][self.holePos.cury]=self.holePos
            self.pieceMap[oldHolePos.curx][oldHolePos.cury]=temp
            return True
        return False

def is_solved (self):
        self.solved = True
        x=-1
        y=-1
        for row in self.pieceMap:
            x+=1
            y=-1
            for piece in row:
                y+=1
                if not y == piece.absy or not x == piece.absx:
                    self.solved = False
        return self.solved