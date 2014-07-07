# coding:utf-8
#!/usr/bin/env python

__author__ = 'SAF'
from PyQt4 import QtCore


class MyQObject(QtCore.QObject):
    # 定義一個無參數的signal
    signal1 = QtCore.pyqtSignal()
    # 定義一個有一個整數參數的signal，並且name為qtSignal2。
    signal2 = QtCore.pyqtSignal(int, name='qtSignal2')

    def __init__(self):
        super(MyQObject,
              self).__init__()  # 如果写了__init__()函数，这一行一定要有，否则会出现TypeError: pyqtSignal must be bound to a QObject, not 'MyQObject'

    def connectSigSlot(self):
        # 利用pySignal物件本身提供的connect，我們可以輕易的將pySignal物件與對應的slot相連。
        # 將signal1與myReceiver1連接起來。
        self.signal1.connect(self.myReceiver1)
        # 將signal2與myReceiver2連接起來。
        self.signal2.connect(self.myReceiver2)

    def myEmitter(self):
        # 利用pyqtSignal物件所提供的emit function，我們就可以輕易的發出signal。

        self.signal1.emit()

        self.signal2.emit(10)

    def myReceiver1(self):
        print 'myReceiver1 called'


    def myReceiver2(self, arg):
        print 'myReceiver2 called with argument value %d' % arg


# 簡單的說，透過pyqtSignal，將signal也視為一種物件，所以signal所需的功能皆可由signal本身的method來定義。 所以整個signal的定義與使用完全符合物件導向的精神，程式看起來也更為直覺。
#而pySlot則是一個Python的decorator，我們可以透過他來將一個method定義為slot。
@QtCore.pyqtSlot()
def mySlot(self):
    print ('mySlot received a signal')


@QtCore.pyqtSlot(int)
def mySlot2(self, arg):
    print ('mySlot2 received a signal with argument %d' % arg)


    # 整個slot的定義與舊的方法相較，頓時變得簡單許多。如果，你的UI使透過pyuic4所製作出來的，那　甚至可以透過 slot的名稱來指定要連結的元件與signal。舉例來說，如果你的UI中有一個名為myBtn的按鈕，想要連接他的clicked signal。你只要在你繼承的視窗類別中，定義如下的slot：


@QtCore.pyqtSlot(bool)
def on_myBtn_clicked(self, checked):
    print 'myBtn clicked.'



    # PyQT會自動將這個slot與UI內的myBtn的clicked singal連接起來。真的是非常省事。
    #新的singal/slot的定義與使用方式是PyQT 4.5中的一大改革。可以讓PyQT程式更清楚易讀。如果你也是用PyQT 4.5以後的版本。 建議您開始使用這種新的方式吧。