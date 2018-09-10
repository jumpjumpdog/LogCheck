#-*- encoding=utf8 -*-


class Cell:
    id = ""
    #绑定的基带设备
    baseBandEqmId = ""

    baseBandEqm = None

    isSafe = True

    reason = None


    def __init__(self, id):
        self.id  = id
        self.isSafe = True
        self.baseBandEqmId = ""
        self.reason = None



    def getCellId(self):
        return self.id

    def getEqmId(self):
        return self.baseBandEqmId


    def isSafe(self):
        return self.isSafe

    def getReason(self):
        return self.reason




    def setId(self, localCellId):
        self.id = localCellId

    def setEqmId(self, eqmId):
        self.baseBandEqmId = eqmId


    def setReason(self, reason):
        self.isSafe = False
        self.reason = reason

    def setEqm(self, basebandEqm):
        self.baseBandEqm = basebandEqm

class BaseBandEqm:
    baseBandEqmId = ""
    baseBandEqmType = ""
    elements = []

    def __init__(self, id):
        self.baseBandEqmId = id
        self.baseBandEqmType = ""
        self.elements = []

    class Element:
        cn = ""
        srn = ""
        sn = ""
        def __init__(self, cn,srn,sn):
            self.cn = cn
            self.srn = srn
            self.sn = sn

    def addElement(self, element):
        self.elements.append(element)

    def getId(self):
        return self.baseBandEqmId

    def getType(self):
        return  self.baseBandEqmType

    def getElementNum(self):
        return len(self.elements)

    def setType(self, type):
        self.baseBandEqmType = type

    def setId(self, id):
        self.baseBandEqmId = id




#
class Site:
    cell_dic = {}

    danger_cells = []

    name = ""
    # 存在的基带设备
    AllBaseBandEqm = {}
    # 是否安全
    isSafe = True

    def __init__(self, name):
        self.name = name
        self.cell_dic = {}
        self.danger_cells = []
        self.isSafe = True

    def search(self, local_cell_id):
        if local_cell_id in self.cell_dic.keys():
            return self.cell_dic.get(local_cell_id)
        return  None

    def getName(self):
        return self.name

    def getCellNum(self):
        return len(self.cell_dic.keys())

    def getAllBaseBandEqm(self):
        return self.AllBaseBandEqm


    def getEqm(self, eqmId):
        return  None if eqmId not in self.AllBaseBandEqm.keys() else self.AllBaseBandEqm[eqmId]

    def getCellDic(self):
        return self.cell_dic

    def getSafeStatus(self):
        return  self.isSafe

    def getDangerCells(self):
        return self.danger_cells

    def addCell(self, local_cell_id):
        cell = self.search(local_cell_id)
        if cell:
            return cell
        self.cell_dic[local_cell_id] = Cell(local_cell_id)
        return self.cell_dic[local_cell_id]


    def addDangerCell(self, cell):
        self.danger_cells.append(cell)

    def setName(self,name):
        self.name = name

    def setSafeStatus(self, isSafe):
        self.isSafe = isSafe



    def addBaseBandEqm(self, newBaseBand):
        baseId = newBaseBand.getId()
        self.AllBaseBandEqm[baseId] = newBaseBand

    def containEqm(self, eqmId):
        return eqmId in self.AllBaseBandEqm.keys()



