import math
from Trajectory import Trajectory
from typing import List

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

    