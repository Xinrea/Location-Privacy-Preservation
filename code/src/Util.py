from typing import List
from Trajectory import Trajectory
from GridTrajectory import GridTrajectory
from Grid import Grid
from Cell import Cell
import random
import numpy as np
import hashlib
import time

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
    for gt in origDBgrid:
        trajCells = gt.getCells()
        for i in range(len(trajCells)-1):
            thisCell = trajCells[i]
            nextCell = trajCells[i+1]
            thisCellIndex = cells.index(thisCell)
            nextCellIndex = cells.index(nextCell)
            actualCounts[thisCellIndex][nextCellIndex] = actualCounts[thisCellIndex][nextCellIndex]+1/(len(trajCells)-1)
    
    return actualCounts

def printGridTraj(gdTraj):
    for i in gdTraj:
        print("["+i.getName()+"]->",end="")
    print("")

def findWithMarkov(prevCell:Cell, eventualCell:Cell, step1matrix, stepNmatrix, g:Grid):
    candidateCells = g.getAdjacentCells(prevCell)
    candidateProbs = []*len(candidateCells)
    for i in range(len(candidateProbs)):
        thisCandidate = candidateCells[i]
        row = g.getPosInListForm(prevCell)
        col = g.getPosInListForm(thisCandidate)
        prob1 = step1matrix[row][col]
        row = g.getPosInListForm(thisCandidate)
        col = g.getPosInListForm(eventualCell)
        prob2 = stepNmatrix[row][col]
        candProb = prob1*prob2
        candidateProbs[i] = candProb
    sump = 0
    for i in range(len(candidateProbs)):
        sump += candidateProbs[i]
    if (sump < 0.00001):
        directRoute = g.giveInterpolatedRoute(prevCell,eventualCell)
        if (len(directRoute) > 1):
            return directRoute[1]
        else:
            return eventualCell
    normalizedProb = []
    for p in candidateProbs:
        normalizedProb.append(p/sump)
    randomVal = random.random()
    seenSoFar = 0
    for i in range(len(candidateProbs)):
        seenSoFar += normalizedProb[i]
        if (seenSoFar >= randomVal):
            return candidateCells[i]
    # Should have returned before here
    directRoute = g.giveInterpolatedRoute(prevCell,eventualCell)
    if (len(directRoute) > 1):
        return directRoute[1]
    else:
        return eventualCell

def precomputeMarkov(oneStep,maxSteps):
    tbr = [oneStep,oneStep]
    for i in range(2,maxSteps+1):
        prevStep = tbr[i-1]
        currStep = matrixMultiply(prevStep,oneStep)
        tbr.append(currStep)
    return tbr

def matrixMultiply(a,b):
    am = np.mat(a)
    bm = np.mat(b)
    c = am*bm
    return c.tolist()
    # c = [[0]*len(b[0]) for _ in range(len(a))]
    # for i in range(len(a)):
    #     for j in range(len(b[0])):
    #         for k in range(len(a[0])):
    #             c[i][j] += a[i][k]*b[k][j]
    # return c

def md5Time():
    m = hashlib.md5()
    m.update(str(time.time()).encode())
    return m.hexdigest()

def md5Str(s):
    m = hashlib.md5()
    m.update(s.encode())
    return m.hexdigest()

if __name__ == "__main__":
    import Convertor
    from GowallaData import GowallaData
    Gowalla = GowallaData()
    Gowalla.read_checkin_file('/home/Gowalla_sample.txt')
    originDB = Convertor.convertGowallaToTraj(Gowalla)
    print(getDataBoundaries(originDB[0]))