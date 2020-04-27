import overload_function
from typing import List
from Trajectory import Trajectory
from Grid import Grid
from Cell import Cell
class GridTrajectory(object):
    @overload_function
    def __init__(self):
        self.trajCells = []

    @__init__.overload
    def __init__(self,t:Trajectory,g:Grid,interpWanted:bool):
        self.trajCells = []
        gridCells = g.getCells()
        for i in range(t.getSize()):
            p = t.getPoint(i)
            found = False
            for c in gridCells:
                if(c.inCell(p)):
                    self.trajCells.append(c)
                    found = True
                    break
            if(found == False):
                self.trajCells.append(g.getCellMatrix()[0][0])
                found = True
        newTrajCells = []
        newTrajCells.append(self.trajCells[0])
        for i in range(1,len(self.trajCells)-1):
            if(self.trajCells[i] == self.trajCells[len(newTrajCells)-1]):
                pass
            else:
                newTrajCells.append(self.trajCells[i])
        if(self.trajCells[len(self.trajCells)-1] != self.trajCells[len(self.trajCells)-2]):
            newTrajCells.append(self.trajCells[len(self.trajCells)-1])
        if(len(newTrajCells) == 1):
            newTrajCells.append(self.trajCells[len(self.trajCells)-1])
        self.trajCells = newTrajCells
        if(interpWanted):
            finTrajCells = []
            for i in range(len(self.trajCells)-1):
                current = self.trajCells[i]
                nextc = self.trajCells[i+1]
                if(current == nextc or g.areAdjacent(current,nextc)):
                    finTrajCells.append(current)
                else:
                    finTrajCells.extend(g.giveInterpolatedRoute(current,nextc))
            finTrajCells.append(self.trajCells[len(self.trajCells)-1])
            self.trajCells = finTrajCells

    @__init__.overload
    def __init__(self, startcell:Cell, endcell:Cell):
        self.trajCells = []
        self.trajCells.append(startcell)
        self.trajCells.append(endcell)
    
    @__init__.overload
    def __init__(self, cellerino:list):
        self.trajCells = cellerino

    def addCell(self, c1:Cell):
        self.trajCells.append(c1)

    def toString(self):
        tbr = ""
        for c in self.trajCells:
            tbr = tbr + "->" + c.toString()
        return tbr

    def getCells(self) -> List[Cell]:
        return self.trajCells

    def getLength(self):
        return len(self.trajCells)

    def getTrajName(self):
        return self.trajCells[0].getName()+"->"+self.trajCells[-1].getName()

    def passesThrough(self, c:Cell):
        for i in self.trajCells:
            if (c == i):
                return True
        return False


if __name__ == "__main__":
    pass

