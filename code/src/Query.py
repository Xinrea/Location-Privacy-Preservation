import random
import math
from Trajectory import Trajectory
from typing import List

class Query(object):
    def __init__(self,minX,maxX,minY,maxY):
        r = random.Random()
        self.centerX = r.random()*(maxX-minX)+minX
        self.centerY = r.random()*(maxY-minY)+minY
        diff = 0
        if (maxX-minX > maxY-minY):
            diff = maxX-minX
        else:
            diff = maxY-minY
        self.radius = diff/10
    
    def evaluateQueryOnTraj(self,t:Trajectory):
        for i in range(t.getSize()-1):
            p1x = t.getPoint(i).getX()
            p2x = t.getPoint(i+1).getX()
            p1y = t.getPoint(i).getY()
            p2y = t.getPoint(i+1).getY()
            if (self.eucDistance(p1x,p1y,self.centerX,self.centerY) <= self.radius):
                return True
            if (self.eucDistance(p2x,p2y,self.centerX,self.centerY) <= self.radius):
                return True
            if (p1x == p2x and p1y == p2y):
                return True
            elif (self.distanceToSegment(self.centerX,self.centerY,p1x,p1y,p2x,p2y) <= self.radius):
                return True
        return False

    def evaluateQueryOnDatabase(self,dataset:List[Trajectory]):
        tbr = 0
        for  t in dataset:
            if (self.evaluateQueryOnTraj(t) == True):
                tbr += 1
        return tbr
        

    def eucDistance(self,p1x,p1y,p2x,p2y):
        return math.sqrt((p2x-p1x)*(p2x-p1x) + (p2y-p1y)*(p2y-p1y))

    def distanceToSegment(self,x3,y3,x1,y1,x2,y2):
        px = 0
        py = 0
        dx = x2-x1
        dy = y2-y1
        if (dx == 0 and dy == 0):
            print("Query:Same Point")
            return 0
        u = ((x3-x1)*dx+(y3-y1)*dy)/(dx*dx+dy*dy)
        if (u < 0):
            px = x1
            py = y1
        elif (u > 1):
            px = x2
            py = y2
        else:
            px = x1+u*dx
            py = y1+u*dy
        return self.eucDistance(px,py,x3,y3)
