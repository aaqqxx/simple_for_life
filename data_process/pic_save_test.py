# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import numpy as np
import matplotlib.pyplot as plt
import sdxf
from dxfwrite import DXFEngine as dxf


def main():
    pos = np.loadtxt("unicom_center_v1.1.txt")
    drawing = dxf.drawing('unicom_center_v1_1.dxf')
    for each in pos:
        point = dxf.point(each)
        point['layer'] = 'points'
        point['color'] = 7
        # point['point'] = (2, 3) # int or float
        drawing.add(point)
    drawing.save()


def rect():
    pos = np.loadtxt("unicom_center_v1.1.txt")
    drawing = dxf.drawing('unicom_center_v1_rect.dxf')
    for each in pos:
        rect = dxf.rectangle(each, 0.05, 0.05, color=7)
        rect['layer'] = 'points'
        # rect['color'] = 7
        # point['point'] = (2, 3) # int or float
        drawing.add(rect)
    drawing.save()


def test():
    pos = np.loadtxt("unicom_center_v1.1.txt")
    # print pos[0]
    d = sdxf.Drawing()
    d.layers.append(sdxf.Layer(name="textlayer", color=3))
    # d.append(d.append(sdxf.Line(points=[tuple(pos[0]), tuple(pos[0])], layer="drawinglayer")))
    # d.append(sdxf.Line(points=[(0.2, 0.5), (0.2, 0.5)], layer="drawinglayer"))
    for each in pos:
        d.append(sdxf.Line(points=[tuple(each), tuple(each)], layer="drawinglayer"))
    d.saveas("unicom_center_v1_1.dxf")
    # for each in data:
    # if each==0:
    # pass


def sdxf_test():
    d = sdxf.Drawing()

    # set the color of the text layer to green
    d.layers.append(sdxf.Layer(name="textlayer", color=3))

    # add drawing elements
    d.append(sdxf.Text('Hello World!', point=(3, 0), layer="textlayer"))
    d.append(sdxf.Line(points=[(0, 0), (1, 1)], layer="drawinglayer"))
    d.append(sdxf.Line(points=[(4, 4), (4, 4)], layer="drawinglayer"))
    # point = sdxf.Point(points=[0.4,3],layer="drawinglayer")
    point = sdxf.Point(points=(0.4, 3), layer="points")
    print dir(point)
    print point.points
    # d.append(sdxf.Point(points=(50.075, 5.025), layer="drawinglayer"))
    d.append(point)
    d.saveas('hello_world.dxf')


def dxf_test():
    drawing = dxf.drawing('drawing.dxf')
    point = dxf.point((1.0, 1.0))
    point['layer'] = 'points'
    point['color'] = 7
    # point['point'] = (2, 3) # int or float
    drawing.add(point)
    drawing.save()


if __name__ == "__main__":
    rect()
    # main()
    # test()
    # sdxf_test()
    # dxf_test()
    # data=np.loadtxt("120_120_res.txt")
    # np.savetxt("60_60res.txt",data[:60,:60],fmt="%.3f",delimiter="\t")

