#-*- encoding=utf8 -*-
from  eNode import  eNode
import re

# store file context to a string
context = ""
site_dict = {}
enode_dict= {}
with open("MY_DSP_CELLPHYTOPO.txt","rb") as f:
    context = f.read()

def getAllSites():
    pattern = "(DSP CELLPHYTOPO:;\s+(\S+)\s*([\s\S]*?)Display Physical Topology of Cells([\s\S]*?)END)"
    pattern = re.compile(pattern)

    results = pattern.findall(context)

    for site in results:
        siteName = site[1]
        topology = site[3]
        site_dict[siteName] = topology



def getDspInfo():
    # name = "GL82100"
    # content = site_dict[name]
    # site_dict.clear()
    # site_dict[name]  = content
    for siteName in site_dict.keys():
        topology = site_dict[siteName]
        pattern = "((\d+)\s+(\d+)\s+\d+-\d+-\d+\s+(\d+-\d+-\d+-\d+\,{0,1})+\s+(\d+)-(\d+)-(\d+)\s+(\S+))"
        pattern = re.compile(pattern)
        newENode = None

        results = pattern.findall(topology)
        if results:
            eNodeId = results[0][1]
            newENode = eNode(siteName, eNodeId)
            for index, item in enumerate(results):
                local_cell_id = results[index][2]
                portOne = results[index][4]
                portTwo = results[index][5]
                portThree = results[index][6]
                type = results[index][7]
                bbp = eNode.BBP(portOne,portTwo,portThree, type)
                newENode.addCellBbp(localCellId= local_cell_id,bbp=bbp)

        enode_dict[siteName] = newENode



    # a = enode_dict["GL82100"]
    # print a
