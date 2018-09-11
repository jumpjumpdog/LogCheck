import os, sys, xml.dom.minidom, csv
from Site import BaseBandEqm



# root = xml.dom.minidom.parse("./EAA387.xml").documentElement
#
# baseBandEqms = root.getElementsByTagName("BASEBANDEQM")
# baseBandEqm = baseBandEqms[0]
# print baseBandEqm
#
# elements = baseBandEqm.getElementsByTagName("element")
# print  len(elements)
# print elements[0].toxml()
#
#
# for element in elements:
#     print  element.getElementsByTagName("CN")[0].childNodes[0].data
#     print  element.getElementsByTagName("SRN")[0].childNodes[0].data
#     print  element.getElementsByTagName("SN")[0].childNodes[0].data


with open("xxx.csv", "wb+") as csvfile:
    fieldNames = ["site_name", "site_id", "cell_id","bbq_id","bbq_type","port_one","port_two","port_three"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
    writer.writeheader()
    writer.writerow({"site_name":"AAAAAA"})
