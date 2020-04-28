class Pattern(object):
    def __init__(self,cells):
        self.cellsInPattern = cells

    def __eq__(self,item):
        if isinstance(item,self.__class__):
            return self.isEqual(item)
        return False

    def __hash__(self):
        return hash(self.cellsInPattern)

    def isEqual(self,other):
        if (len(self.cellsInPattern) != len(other.cellsInPattern)):
            return False
        for i in range(len(self.cellsInPattern)):
            if (self.cellsInPattern[i].toString() != other.cellsInPattern[i].toString()):
                return False
        return True

