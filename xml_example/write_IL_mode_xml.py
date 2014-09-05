# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import xlrd
from xml.dom import minidom

start_row = 1


class xmlwrite:
    def __init__(self, resultfile):
        self.resultfile = resultfile
        self.rootname = 'Illumination_mode'
        self.__create_xml_dom()

    def __create_xml_dom(self):
        xmlimpl = minidom.getDOMImplementation()
        self.dom = xmlimpl.createDocument(None, self.rootname, None)
        self.root = self.dom.documentElement

    def __get_spec_node(self, xpath):
        patharr = xpath.split(r'/')
        parentnode = self.root
        exist = 1
        for nodename in patharr:
            if nodename.strip() == '':
                continue
            if not exist:
                return None
            spcindex = nodename.find('[')
            if spcindex > -1:
                index = int(nodename[spcindex + 1:-1])
            else:
                index = 0
            count = 0
            childs = parentnode.childNodes
            for child in childs:
                if child.nodeName == nodename[:spcindex]:
                    if count == index:
                        parentnode = child
                        exist = 1
                        break
                    count += 1
                    continue
                else:
                    exist = 0
        return parentnode


    def write_node(self, parent, nodename, value, attribute=None, CDATA=False):
        node = self.dom.createElement(nodename)
        if value:
            if CDATA:
                nodedata = self.dom.createCDATASection(value)
            else:
                nodedata = self.dom.createTextNode(value)
            node.appendChild(nodedata)
            if attribute and isinstance(attribute, dict):
                for key, value in attribute.items():
                    node.setAttribute(key, value)
        try:
            parentnode = self.__get_spec_node(parent)
        except:
            print 'Get parent Node Fail, Use the Root as parent Node'
            parentnode = self.root
        parentnode.appendChild(node)


    def write_IL_mode(self):
        self.write_node("/", "IL_mode", None)

    def save_xml(self):
        myfile = file(self.resultfile, 'w')
        self.dom.writexml(myfile, encoding='utf-8')
        myfile.close()


class IL_mode_struct:
    def __init__(self):
        "u'illumi_mode', u'd1', u'd2', u'd3', u'd4', u'DOE_mode', u'sigma_outer', u'sigma_inner'"
        self.illumi_mode = "C1"
        self.d1 = 100
        self.d2 = 100
        self.d3 = 100
        self.d4 = 100
        self.DOE_mode = "CONVENTIONAL"
        self.sigma_outer = 2
        self.sigma_inner = 2


def get_info(filename=r"./IL_mode.xlsx"):
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    nrows = table.nrows
    # ncols=table.ncols

    IL_mode_list = []

    for each in xrange(start_row, nrows):
        print table.row_values(each)
        IL_mode = IL_mode_struct()
        IL_mode.illumi_mode = table.row_values(each)[0]
        IL_mode.d1 = table.row_values(each)[1]
        IL_mode.d2 = table.row_values(each)[2]
        IL_mode.d3 = table.row_values(each)[3]
        IL_mode.A1 = table.row_values(each)[4]
        IL_mode.DOE_mode = table.row_values(each)[5]
        IL_mode.sigma_outer = table.row_values(each)[6]
        IL_mode.sigma_inner = table.row_values(each)[7]
        IL_mode_list.append(IL_mode)

    return IL_mode_list
    # print table.row_values(0)


if __name__ == "__main__":
    IL_mode_list = get_info()
    xr = xmlwrite(r'test1.xml')
    # xr.write_Illumination_modes()

    for index, each in enumerate(IL_mode_list):
        xr.write_IL_mode()
        xr.write_node('/IL_mode[%s]/' % index, 'illumi_mode', each.illumi_mode)
        xr.write_node('/IL_mode[%s]/' % index, 'd1', str(each.d1))
        xr.write_node('/IL_mode[%s]/' % index, 'd2', str(each.d2))
        xr.write_node('/IL_mode[%s]/' % index, 'd3', str(each.d3))
        xr.write_node('/IL_mode[%s]/' % index, 'A1', str(each.d4))
        xr.write_node('/IL_mode[%s]/' % index, 'DOE_mode', str(each.DOE_mode))
        xr.write_node('/IL_mode[%s]/' % index, 'sigma_outer', str(each.sigma_outer))
        xr.write_node('/IL_mode[%s]/' % index, 'sigma_inner', str(each.sigma_inner))
    xr.save_xml()

    # print illumi_mode.illumi_mode
    #
    # # print "<?xml version="1.0" encoding="UTF-8"?>"
    #
    # print "<Illumination_modes>"
    # for each in IL_mode_list:
    # print "<IL_mode>"
    # print "<illumi_mode>" + each.illumi_mode + "</illumi_mode>"
    #     print "<d1>"+ str(each.d1)+"</d1>"
    #     print "<d2>" + str(each.d2) + "</d2>"
    #     print "<d3>"+str(each.d3) + "</d3>"
    #     print "<A1>"+str(each.A1) + "</A1>"
    #     print "<DOE_mode>"+str(each.DOE_mode)+"</DOE_mode>"
    #     print "<sigma_outer>"+str(each.sigma_outer)+"</sigma_outer>"
    #     print "<sigma_inner>"+str(each.sigma_inner) + "</sigma_inner>"
    #     print "</IL_mode>"
    # print "</Illumination_modes>"



