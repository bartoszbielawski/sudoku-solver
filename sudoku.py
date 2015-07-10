#!/usr/bin/python

#
# A Simple Sudoku Solver
# v. 0.1
# Bartosz Bielawski
#

import string

class sudoku:
    fullCell = set(range(1,10))

    def __init__(self, initString):
        initString = initString.translate(None, " \n\t")
        print initString

        if len(initString) != 81:
            raise Exception("Init string should contain 81 characters")

        self.board = [[sudoku.fullCell.copy() for i in xrange(9)] for j in xrange(9)]

        cnt = 0

        #initialize known values
        for c in initString:
            col = cnt // 9;             #calculate row
            row = cnt % 9;              #calculate col

            if c in string.digits:
                digitValue = ord(c) - ord('0')
                #print "{} @ {}, {}".format(digitValue, row, col);
                self.board[col][row] = set([digitValue])

            cnt += 1

    def isCellComplete(self, sx, sy):
        return len(self.get(sx, sy)) == 1;

    def getSolvedCells(self):
        return sum(1 for x in xrange(9) for y in xrange(9) if self.isCellComplete(x,y))

    def isSolved(self):
        return self.getSolvedCells() == 81;

    def get(self, x, y):
        return self.board[x][y]

    def _getSquare(self, sx, sy):
        return (sx // 3, sy // 3)

    def removeFromSquare(self, sx, sy, n):
        (squareX, squareY) = self._getSquare(sx, sy)
        for x in xrange(3):
            for y in xrange(3):
                dx = squareX * 3 + x
                dy = squareY * 3 + y
                if not (dx == sx and dy == sy):
                    self.get(dx,dy).discard(n)

    def removeFromLines(self, sx, sy, n):
        for x in xrange(9):
            if x != sx:
                self.get(x, sy).discard(n)
        for y in xrange(9):
            if y != sy:
                self.get(sx, y).discard(n)

    def removeHiddenSingle(self, sx, sy):
        if self.isCellComplete(sx, sy):
            return;

        s = self.get(sx,sy).copy()
        (kx,ky) = self._getSquare(sx, sy)
        for x in xrange(3):
            for y in xrange(3):
                ex = kx * 3 + x;
                ey = ky * 3 + y;
                if not (ex == sx and ey == sy):
                    s -= self.get(ex, ey)
        if len(s) == 1:
            self.board[sx][sy] = s;
            return

        s = self.get(sx, sy).copy()
        for x in xrange(9):
            if (x != sx):
                s = s - self.get(x, sy)
        if len(s) == 1:
            self.board[sx][sy] = s;
            return;

        s = self.get(sx, sy).copy()
        for y in xrange(9):
            if (y != sy):
                s = s - self.get(sx, y)
        if len(s) == 1:
            self.board[sx][sy] = s;
            return;


    def iterate(self):
        for x in xrange(9):
            for y in xrange(9):
                if self.isCellComplete(x,y):
                    (e,) = self.get(x, y)
                    self.removeFromSquare(x, y, e);
                    self.removeFromLines(x, y, e);
                else:
                    self.removeHiddenSingle(x, y);
        return self.getSolvedCells()

    def __str__(self):
        return repr(self.board)

    def str(self):
        result = ""
        for x in xrange(9):
            for y in xrange(9):
                l = len(self.get(x,y))
                if l  == 1:
                    (e,) = self.get(x,y)
                    result += str(e);
                elif l == 0:
                    result += "!"
                else:
                    result += "?"
            result += "\n";
        return result;


hidden = """
9??7?2???
???3?5?91
??2?16?4?
2?????46?
??72?????
83???9???
4?????835
??1??????
??8??71??
"""

ciotki1 = """
6??2???7?
??7?14???
????56??2
?23????8?
?68???9?7
4?????1?5
3???9??4?
???4?58??
?4?3?2???
"""

ciotki2 = """
???49??3?
1????37??
?39????1?
?4??75??2
9??1????7
?6?9??3??
??2????76
??52?9???
6???1?2??
"""
s = sudoku(ciotki2)

print "Initial state"
print s

cmd = "s"
while True:
    i = raw_input(">")

    if len(i) != 0:
        cmd = i

    if cmd == "h":
        print("h - help\ns - step\nf - print full state\nq - quit")

    if cmd == "s":
        print "Solved cells:", s.iterate()
        print s.str()

    if cmd == "f":
        print str(s)

    if cmd == "q":
        break;

    if s.isSolved():
        print "Solution found!"
        break;
