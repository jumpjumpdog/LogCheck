#-*- encoding=utf8 -*-
from  eNode import  eNode
import re

# store file context to a string
context = ""
with open("DSP_CELLPHYTOPO.txt","rb") as f:
    context = f.read()



def getDspInfoByName(siteName):
    command = "DSP CELLPHYTOPO:;\r\n"+siteName+"([\s\S]*?)Display Physical Topology of Cells"
    pattern =  "("+command+"([\s\S]*?)END)"
    pattern = re.compile(pattern)
    newENode = None


    try:
        topology = pattern.findall(context)[0][2]
        pattern = "((\d+)\s+\d+-\d+-\d+\s+\d+-\d+-\d+-\d+\s+(\d+)-(\d+)-(\d+)\s+)"
        pattern = re.compile(pattern)
        results = pattern.findall(topology)
        if results:
            eNodeId = results[0][1]
            newENode = eNode(siteName, eNodeId)
            for index, item in enumerate(results):
                portOne = results[index][2]
                portTwo = results[index][3]
                portThree = results[index][4]
                bbp = eNode.BBP(portOne,portTwo,portThree)
                newENode.addCellBpp(bbp=bbp)
    except Exception:
        print "error"
    finally:
        return  newENode


def generateBBP():
    pass
if __name__ == "__main__":
    print getDspInfoByName("L84654")
