from typing import List
from Trajectory import Trajectory
from Grid import Grid
import Util
import Convertor

def SynTraj(originalDB:List[Trajectory], totalEpsilon:float) -> List[Trajectory]:
    interp = True
    cellCount = 6
    budgetDistnWeights = [0.05,0.35,0.50,0.10]
    boundaries = Util.getDataBoundaries(originalDB)
    minX = boundaries[0]
    maxX = boundaries[1]
    minY = boundaries[2]
    maxY = boundaries[3]
    grid = Grid(cellCount, minX,maxX,minY,maxY)
    dbGrid = Convertor.convertTrajToGridTraj(originalDB, grid, interp,budgetDistnWeights[0]*totalEpsilon, (1.0-budgetDistnWeights[0])*totalEpsilon)
    markovTransitionProbs = Util.extractMarkovProbs(originalDB,grid,budgetDistnWeights[1]*totalEpsilon)
    

if __name__ == "__main__":
    pass