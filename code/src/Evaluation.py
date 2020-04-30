import math
from Trajectory import Trajectory
from GridTrajectory import GridTrajectory
from typing import List
from Query import Query
from Grid import Grid
import Util
import Convertor
import time
from Pattern import Pattern

class Evaluation(object):
    def __init__(self,ptime,oDB,sDB):
        self.eva = []
        self.eva.append(ptime)
        self.eva.append(DiameterError(oDB,sDB,40))
        self.eva.append(DistanceError(oDB,sDB,40))
        self.eva.append(QueryError(oDB,sDB))
        self.eva.append(locationKendallTau(oDB,sDB))
        self.eva.append(TimeError(oDB,sDB))
        self.eva.append(PFError(oDB,sDB))
        self.eva.append(FPError(oDB,sDB))
        
    def toList(self):
        return self.eva


def calcJSD(origProb, synProb):
    avgProb = []
    for i in range(len(origProb)):
        avgProb.append((origProb[i]+synProb[i])/2)
    return 0.5*calcKL(origProb,avgProb) + 0.5*calcKL(synProb,avgProb)

def calcKL(p1,p2):
    KL = 0
    for i in range(len(p1)):
        q = p2[i]
        p = p1[i]
        if (p != 0):
            KL += math.log(p/q)*p
    return KL

def DiameterError(origin:List[Trajectory], syn:List[Trajectory], bucketNum:int):
    minf = float('inf')
    maxf = float('-inf')
    originalDiameters = []
    for t in origin:
        dia = t.getDiameter()
        originalDiameters.append(dia)
        if (dia < minf):
            minf = dia
        if (dia > maxf):
            maxf = dia
    syntheticDiameters = []
    for t in syn:
        syntheticDiameters.append(t.getDiameter())
    bucketSize = (maxf-minf)/bucketNum
    originDiaCount = []
    synDiaCount = []
    for i in range(bucketNum):
        l = i*bucketSize+minf
        r = (i+1)*bucketSize+minf
        cnt = 0
        for d in originalDiameters:
            if (d >= l and d <= r):
                cnt += 1
        originDiaCount.append(cnt)
        cnt = 0
        for d in syntheticDiameters:
            if (d >= l and d <= r):
                cnt += 1
        synDiaCount.append(cnt)
    originDiaProbs = []
    synDiaProbs = []
    for i in range(bucketNum):
        originDiaProbs.append(originDiaCount[i]/len(originalDiameters))
        synDiaProbs.append(synDiaCount[i]/len(syntheticDiameters))
    return calcJSD(originDiaProbs, synDiaProbs)

def DistanceError(origin:List[Trajectory], syn:List[Trajectory], bucketNum:int):
    minf = float('inf')
    maxf = float('-inf')
    originalDistance = []
    for t in origin:
        dia = t.getDistanceTravelled()
        originalDistance.append(dia)
        if (dia < minf):
            minf = dia
        if (dia > maxf):
            maxf = dia
    syntheticDistance = []
    for t in syn:
        syntheticDistance.append(t.getDistanceTravelled())
    bucketSize = (maxf-minf)/bucketNum
    originDiaCount = []
    synDiaCount = []
    for i in range(bucketNum):
        l = i*bucketSize+minf
        r = (i+1)*bucketSize+minf
        cnt = 0
        for d in originalDistance:
            if (d >= l and d <= r):
                cnt += 1
        originDiaCount.append(cnt)
        cnt = 0
        for d in syntheticDistance:
            if (d >= l and d <= r):
                cnt += 1
        synDiaCount.append(cnt)
    originDiaProbs = []
    synDiaProbs = []
    for i in range(bucketNum):
        originDiaProbs.append(originDiaCount[i]/len(originalDistance))
        synDiaProbs.append(synDiaCount[i]/len(syntheticDistance))
    return calcJSD(originDiaProbs, synDiaProbs)

def TimeError(origin:List[Trajectory], syn:List[Trajectory], bucketNum:int=24):
    minf = float('inf')
    maxf = float('-inf')
    originalTime = []
    for t in origin:
        points = t.getPoints()
        for p in points:
            ptime = time.mktime(p.getTime())
            originalTime.append(ptime)
            if (ptime < minf):
                minf = ptime
            if (ptime > maxf):
                maxf = ptime
    syntheticTime = []
    for t in syn:
        points = t.getPoints()
        for p in points:
            ptime = time.mktime(p.getTime())
            syntheticTime.append(ptime)
    bucketSize = (maxf-minf)/bucketNum
    originCount = []
    synCount = []
    for i in range(bucketNum):
        l = i*bucketSize+minf
        r = (i+1)*bucketSize+minf
        cnt = 0
        for d in originalTime:
            if (d >= l and d <= r):
                cnt += 1
        originCount.append(cnt)
        cnt = 0
        for d in syntheticTime:
            if (d >= l and d <= r):
                cnt += 1
        synCount.append(cnt)
    originProbs = []
    synProbs = []
    for i in range(bucketNum):
        originProbs.append(originCount[i]/len(originalTime))
        synProbs.append(synCount[i]/len(syntheticTime))
    return calcJSD(originProbs, synProbs)

def PFError(origin:List[Trajectory], syn:List[Trajectory]):
    boundaries = Util.getDataBoundaries(origin)
    minX = boundaries[0]
    maxX = boundaries[1]
    minY = boundaries[2]
    maxY = boundaries[3]
    ug = Grid(15,minX,maxX,minY,maxY)
    originDBgrid = Convertor.convertTrajToGridTraj(origin,ug,True)
    synDBgrid = Convertor.convertTrajToGridTraj(syn,ug,True)
    cells = ug.getCells()
    originCount = []
    synCount = []
    originNum = 0
    synNum = 0
    for i in range(len(cells)):
        cnt = 0
        for t in originDBgrid:
            if (t.passesThrough(cells[i])):
                cnt += 1
        originCount.append(cnt)
        originNum += cnt
        cnt = 0
        for t in synDBgrid:
            if (t.passesThrough(cells[i])):
                cnt += 1
        synCount.append(cnt)
        synNum += cnt
    originProbs = []
    synProbs = []
    for i in range(len(cells)):
        originProbs.append(originCount[i]/originNum)
        synProbs.append(synCount[i]/synNum)
    return calcJSD(originProbs, synProbs)

def FPError(origin:List[Trajectory], syn:List[Trajectory]):
    boundaries = Util.getDataBoundaries(origin)
    minX = boundaries[0]
    maxX = boundaries[1]
    minY = boundaries[2]
    maxY = boundaries[3]
    ug = Grid(15,minX,maxX,minY,maxY)
    originDBgrid = Convertor.convertTrajToGridTraj(origin,ug,True)
    synDBgrid = Convertor.convertTrajToGridTraj(syn,ug,True)
    originPattern = minePatterns(originDBgrid)
    synPattern = minePatterns(synDBgrid)
    oCount = []
    sCount = []
    oNum = 0
    sNum = 0
    for p,n in originPattern.items():
        if (p in synPattern):
            oCount.append(n)
            oNum += n
            sCount.append(synPattern[p])
            sNum += synPattern[p]
    originProbs = []
    synProbs = []
    for i in range(len(oCount)):
        originProbs.append(oCount[i]/oNum)
        synProbs.append(sCount[i]/sNum)
    return calcJSD(originProbs, synProbs)



def minePatterns(db,minSize=2,maxSize=8):
    tbr = {}
    for i in range(minSize,maxSize+1):
        for t in db:
            for k in range(len(t.getCells())-i+1):
                p = Pattern(t.getCells()[k:k+i])
                if (p in tbr):
                    tbr[p] = tbr[p]+1
                else:
                    tbr[p] = 1
    return tbr


def QueryError(origin:List[Trajectory], syn:List[Trajectory], querySanity:float=0.01,num:int=100):
    queries = GenerateQueries(origin,num)
    actualAnswers = [0]*len(queries)
    syntheticAnswers = [0]*len(queries)
    for i in range(len(queries)):
        q = queries[i]
        actualAnswers[i] = q.evaluateQueryOnDatabase(origin)
        syntheticAnswers[i] = q.evaluateQueryOnDatabase(syn)
    error = [0]*len(queries)
    for i in range(len(queries)):
        numerator = abs(syntheticAnswers[i]-actualAnswers[i])
        denominator = actualAnswers[i]
        if (len(origin)*querySanity > denominator):
            denominator = len(origin)*querySanity
        error[i] = numerator/denominator
    sumErr = 0
    for e in error:
        sumErr += e
    return sumErr/(len(error))

def GenerateQueries(db:List[Trajectory],count:int):
    boundaries = Util.getDataBoundaries(db)
    minX = boundaries[0]
    maxX = boundaries[1]
    minY = boundaries[2]
    maxY = boundaries[3]
    tbr = []
    for i in range(count):
        tbr.append(Query(minX,maxX,minY,maxY))
    return tbr

def locationKendallTau(origin:List[Trajectory],syn:List[Trajectory],gridCell:int=15):
    boundaries = Util.getDataBoundaries(origin)
    minX = boundaries[0]
    maxX = boundaries[1]
    minY = boundaries[2]
    maxY = boundaries[3]
    ug = Grid(gridCell,minX,maxX,minY,maxY)
    originDBgrid = Convertor.convertTrajToGridTraj(origin,ug,True)
    synDBgrid = Convertor.convertTrajToGridTraj(syn,ug,True)
    cells = ug.getCells()
    actualCounts = [0]*len(cells)
    synCounts = [0]*len(cells)
    for i in range(len(cells)):
        c = cells[i]
        for t in originDBgrid:
            if (t.passesThrough(c)):
                actualCounts[i] += 1
        for t in synDBgrid:
            if (t.passesThrough(c)):
                synCounts[i] += 1
    concordantPairs = 0
    reversedPairs = 0
    for i in range(len(actualCounts)):
        for j in range(i+1,len(actualCounts)):
            if (actualCounts[i] > actualCounts[j]):
                if (synCounts[i] > synCounts[j]):
                    concordantPairs += 1
                else:
                    reversedPairs += 1
            if (actualCounts[i] < actualCounts[j]):
                if (synCounts[i] < synCounts[j]):
                    concordantPairs += 1
                else:
                    reversedPairs += 1
    denom = concordantPairs+reversedPairs
    return (concordantPairs-reversedPairs)/denom