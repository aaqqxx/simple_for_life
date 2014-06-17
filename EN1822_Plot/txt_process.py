#coding:utf-8
#!/usr/env/bin python

__author__ = 'SIOM'

a='''本系统选用德国TOPAS公司的ATM 241
气溶胶发生器，该发生器可产生最高浓度大于108
颗/cm3 的多分散气溶胶粒子，且浓度可调节，能
够满足检漏系统对高浓度粒子的需求。管路中的喷
嘴装置和压差计用于测量管道中的风量值。三通管
路设计一路为主气流管，用作测试气流；另一路为
旁通管，在更换被测过滤器过程中主气流电动阀关
闭时打开。这样一方面可以防止在更换过滤器时，
高浓度气溶胶污染检测环境；另一方面使得检测下
一只过滤器时，上游粒子浓度稳定时间大大缩短，
减少等待时间。
'''

a='''主气流风管与被测过滤器之间为一漏斗形风
管，被测过滤器通过一个适配板卧式放置在二维扫
描平台上。漏斗形风管的出风口尺寸最大可放置
1220 mm × 610 mm 规格的过滤器，针对不同规格
的过滤器设计了对应尺寸的适配板以及相应尺寸的
围板，使被测过滤器的下游气流与周围环境的气流
隔离，以避免周围环境对漏点检测造成影响。上下
游粒子计数器均采用Lighthouse公司的Remote 1104
粒子计数器，上位机可通过RS485 对其进行控制。
由于检漏过程中上游管路的粒子浓度非常高，超出
了Remote 1104 的饱和浓度，故安置了3 台德国
TOPAS 公司的稀释比为100:1 的DIL 550 稀释器，
检测过程中根据实际需要串联相应数量的稀释器。
上游采样探头安置在漏斗形风管中间，下游采样探
头固定在一个可在滤芯上方二维移动的探头臂上，
其定位精度可达1 mm，探头和滤芯的距离可人工
调节。
'''

b = a.split('\n')

c = ''
for each in b:
    c=c+each

print c