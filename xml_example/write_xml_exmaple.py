# coding:utf-8
#!/usr/bin/env python

__author__ = 'XingHua'

"""

"""
#!\urs\bin\env python
#encoding: utf-8
from xml.dom import minidom


class xmlwrite:
    def __init__(self, resultfile):
        self.resultfile = resultfile
        self.rootname = 'api'
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
                index = int(nodename[spcindex+1:-1])
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


    def write_start_time(self, time):
        self.write_node('/','StartTime', time)

    def write_end_time(self, time):
        self.write_node('/','EndTime', time)

    def write_pass_count(self, count):
        self.write_node('/','PassCount', count)

    def write_fail_count(self, count):
        self.write_node('/','FailCount', count)

    def write_case(self):
        self.write_node('/','Case', None)

    def write_case_no(self, index, value):
        self.write_node('/Case[%s]/' % index,'No', value)

    def write_case_url(self, index, value):
        self.write_node('/Case[%s]/' % index,'URL', value)

    def write_case_dbdata(self, index, value):
        self.write_node('/Case[%s]/' % index,'DBData', value)

    def write_case_apidata(self, index, value):
        self.write_node('/Case[%s]/' % index,'APIData', value)

    def write_case_dbsql(self, index, value):
        self.write_node('/Case[%s]/' % index,'DBSQL', value, CDATA=True)

    def write_case_apixpath(self, index, value):
        self.write_node('/Case[%s]/' % index,'APIXPath', value)

    def save_xml(self):
        myfile = file(self.resultfile, 'w')
        self.dom.writexml(myfile, encoding='utf-8')
        myfile.close()


if __name__ == '__main__':
      xr = xmlwrite(r'.\test.xml')
      xr.write_start_time('2223')
      xr.write_end_time('444')
      xr.write_pass_count('22')
      xr.write_fail_count('33')
      xr.write_case()
      xr.write_case()
      xr.write_case_no(0, '0')
      xr.write_case_url(0, 'http://www.google.com')
      xr.write_case_url(0, 'http://www.google.com')
      xr.write_case_dbsql(0, 'select * from ')
      xr.write_case_dbdata(0, 'dbtata')
      xr.write_case_apixpath(0, '/xpath')
      xr.write_case_apidata(0, 'apidata')
      xr.write_case_no(1, '1')
      xr.write_case_url(1, 'http://www.baidu.com')
      xr.write_case_url(1, 'http://www.baidu.com')
      xr.write_case_dbsql(1, 'select 1 from ')
      xr.write_case_dbdata(1, 'dbtata1')
      xr.write_case_apixpath(1, '/xpath1')
      xr.write_case_apidata(1, 'apidata1')
      xr.save_xml()
