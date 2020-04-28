import scipy.stats as st
import numpy as np
import Util
import random
import sys
from typing import List
from GridTrajectory import GridTrajectory
from Grid import Grid

class LengthDistribution(object):
    def __init__(self,inputDB:List[GridTrajectory],grid:Grid,eps:float):
        self.lengthCount = {}
        self.minL = sys.maxsize
        self.maxL = -sys.maxsize
        count = 0
        for t in inputDB:
            name = t.getTrajName()
            if(t.getLength() > self.maxL):
                self.maxL = t.getLength()
            if(t.getLength() < self.minL):
                self.minL = t.getLength()

            if (name not in self.lengthCount):
                self.lengthCount[name] = [t.getLength()]
            else:
                self.lengthCount[name].append(t.getLength())
            
            count += 1
        if (self.maxL > 100):
            self.maxL = 100
        # print("[LengthDistribution]Get Sample Number",count)

    def addBias(self,other):
        self.minL = self.minL if self.minL < other.minL else other.minL
        self.maxL = self.maxL if self.maxL > other.maxL else other.maxL
        lc = other.lengthCount
        for n,d in lc.items():
            if (n in self.lengthCount):
                self.lengthCount[n].extend(d)
            else:
                self.lengthCount[n] = d

    def sample(self, start, end):
        name = start.getName()+"->"+end.getName()
        if(name not in self.lengthCount):
            return random.randint(self.minL,self.maxL+1)
        return self.lengthCount[name][random.randint(0,len(self.lengthCount[name])-1)]


# class LengthDistribution(object):
#     def __init__(self,inputDB:List[GridTrajectory],grid:Grid,eps:float):
#         print("[LengthDistribution] Init")
#         cells = grid.getCells()
#         trajs = []
#         for t in inputDB:
#             trajs.append(t)
#         self.distributionTypeMap = {}
#         self.maxExtraLengthAllowed = {}
#         print("[LengthDistribution] Cells Num:",len(cells))
#         for i in range(len(cells)):
#             for j in range(len(cells)):
#                 startCell = cells[i]
#                 endCell = cells[j]
#                 print("[LengthDistribution] ",startCell.getName(),endCell.getName())
#                 currentTrip = startCell.getName()+"->"+endCell.getName()
#                 subsetTrajs = []
#                 subsetTrajCounts = []
#                 minCellCount = grid.findShortestLengthBetween(startCell,endCell)
#                 for t in trajs:
#                     cellsOfTraj = t.getCells()
#                     if(cellsOfTraj[0].getName() == startCell.getName() and cellsOfTraj[len(cellsOfTraj)-1].getName() == endCell.getName()):
#                         subsetTrajs.append(t)
#                         subsetTrajCounts.append(len(cellsOfTraj)-minCellCount)
#                         # iter.remove()
#                 MAX = 0
#                 SUM = 0
#                 COUNT = len(subsetTrajCounts)
#                 for i in subsetTrajCounts:
#                     SUM += i
#                     if (i > MAX):
#                         MAX = i
#                 if(len(subsetTrajCounts) == 0 or MAX == 0):
#                     self.distributionTypeMap[currentTrip] = st.uniform(loc=0,scale=0)
#                     self.maxExtraLengthAllowed[currentTrip] = 0
#                     continue
#                 ld = st.laplace(loc=0,scale=MAX/eps)
#                 noisySum = SUM + ld.rvs()
