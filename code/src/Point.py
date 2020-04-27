import overload_function
import math

class Point(object):
    @overload_function
    def __init__(self,time,xc,yc):
        self.time = time
        self.xCoord = xc
        self.yCoord = yc
    
    def getTime(self):
        return self.time

    def getX(self):
        return self.xCoord

    def getY(self):
        return self.yCoord

    def isEqualTo(self,p2):
        if(self.time != p2.getTime()):
            return False
        if(self.xCoord != p2.getX()):
            return False
        if(self.yCoord != p2.getY()):
            return False
        return True
    
    def setTime(self,time):
        self.time = time

    def setX(self,xc):
        self.xCoord = xc

    def setY(self,yc):
        self.yCoord = yc

    def euclideanDistTo(self,p2):
        sum = (self.getY()-p2.getY())*(self.getY()-p2.getY()) + (self.getX()-p2.getX())*(self.getX()-p2.getX())
        return math.sqrt(sum)
    