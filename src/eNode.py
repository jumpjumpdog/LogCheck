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
        type = ""
        portOne=""
        portTwo=""
        poerThree=""

        def __init__(self, portOne, portTwo, portThree,type):
            self.portOne = portOne
            self.portTwo = portTwo
            self.portThree = portThree
            self.type = type

        def getPortOne(self):
            return self.portOne

        def getPortTwo(self):
            return self.portTwo

        def getPortThree(self):
            return self.portThree

        def getType(self):
            return  self.type

    def getName(self):
        return self.name

    def getId(self):
        return self.id


    def getCellBbp(self):
        return  self.cellToBBp

    def setName(self,name):
        self.name = name

    def setId(self, id):
        self.id = id

    def setType(self,type):
        self.setType(type)

    def addCellBbp(self, localCellId, bbp):
        if localCellId in self.cellToBBp.keys():
            temp = self.cellToBBp[localCellId]
            temp.append(bbp)
        else:
            self.cellToBBp[localCellId] = []
            self.cellToBBp[localCellId].append(bbp)


