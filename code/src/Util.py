import Convertor
from typing import List
from GowallaData import GowallaData
from Trajectory import Trajectory
from GridTrajectory import GridTrajectory
from Grid import Grid
from Cell import Cell

def getDataBoundaries(db:List[Trajectory]):
    dataMinX = float('inf')
    dataMinY = float('inf')
    dataMaxX = float('-inf')
    dataMaxY = float('-inf')
    for t in db:
        if (t.getMinXCoord() < dataMinX):
            dataMinX = t.getMinXCoord()
        if (t.getMaxXCoord() > dataMaxX):
            dataMaxX = t.getMaxXCoord()
        if (t.getMinYCoord() < dataMinY):
            dataMinY = t.getMinYCoord()
        if (t.getMaxYCoord() > dataMaxY):
            dataMaxY = t.getMaxYCoord()
    tbr = []
    tbr.append(dataMinX)
    tbr.append(dataMaxX)
    tbr.append(dataMinY)
    tbr.append(dataMaxY)
    return tbr

def extractMarkovProbs(origDBgrid:List[GridTrajectory],g:Grid,privacyBudget) -> List[List[float]]:
    cells = g.getCells()
    actualCounts = [[0]*len(cells) for _ in range(len(cells))]
    for t in origDBgrid:
        trajCells = t.getCells()
        for i in range(len(trajCells)-1):
            thisCell = trajCells[i]
            nextCell = trajCells[i+1];
            thisCellIndex = cells.index(thisCell)
            nextCellIndex = cells.index(nextCell)
            actualCounts[thisCellIndex][nextCellIndex] = actualCounts[thisCellIndex][nextCellIndex]+1/(len(trajCells)-1)
    # For now, noise is not added
    return actualCounts

if __name__ == "__main__":
    Gowalla = GowallaData()
    Gowalla.read_checkin_file('/home/Gowalla_sample.txt')
    originDB = Convertor.convertGowallaToTraj(Gowalla)
    print(getDataBoundaries(originDB[0]))