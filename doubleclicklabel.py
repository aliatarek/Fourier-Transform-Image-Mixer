from PyQt5.QtWidgets import QMainWindow, QApplication,QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import uic
from PyQt5.QtCore import Qt
import interface
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib 
import functions
class DoubleClickLabel(QLabel):
    doubleClicked = pyqtSignal()
    dragged=pyqtSignal(int,int)

    def __init__(self, parent=None):
        super(DoubleClickLabel, self).__init__(parent)
        self.prev_pos = None
        self.xloc=0
        self.yloc=0

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
        super(DoubleClickLabel, self).mouseDoubleClickEvent(event)
        
    def mousePressEvent(self, event):
        self.prev_pos = event.pos()

    def mouseMoveEvent(self, event):
        global xloc
        global yloc
        if self.prev_pos:
            delta = event.pos() - self.prev_pos
            if delta.x() > 0:
                self.xloc+=1
            elif delta.x() < 0:
                self.xloc-=1
            if delta.y() > 0:
                self.yloc-=1
            elif delta.y() < 0:
                self.yloc+=1
            print(self.xloc)
            print(self.yloc)

        self.prev_pos = event.pos()
        self.dragged.emit(self.xloc,self.yloc)

    def mouseReleaseEvent(self, event):
        self.prev_pos = None