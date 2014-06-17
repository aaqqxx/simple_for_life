#-*-coding:utf8 -*-
#!/usr/env python
__author__ = 'SIOM'

import GdImageFile
import matplotlib.pyplot as plt
#x=GdImageFile.open(r"c:\2200.TIF")
#x=GdImageFile.open(r'c:\1.jpg')
x=plt.imread(r'c:\2200.TIF')

plt.imshow(x)
plt.show()