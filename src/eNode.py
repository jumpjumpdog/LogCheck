#-*- encoding=utf8 -*-


class eNode:
    name = ""
    id = ""
    cellToBBp = {}
    def __init__(self, name,id):
        self.name = name
        self.id  = id
        self.cellToBBp = {}

    class BBP:
        portOne=""
        portTwo=""
        poerThree=""

        def __init__(self, portOne, portTwo, portThree):
            self.portOne = portOne
            self.portTwo = portTwo
            self.portThree = portThree

        def getPortOne(self):
            return self.portOne

        def getPortTwo(self):
            return self.portTwo

        def getPortThree(self):
            return self.portThree

    def getName(self):
        return self.name

    def getId(self):
        return self.id

    def setName(self,name):
        self.name = name

    def setId(self, id):
        return  self.id

    def addCellBpp(self, localCellId, bbp):
        if localCellId in self.cellToBBp.keys():
            return None
        else:
            self.cellToBBp[localCellId] = bbp

