import os, sys, xml.dom.minidom
from Site import BaseBandEqm



root = xml.dom.minidom.parse("./EAA387.xml").documentElement

baseBandEqms = root.getElementsByTagName("BASEBANDEQM")
baseBandEqm = baseBandEqms[0]
print baseBandEqm

elements = baseBandEqm.getElementsByTagName("element")
print  len(elements)
print elements[0].toxml()


for element in elements:
    print  element.getElementsByTagName("CN")[0].childNodes[0].data
    print  element.getElementsByTagName("SRN")[0].childNodes[0].data
    print  element.getElementsByTagName("SN")[0].childNodes[0].data


