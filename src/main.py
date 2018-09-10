#-*- encoding=utf8 -*-
import  sys, os, gzip, xml.dom.minidom
from Site import  Site, Cell, BaseBandEqm



# 全局变量存储site
g_site_list = []

# 遍历所有的site，察看当前cell绑定的基带设备是否在site
def findDangerSite():
    for site in g_site_list:
        cells = site.getCellDic()
        for name,cell in cells.items():
            eqmId  = cell.getEqmId()
            # 如果未绑定则不处理
            if eqmId=="":
                continue
            # 如果绑定则检测对应的设备是否符合规则(这种情况不存在)
            # if not site.containEqm(eqmId):
            #     cell.setReason("noeqm")
            #     site.setSafeStatus(False)
            #     site.addDangerCell(cell)
            #     continue

            eqm = site.getEqm(eqmId)
            if(eqm.getType()!="2"):
                cell.setReason("typeError")
                site.setSafeStatus(False)
                site.addDangerCell(cell)
                continue

            if(eqm.getElementNum()!=1):
                cell.setReason("wrongelement")
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
    g_site_list.append(site)


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
        parent_path = os.path.split(path)[0]
        with gzip.GzipFile(mode="rb",fileobj=open(path, 'rb')) as g:
            content = g.read()
            processOneSite(site_name, content)

def outPut(outputPath):
    with open("danger_site_list", "w+") as f:
        f.write("danger_site_name:  ")
        danger_list = filter(lambda x: x.getSafeStatus() == False, g_site_list)
        for site in danger_list:
            f.write(site.getName() + "\n")
            cells = site.getDangerCells()
            for cell in cells:
                f.write(cell.getCellId()+"     ")
                f.write(cell.getReason()+"     \n")



if __name__ == "__main__":
    inputPath = sys.argv[1]
    outputPath = sys.argv[2]
    argv_error = False
    if not inputPath or len(inputPath)==0:
        argv_error = True
        print "输入路径不合法"
    if not outputPath or len(outputPath)==0:
        argv_error = True
        print "输出路径不合法"
    if argv_error:
        print "请重新输入"
    else:
        findSite(inputPath)


    # 遍历所有的site，将危险的site标记
    findDangerSite()

    #输出
    outPut(outputPath)



