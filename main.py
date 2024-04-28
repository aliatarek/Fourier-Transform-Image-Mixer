# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import interface
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib 


import sys
     
class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi("Task4UI.ui",self)
        interface.initConnectors(self)
        self.show()

 
app=QApplication(sys.argv)
UIWindow= UI()
app.exec_()

