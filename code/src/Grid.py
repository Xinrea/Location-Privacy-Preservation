from Cell import Cell

class Grid(object):
    def __init__(self, cellCount, minX, maxX, minY, maxY):
        self.topLevelCells = [[0]*cellCount for _ in range(cellCount)]
        xIncrement = (maxX-minX)/cellCount
        yIncrement = (maxY-minY)/cellCount
        for(i = 0; i < cellCount; i += 1):
            for (j = 0; j < cellCount; j += 1):
                self.topLevelCells[i][j] = Cell(minX+xIncrement*i,minY+yIncrement*j,xIncrement,yIncrement,str(i)+","+str(j))
        self.posInListForm = {}
        for(i = 0; i < len(self.getCells()); i += 1):
            posInListForm[self.getCells()[i]] = i

    def getN(self):
        return len(self.topLevelCells)

    def getXofCell(self, c1):
        for(i = 0; i < len(self.topLevelCells); i += 1):
            for(j = 0; j < len(self.topLevelCells); j += 1):
                if(self.topLevelCells[i][j] == c1):
                    return i+1
        return -1

    def getYofCell(self, c1):
        for(i = 0; i < len(self.topLevelCells); i += 1):
            for(j = 0; j < len(self.topLevelCells); j += 1):
                if(self.topLevelCells[i][j] == c1):
                    return j+1
        return -1
    
    def getCells(self):
        tbR = []
        for(i = 0; i < len(self.topLevelCells); i += 1):
            for(j = 0; j < len(self.topLevelCells); j += 1):
                tbR.append(topLevelCells[i][j])
        return tbR

    def getPosInListForm(self, c1):
        return self.posInListForm[c1]
    
    def getCellMatrix(self):
        return self.topLevelCells

    def areAdjacent(self, c1, c2):
        c1x = -1
        c1y = -1
        c2x = -1
        c2y = 1
		c1found = False
        c2found = False
		for (i = 0; i < self.getN(); i += 1):
			for (j = 0; j < self.getN(); j += 1):
				if (c1 == self.topLevelCells[i][j]):
					c1x = i
					c1y = j
					c1found = True
				if (c2 == self.topLevelCells[i][j]):
					c2x = i
					c2y = j
					c2found = True

		if (c1found == false or c2found == false):
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
		if (c1x == c2x+1 and c1y == c2y) 
			return True
		if (c1x == c2x+1 and c1y == c2y+1)
			return True
		if (c1x == c2x and c1y == c2y+1)
			return True
		if (c1x == c2x-1 and c1y == c2y+1)
			return True
		if (c1x == c2x-1 and c1y == c2y) 
			return True
		if (c1x == c2x-1 and c1y == c2y-1)
			return True
		if (c1x == c2x and c1y == c2y-1)
			return True
		if (c1x == c2x+1 and c1y == c2y-1)
			return True
		return False

    def getAdjacentCells(self, c1):
        cells = self.getCells()
        tbr = []
        for(i in cells):
            if(this.areAdjacent(i,c1)):
                tbr.append(i)
        return tbr

    def giveInterpolateRoute(self, start, end):
        startx = -1
        starty = -1
        endx = -1
        endy = -1
        startfound = False
        endfound = False
        