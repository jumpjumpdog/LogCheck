#-*- encoding=utf8 -*-
import sys
from findDangerSite import *
from getEnodeInfo import *


def processTXT():
    getAllSites()
    getDspInfo()
    for node_name in enode_dict.keys():
        enode = enode_dict[node_name]
        site = g_site_dict[node_name]
        cellToBBp = enode.getCellBbp()
        for cell_id in cellToBBp.keys():
            bbp = cellToBBp[cell_id]
            bbp = filter(lambda x : x.getType()=="PRIMARY", bbp)
            if len(bbp) == 0:
                pass
            cell = site.search(cell_id)
            if cell.getEqmId() != "":
                pass



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
    processTXT()
    # processXML()



