#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import math

from Point import Point

class Cell(object):
    def __init__(self,minx,miny,xIncrement,yIncrement,nm):
        self.minX = minx
        self.minY = miny
        self.maxX = minx + xIncrement
        self.maxY = miny + yIncrement
        self.name = nm
        self.leve2cells = []
        self.leve2densities = []

    def inCell(self,xCoord, yCoord = None):
        x = xCoord
        y = yCoord
        if(yCoord == None):
            x = xCoord.getX()
            y = xCoord.getY()
        
        if (x >= self.minX and x <= self.maxX and y >= self.minY and y <= self.maxY):
            return True
        else:
            return False
    
    def toString(self):
        return self.name
    
    def getName(self):
        return self.name

    def sampleRandomPoint(self,time):
        if (len(self.leve2cells) == 0 or len(self.leve2cells) == 1):
            xcoord = self.minX + random.uniform(0,1)*(self.maxX-self.minX)
            ycoord = self.minY + random.uniform(0,1)*(self.maxY-self.minY)
            return Point(time,xcoord,ycoord)
        else:
            rand = random.uniform(0,1)
            seenSoFar = 0.0
            for i in range(len(self.leve2densities)):
                seenSoFar = seenSoFar + self.leve2densities[i]
                if (seenSoFar >= rand):
                    myAdaptiveCell = self.leve2cells[i]
                    xcoord = self.minX + random.uniform(0,1)*(self.maxX-self.minX)
                    ycoord = self.minY + random.uniform(0,1)*(self.maxY-self.minY)
                    return Point(time,xcoord,ycoord)
            xcoord = self.minX + random.uniform(0,1)*(self.maxX-self.minX)
            ycoord = self.minY + random.uniform(0,1)*(self.maxY-self.minY)
            return Point(time,xcoord,ycoord)

    def divideFurther(self,noisydensity, EpsLeft,db):
        lvl2cell = math.ceil(5*noisydensity/(len(db)*EpsLeft))
        if(lvl2cell <= 0):
            lvl2cell = 1
        xIncrement = (self.maxX-self.minX)/lvl2cell
        yIncrement = (self.maxY-self.minY)/lvl2cell
        densities = []
        for i in range(lvl2cell):
            for j in range(lvl2cell):
                lvl2cellSelf = Cell(self.minX+xIncrement*i, self.minY+yIncrement*j,xIncrement,yIncrement,str(i)+","+str(j))
                lvl2cellDensity = 0
                for t in db:
                    for k in range(t.getSize()):
                        if(lvl2cellSelf.inCell(t.getPoint(k))):
                            lvl2cellDensity = lvl2cellDensity + 1
                            break
                self.leve2cells.append(lvl2cellSelf)
                densities.append(lvl2cellDensity)
        totoaldensity = 0
        for d in densities:
            totoaldensity = totoaldensity + d
        for i in range(len(densities)):
            if (totoaldensity != 0):
                self.leve2densities.append(densities[i]/totoaldensity)
            else:
                self.leve2densities.append(0)