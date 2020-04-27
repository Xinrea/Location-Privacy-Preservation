import scipy.stats as st
import numpy as np
import Util
import random
import sys
from typing import List
from GridTrajectory import GridTrajectory
from Cell import Cell

class StartEndDistribution(object):
    def __init__(self,inputDB:List[GridTrajectory]):
        self.startCount = []
        self.endCount = []
        count = 0
        for t in inputDB:
            cells = t.getCells()
            self.startCount.append(cells[0].toString())
            self.endCount.append(cells[-1].toString())
            count += 1 
        print("[StartEndDistribution]Get Sample Number",count)

    def sample(self):
        start = self.startCount[random.randint(0,len(self.startCount)-1)]
        end = self.endCount[random.randint(0,len(self.endCount)-1)]
        return [start,end]