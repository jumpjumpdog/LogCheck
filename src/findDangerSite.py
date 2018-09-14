#-*- encoding=utf8 -*-
import  os, gzip, xml.dom.minidom, csv
from Site import  Site,BaseBandEqm




# 全局变量存储site
g_site_dict = {}

# 遍历所有的site，察看当前cell绑定的基带设备是否在site
def findDangerSite():
    for site_name in g_site_dict.keys():
        site = g_site_dict[site_name]
        cells = site.getCellDic()
        for name,cell in cells.items():
            eqmId  = cell.getEqmId()
            # 如果未绑定则不处理
            if eqmId=="":
                continue
            eqm = site.getEqm(eqmId)
            if eqm ==None:
                continue
            if(eqm.getType()!="2"):
                cell.setReason("typeError")
                cell.setSafeStatus(False)
                site.setSafeStatus(False)
                site.addDangerCell(cell)
                continue

            if(eqm.getElementNum()!=1):
                cell.setReason("wrongElement")
                cell.setSafeStatus(False)
                site.setSafeStatus(False)
                site.addDangerCell(cell)
                continue




def processOneSite(site_name,content):
    site = Site(site_name)
    dom = xml.dom.minidom.parseString(content)
    root = dom.documentElement
    # 获取cell和eqm绑定节点
    euCellPriBBEqm = root.getElementsByTagName("EuCellPriBBEqm")
    # 获取所有cell
    cells = root.getElementsByTagName("Cell")
    # 获取所有设备
    baseband_eqms = root.getElementsByTagName("BASEBANDEQM")

    for eqm in baseband_eqms:
        baseband_eqm_id = eqm.getElementsByTagName("BASEBANDEQMID")[0].childNodes[0].data
        baseband = BaseBandEqm(baseband_eqm_id)
        site.avaliBBqIdDecrease(baseband_eqm_id)

        baseband_eqm_type = eqm.getElementsByTagName("BASEBANDEQMTYPE")[0].childNodes[0].data
        baseband.setType(baseband_eqm_type)

        elements = eqm.getElementsByTagName("element")
        for element in elements:
            CN = element.getElementsByTagName("CN")[0].childNodes[0].data
            SRN = element.getElementsByTagName("SRN")[0].childNodes[0].data
            SN = element.getElementsByTagName("SN")[0].childNodes[0].data
            new_element = baseband.Element(CN, SRN, SN)
            baseband.addElement(new_element)
        site.addBaseBandEqm(baseband)


    for cell in cells:
        local_cell_id = cell.getElementsByTagName("LocalCellId")[0]
        site.addCell(local_cell_id.childNodes[0].nodeValue)

    for eu in euCellPriBBEqm:
        attributes = eu.getElementsByTagName("attributes")
        for attribute in attributes:
            local_cell_id = attribute.getElementsByTagName("LocalCellId")
            eqmId = attribute.getElementsByTagName("PriBaseBandEqmId")
            if len(local_cell_id) != 0:
                local_cell_id = local_cell_id[0].childNodes[0].data
                site.cell_dic[local_cell_id].setEqmId(eqmId[0].childNodes[0].data)
                site.cell_dic[local_cell_id].setEqm(site.getEqm(eqmId[0].childNodes[0].data))
    g_site_dict[site.getName()] = site


  # 递归处理
def findSite(path):
    if os.path.isfile(path):
        handleOneFile(path)
        return

    for file in os.listdir(path):
        file_name = os.path.join(path, file)
        if os.path.isfile(file_name):
            handleOneFile(file_name)
        if os.path.isdir(file_name):
            findSite(file_name)



def handleOneFile(path):
    if path.find(".gz")!=-1:
        site_name = path.split("\\")[1]
        with gzip.GzipFile(mode="rb",fileobj=open(path, 'rb')) as g:
            content = g.read()
            processOneSite(site_name, content)

def outPut(outputPath):
    with open("danger_sites.csv", "wb+") as csvfile:
        fieldNames = ["site_name", "cell_id", "reason"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
        writer.writeheader()

        danger_list = filter(lambda x: x.getSafeStatus() == False, g_site_dict.values())
        for site in danger_list:
            rows = []
            cells = site.getDangerCells()
            for index, cell in enumerate(cells):
                row = {}
                if index == 0:
                    row["site_name"] = site.getName()
                row["cell_id"] = cell.getCellId()
                row["reason"] = cell.getReason()
                rows.append(row)
            writer.writerows(rows)








