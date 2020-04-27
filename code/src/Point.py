class Point(object):
    def __init__(self,xc,yc):
        self.xCoord = xc
        self.yCoord = yc
    
    def getX(self):
        return self.xCoord

    def getY(self):
        return self.yCoord

    def isEqualTo(self,p2):
        if(self.xCoord != p2.getX()):
            return False
        if(self.yCoord != p2.getY()):
            return False
        return True
    
    def setX(self,xc):
        self.xCoord = xc

    def setY(self,yc):
        self.yCoord = yc

    def euclideanDistTo(self,p2):
        sum = (self.getY()-p2.getY())*(self.getY()-p2.getY()) + (self.getX()-p2.getX())*(self.getX()-p2.getX())
        return math.sqrt(sum)
    