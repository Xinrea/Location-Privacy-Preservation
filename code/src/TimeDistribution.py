import scipy.stats as st
import numpy as np
import random
import sys
from typing import List
from Trajectory import Trajectory
from Point import Point

class TimeDistribution(object):
    def __init__(self,inputDB:List[Trajectory]):
        self.timeCount = {}
        count = 0
        for t in inputDB:
            size = t.getSize()
            for i in range(size):
                p = t.getPoint(i)
                if (i not in self.timeCount):
                    self.timeCount[i] = [p.getTime()]
                else:
                    self.timeCount[i].append(p.getTime())
                count += 1
        # print("[TimeDistribution]Get Sample Number",count)

    def addBias(self,other):
        tc = other.timeCount
        for s,t in tc.items():
            self.timeCount[s] = t

    def sample(self, step:int):
        if (step not in self.timeCount):
            for s,t in self.timeCount.items():
                return t[random.randint(0,len(t)-1)]
        return self.timeCount[step][random.randint(0,len(self.timeCount[step])-1)]