#-*- encoding=utf8 -*-
import random
import sys
from findDangerSite import *
from getEnodeInfo import *

#
# # safe node and no bbp id  enters this function
# def getBbpID(site,enode,cell):
#     allBBP = site.getAllBaseBandEqm().items
#     allBBP = site.getAllBaseBandEqm().values()
#     bbp =  enode.getBBpByCellId(cell.getCellId())
#     element = bbp.getElement()



def processTXT():
    getAllSites()
    getDspInfo()
    allRows = []
    for node_name in enode_dict.keys():
        rows = []
        enode = enode_dict[node_name]
        site = g_site_dict[node_name]

        row = {"Site-Name":node_name,"Site-ID":enode_dict[node_name].getId()}
        rows.append(row)
        cellToBBp = enode.getCellBbp()

        availBBpIdSet = set(site.getAvailBBQId())
        allBBP = site.getAllBaseBandEqm()
        elementToBBQId = {}

        for bbqId in allBBP.keys():
            elements = allBBP[bbqId].getElements()
            for element in elements:
                elementToBBQId[element] = bbqId


        for index, cell_id in enumerate(cellToBBp.keys()):
            row = {}
            cell = site.search(cell_id)
            row["Cell-ID"] = cell_id
            if not cell.safe():
                row["Is-Danger"] = "True"
                row["BBP-ID"] = cell.getEqmId()
            else:
                row["Is-Danger"] = "False"
                row["BBP-ID"]  = cell.getEqmId()

                bbq = cellToBBp[cell_id]
                row["Gui"] = bbq[0].getPortOne()
                row["Kuang"] = bbq[0].getPortTwo()
                row["Cao"] = bbq[0].getPortThree()
                if cell.getEqmId() == "":
                    element = enode.getBBpByCellId(cell_id)
                    if element  in elementToBBQId.keys():
                        normalBBqId = elementToBBQId[element]
                        if normalBBqId in availBBpIdSet:
                            row["Normal-BBP-ID"] = normalBBqId
                            availBBpIdSet.remove(normalBBqId)
                        else:
                            portThree = bbq.getPortThree()
                            if str(str(int(portThree) + 10)) in availBBpIdSet:
                                newNormalBBqId = str(str(int(portThree) + 10))
                                availBBpIdSet.remove(newNormalBBqId)
                                cell.setEqmId(newNormalBBqId)
                            else:
                                if len(availBBpIdSet) == 0:
                                    newNormalBBqId = "no available eqmid"
                                else:
                                    newNormalBBqId = random.sample(availBBpIdSet, 1)[0]
                                    cell.setEqmId(newNormalBBqId)
                                    availBBpIdSet.remove(newNormalBBqId)
                            row["Normal-BBP-ID"] = newNormalBBqId
                    else:
                        portThree = bbq[0].getPortThree()
                        if str(str(int(portThree) + 10)) in availBBpIdSet:
                            newNormalBBqId = str(str(int(portThree) + 10))
                            availBBpIdSet.remove(newNormalBBqId)
                            cell.setEqmId(newNormalBBqId)
                        else:
                            if len(availBBpIdSet) == 0:
                                newNormalBBqId = "no available eqmid"
                            else:
                                newNormalBBqId = random.sample(availBBpIdSet, 1)[0]
                                cell.setEqmId(newNormalBBqId)
                                availBBpIdSet.remove(newNormalBBqId)
                        row["Normal-BBP-ID"] = newNormalBBqId
            rows.append(row)
        # rows = sorted(rows,key=lambda d:int(d["cell_id"]))
        allRows.extend(rows)

    return  allRows


def processXML():
    inputPath = sys.argv[1]
    outputPath = sys.argv[2]
    argv_error = False
    if not inputPath or len(inputPath) == 0:
        argv_error = True
        print "输入路径不合法"
    if not outputPath or len(outputPath) == 0:
        argv_error = True
        print "输出路径不合法"
    if argv_error:
        print "请重新输入"
    else:
        findSite(inputPath)

    # 遍历所有的site，将危险的site标记
    findDangerSite()

    # 输出
    outPut(outputPath)


if __name__ == "__main__":
    processXML()
    rows = processTXT()
    with open("bbeq_info.csv", "wb+") as csvfile:
        fieldNames = ["Site-Name","Site-ID","Is-Danger","Cell-ID","BBP-ID","Gui","Kuang","Cao","Normal-BBP-ID","New Normal-BBP-ID","MML CMD"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerows(rows)



