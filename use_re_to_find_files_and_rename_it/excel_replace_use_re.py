# coding:utf-8
# !/usr/env/bin python

'''
读取excel文件，使用正则法则将其中的文字替换。
替换excel中的表格信息的文字。
'''

# 读取docx中的文本代码示例
import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH

import xlrd

exteral_diameter2xianjia_dict = {"5-7mm": "61030000141",
                                 "7-10mm": "61030000044",
                                 "9-12mm": "61030000143",
                                 "11-14mm": "61030000145"}

cable_sn2cable_exteral_diameter_dict = {
    'LAPP.0035136': 10.10,
    'LAPP.0035137': 12.10,
    'LAPP.0035142': 11.10,
    'LAPP.0034310': 6.10,
    'LAPP.0034315': 6.90,
    'LAPP.0034406': 6.00,
    'LAPP.0034504': 5.7,
    'LAPP.0035150': 8.2,
    'LAPP.0034340': 10.4,
    'LAPP.0034325': 8.4,
}


def trans_exteral_diameter(exteral_diameter):
    if 5 < exteral_diameter < 7:
        res = "5-7mm"
    elif 7 < exteral_diameter < 10:
        res = "7-10mm"
    elif 9 < exteral_diameter < 12:
        res = "9-12mm"
    elif 11 < exteral_diameter < 14:
        res = "11-14mm"
    else:
        res = "none"
    return res


def get_xianjia_type(cable_sn):
    exteral_diameter = cable_sn2cable_exteral_diameter_dict[cable_sn]
    tmp = trans_exteral_diameter(exteral_diameter)
    res = exteral_diameter2xianjia_dict[tmp]
    # print tmp
    return res
    pass


def chose_xian_jia():
    data = xlrd.open_workbook(ur'\\172.16.78.59\f\sharefiles\KrF电气互联总图素材\EPLAN\文档\Cable.xls')  # 打开xls文件
    table = data.sheets()[0]  # 打开第一张表
    nrows = table.nrows  # 获取表的行数
    num_61030000141 = 0
    num_61030000044 = 0
    num_61030000143 = 0
    num_61030000145 = 0

    for i in range(nrows):  # 循环逐行打印
        if i < 2:  # 跳过第一行
            continue
        # print table.row_values(i)[:13], table.row_values(i)[6]  # 取前十三列
        table.row_values(i)[11] = cable_sn2cable_exteral_diameter_dict[table.row_values(i)[6]]
        table.row_values(i)[12] = get_xianjia_type(table.row_values(i)[6])
        xianjia_type = get_xianjia_type(table.row_values(i)[6])

        if xianjia_type == "61030000141":
            num_61030000141 += 1
        if xianjia_type == "61030000044":
            num_61030000044 += 1
        if xianjia_type == "61030000143":
            num_61030000143 += 1
        if xianjia_type == "61030000145":
            print xianjia_type
            print cable_sn2cable_exteral_diameter_dict[table.row_values(i)[6]]
            num_61030000145 += 1

    print "num_61030000141", num_61030000141
    print "num_61030000044", num_61030000044
    print "num_61030000143", num_61030000143
    print "num_61030000145", num_61030000145



    # print cable_sn2cable_exteral_diameter_dict[table.row_values(i)[6]]


chose_xian_jia()
