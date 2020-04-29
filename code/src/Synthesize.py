from typing import List
from Trajectory import Trajectory
from Grid import Grid
from GridTrajectory import GridTrajectory
from LengthDistribution import LengthDistribution
from TimeDistribution import TimeDistribution
from StartEndDistribution import StartEndDistribution
from GowallaData import GowallaData
import Util
import Convertor

def SynTraj(originalDB:List[Trajectory], totalEpsilon:float, options:List,blockDistribution) -> List[Trajectory]:
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
    markovTransitionProbs = Util.extractMarkovProbs(dbGrid,grid,budgetDistnWeights[1]*totalEpsilon)
    lengthDistribution = LengthDistribution(dbGrid,grid,budgetDistnWeights[2]*totalEpsilon)
    if (options[0] == 0):
        lengthDistribution.addBias(blockDistribution[0])
    startendDistribution = StartEndDistribution(dbGrid)
    if (options[1] == 0):
        startendDistribution.addBias(blockDistribution[1])
    timeDistribution = TimeDistribution(originalDB)
    if (options[2] == 0):
        timeDistribution.addBias(blockDistribution[2])
    synGridDB = DoSynTraj(grid,markovTransitionProbs,timeDistribution,startendDistribution,lengthDistribution,len(originalDB))
    synDB = Convertor.convertGridTrajToTraj(synGridDB,timeDistribution)
    return synDB


def DoSynTraj(g,markovProbs,td:TimeDistribution,sed:StartEndDistribution,ld:LengthDistribution,desired:int):
    tbr = []
    # transitionMatrices = [[0]*len(markovProbs) for _ in range(len(markovProbs))]
    transitionMatrices = Util.precomputeMarkov(markovProbs,100)
    for cnt in range(desired):
        se = sed.sample()
        startCell = g.getCellByName(se[0])
        endCell = g.getCellByName(se[1])
        length = ld.sample(startCell,endCell)
        newTrajCells = [0]*length
        newTrajCells[0] = startCell
        newTrajCells[-1] = endCell
        for i in range(1,length-1):
            prevCell = newTrajCells[i-1]
            eventualCell = newTrajCells[-1]
            stepToEventual = length-i-1
            step1matrix = transitionMatrices[1]
            stepNmatrix = transitionMatrices[stepToEventual]
            newTrajCells[i] = Util.findWithMarkov(prevCell,eventualCell,step1matrix,stepNmatrix,g)
        sTraj = GridTrajectory(newTrajCells)
        tbr.append(sTraj)
    return tbr


if __name__ == "__main__":
    Gowalla = GowallaData()
    Gowalla.read_checkin_file('/home/Gowalla_sample.txt')
    originDB = Convertor.convertGowallaToTraj(Gowalla)
    print(Gowalla.getUidlist())
    SynTraj(originDB[0],1)
