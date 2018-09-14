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
        element = ["","",""]

        def __init__(self, portOne, portTwo, portThree,type):
            self.element[0] = portOne
            self.element[1] = portTwo
            self.element[2] = portThree
            self.type = type

        def getPortOne(self):
            return self.element[0]

        def getPortTwo(self):
            return self.element[1]

        def getPortThree(self):
            return self.element[2]

        def getType(self):
            return  self.type

        def getElement(self):
            return self.element

    def getName(self):
        return self.name

    def getId(self):
        return self.id


    def getCellBbp(self):
        return  self.cellToBBp


    def getBbpByCellID(self, cellId):
        return None if cellId not in self.cellToBBp.keys() else self.cellToBBp[cellId]

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


    def getBBpByCellId(self, id):
        return None if id not in self.cellToBBp.keys() else self.cellToBBp[id]


