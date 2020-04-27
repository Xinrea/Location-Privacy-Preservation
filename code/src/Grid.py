from Cell import Cell
from typing import List

class Grid(object):
    def __init__(self, cellCount, minX, maxX, minY, maxY):
        self.topLevelCells = [[0]*cellCount for _ in range(cellCount)]
        xIncrement = (maxX-minX)/cellCount
        yIncrement = (maxY-minY)/cellCount
        for i in range(cellCount):
            for j in range(cellCount):
                self.topLevelCells[i][j] = Cell(minX+xIncrement*i,minY+yIncrement*j,xIncrement,yIncrement,str(i)+","+str(j))
        self.posInListForm = {}
        for i in range(len(self.getCells())):
            self.posInListForm[self.getCells()[i]] = i

    def getN(self):
        return len(self.topLevelCells)

    def getXofCell(self, c1):
        for i in range(len(self.topLevelCells)):
            for j in range(len(self.topLevelCells)):
                if(self.topLevelCells[i][j] == c1):
                    return i+1
        return -1

    def getYofCell(self, c1):
        for i in range(len(self.topLevelCells)):
            for j in range(len(self.topLevelCells)):
                if(self.topLevelCells[i][j] == c1):
                    return j+1
        return -1
    
    def getCells(self) -> List[Cell]:
        tbR = []
        for i in range(len(self.topLevelCells)):
            for j in range(len(self.topLevelCells)):
                tbR.append(self.topLevelCells[i][j])
        return tbR

    def getPosInListForm(self, c1):
        return self.posInListForm[c1]
    
    def getCellMatrix(self):
        return self.topLevelCells

    def getCellByName(self,name:str):
        xy = name.split(',')
        return self.topLevelCells[int(xy[0])][int(xy[1])]

    def areAdjacent(self, c1, c2):
        c1x = -1
        c1y = -1
        c2x = -1
        c2y = 1
        c1found = False
        c2found = False
        for i in range(self.getN()):
            for j in range(self.getN()):
                if (c1 == self.topLevelCells[i][j]):
                    c1x = i
                    c1y = j
                    c1found = True
                if (c2 == self.topLevelCells[i][j]):
                    c2x = i
                    c2y = j
                    c2found = True

        if (c1found == False or c2found == False):
            print("cells not found, cannot compute adjacency")
            return False
        if (c2x == c1x+1 and c2y == c1y):
            return True
        if (c2x == c1x+1 and c2y == c1y+1):
            return True
        if (c2x == c1x and c2y == c1y+1):
            return True
        if (c2x == c1x-1 and c2y == c1y+1):
            return True
        if (c2x == c1x-1 and c2y == c1y):
            return True
        if (c2x == c1x-1 and c2y == c1y-1):
            return True
        if (c2x == c1x and c2y == c1y-1):
            return True
        if (c2x == c1x+1 and c2y == c1y-1):
            return True
        if (c1x == c2x+1 and c1y == c2y):
            return True
        if (c1x == c2x+1 and c1y == c2y+1):
            return True
        if (c1x == c2x and c1y == c2y+1):
            return True
        if (c1x == c2x-1 and c1y == c2y+1):
            return True
        if (c1x == c2x-1 and c1y == c2y):
            return True
        if (c1x == c2x-1 and c1y == c2y-1):
            return True
        if (c1x == c2x and c1y == c2y-1):
            return True
        if (c1x == c2x+1 and c1y == c2y-1):
            return True
        return False

    def getAdjacentCells(self, c1):
        cells = self.getCells()
        tbr = []
        for i in cells:
            if(self.areAdjacent(i,c1)):
                tbr.append(i)
        return tbr

    def giveInterpolatedRoute(self, start, end):
        startx = -1
        starty = -1
        endx = -1
        endy = -1
        startfound = False
        endfound = False
        for i in range(self.getN()):
            for j in range(self.getN()):
                if(start == self.topLevelCells[i][j]):
                    startx = i
                    starty = j
                    startfound = True
                if(end == self.topLevelCells[i][j]):
                    endx = i
                    endy = j
                    endfound = True
        if(startfound == False or endfound == False):
            print("Cell Not Found")
            return
        tbr = []
        currx = startx
        curry = starty
        while(True):
            tbr.append(self.topLevelCells[currx][curry])
            if(endx > currx):
                currx += 1
            elif(endx < currx):
                currx -= 1
            else:
                currx = currx
            if(endy > curry):
                curry += 1
            elif(endy < curry):
                curry -= 1
            else:
                curry = curry
            if(currx == endx and curry == endy):
                break
        return tbr

    def findShortestLengthBetween(self, start, end):
        shortestPath = self.giveInterpolatedRoute(start,end)
        shortestPath.append(end)
        return len(shortestPath)