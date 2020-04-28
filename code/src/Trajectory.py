import overload_function
from Point import Point
from Cell import Cell

class Trajectory(object):
    def __init__(self,xs=None,ys=None):
        if (xs == None):
            self.points = []
            return
        if (len(xs) != len(ys)):
            print("Cound't Create: check sizeof xs and ys")
            return
        self.points = []
        for i in range(len(xs)):
            p = Point(xs[i],ys[i])
            self.points.append(p)
    
    def addCoordinates(self,xc,yc,time):
        p = Point(time,xc,yc)
        self.points.append(p)

    def addPoint(self,p):
        self.points.append(p)

    def getSize(self):
        return len(self.points)

    def getPointString(self,pos):
        return self.points[pos].toString()

    def getPoint(self,pos):
        return self.points[pos]

    def getPoints(self):
        return self.points

    def getMinXCoord(self):
        currMin = self.points[0].getX()
        for p in self.points:
            if(p.getX() < currMin):
                currMin = p.getX()
        return currMin

    def getMinYCoord(self):
        currMin = self.points[0].getY()
        for p in self.points:
            if(p.getY() < currMin):
                currMin = p.getY()
        return currMin

    def getMaxXCoord(self):
        currMin = self.points[0].getX()
        for p in self.points:
            if(p.getX() > currMin):
                currMin = p.getX()
        return currMin

    def getMaxYCoord(self):
        currMin = self.points[0].getY()
        for p in self.points:
            if(p.getY() > currMin):
                currMin = p.getY()
        return currMin

    def getDiameter(self):
        maxDist = 0
        for i in range(self.getSize()):
            for j in range(self.getSize()):
                p1 = self.points[i]
                p2 = self.points[j]
                dist = p1.euclideanDistTo(p2)
                if(dist > maxDist):
                    maxDist = dist
        return maxDist

    def getDistanceTravelled(self):
        tbr = 0
        for i in range(len(self.points)-1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            tbr += p1.euclideanDistTo(p2)
        return tbr

    def getSniffedPoints(self,sniffZone):
        tbr = []
        pos = 0
        while(pos < self.getSize()):
            if(sniffZone.inCell(self.points[pos])):
                sniffpos = pos
                while(sniffpos < self.getSize() and sniffZone.inCell(self.points[sniffpos])):
                    tbr.append(self.points[sniffpos])
                    sniffpos += 1
                return tbr
            pos += 1
        return tbr

    def calcIntersectionWith(self, t2):
        intersected = []
        for p in t2.points:
            for i in range(len(self.points)):
                cand = self.points[i]
                if(p.euclideanDistTo(cand)<0.01):
                    intersected.append(p)
                    break
        return intersected

    def calcIntersectionCount(self, t2):
        return len(self.calcIntersectionWith(t2))

    def calculateDTWto(self, t2):
        #TODO Evaluation Here
        return 0
