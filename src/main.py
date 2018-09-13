#-*- encoding=utf8 -*-
import random
import sys
from findDangerSite import *
from getEnodeInfo import *


def processTXT():
    getAllSites()
    getDspInfo()
    allRows = []
    for node_name in enode_dict.keys():
        rows = []
        enode = enode_dict[node_name]
        site = g_site_dict[node_name]
        cellToBBp = enode.getCellBbp()
        usedIdSet  = set(site.getAllBaseBandEqm().keys())

        for index, cell_id in enumerate(cellToBBp.keys()):
            row = {}

            row["cell_id"] = cell_id
            bbp = cellToBBp[cell_id]
            bbp = filter(lambda x : x.getType()=="PRIMARY", bbp)
            if len(bbp) == 0:
                continue
            bbp = bbp[0]
            row["port_one"] = bbp.getPortOne()
            row["port_two"] = bbp.getPortTwo()
            row["port_three"] = bbp.getPortThree()
            cell = site.search(cell_id)
            if cell.getEqmId() != "":
                row["bbq_id"] = cell.getEqmId()
            else:
                bbq_id = ""
                portThree = bbp.getPortThree()
                if int(portThree)+10<=23 and str(str(int(portThree)+10)) not in usedIdSet:
                    bbq_id = str(str(int(portThree)+10))
                    usedIdSet.add(bbq_id)
                    cell.setEqmId(bbq_id)
                else:
                    availSet = set([str(x) for x in range(24)])
                    availSet = availSet-usedIdSet
                    if len(availSet) ==0:
                        bbq_id = "no available eqmid"
                    else:
                        bbq_id = random.sample(availSet, 1)[0]
                        cell.setEqmId(bbq_id)
                        usedIdSet.add(bbq_id)
                row["bbq_id"] = bbq_id
            rows.append(row)
        rows = sorted(rows,key=lambda d:int(d["cell_id"]))
        if len(rows) == 0:
            rows.insert(0, {"site_name": node_name, "site_id": enode.getId()})
        else:
            rows[0]["site_name"]=node_name
            rows[0]["site_id"] = enode.getId()
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
        fieldNames = ["site_name", "site_id", "cell_id", "bbq_id", "port_one", "port_two", "port_three"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerows(rows)



