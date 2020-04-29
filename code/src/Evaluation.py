import math
from Trajectory import Trajectory
from GridTrajectory import GridTrajectory
from typing import List
from Query import Query
import Util
import Convertor

class Evaluation(object):
    def __init__(self,ptime,oDB,sDB):
        self.eva = []
        self.eva.append(round(ptime,2))
        self.eva.append(round(DiameterError(oDB,sDB,40),6))
        self.eva.append(round(DistanceError(oDB,sDB,40),6))
        self.eva.append(round(QueryError(oDB,sDB),6))
        
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
        l = i*bucketSize
        r = (i+1)*bucketSize
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
        l = i*bucketSize
        r = (i+1)*bucketSize
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

def QueryError(origin:List[Trajectory], syn:List[Trajectory], querySanity:float=0.01,num:int=200):
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

