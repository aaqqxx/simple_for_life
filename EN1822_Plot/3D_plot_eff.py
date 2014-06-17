#-*- coding:utf8 -*-
#!/usr/bin/env python
__author__ = 'SIOM'
import numpy as np
import matplotlib.pyplot as plt

filename=r'c:\Data14H15M9S.txt'
data1_plot=plt.plotfile(filename,(2,),delimiter='\t')
ax=plt.gca()
plt.show()

#data1=data1_plot.get_data()
#plt.show()