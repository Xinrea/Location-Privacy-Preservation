class Pattern(object):
    def __init__(self,cells):
        self.cellsInPattern = cells

    def __eq__(self,item):
        if isinstance(item,self.__class__):
            return self.isEqual(item)
        return False

    def __hash__(self):
        pname = ""
        for c in self.cellsInPattern:
            pname += c.getName()
        return hash(pname)

    def isEqual(self,other):
        if (len(self.cellsInPattern) != len(other.cellsInPattern)):
            return False
        for i in range(len(self.cellsInPattern)):
            if (self.cellsInPattern[i].toString() != other.cellsInPattern[i].toString()):
                return False
        return True

