# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 12:39:16 2023

@author: amrdo
"""

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

class ScrollLabel(QLabel):
    dragged= pyqtSignal(int,int)
    
    def __init__(self,parent=None):
        super(ScrollLabel, self).__init__(parent)
        self.prev_pos = None
        self.xloc=0
        self.yloc=0

    def mousePressEvent(self, event):
        self.prev_pos = event.pos()

    def mouseMoveEvent(self, event):
        global xloc
        global yloc
        if self.prev_pos:
            # Calculate the difference between current and previous positions
            delta = event.pos() - self.prev_pos
            

            # Detect the direction of mouse movement
            if delta.x() > 0:
                #print("Mouse dragged to the right")
                self.xloc+=1
                #print(self.xloc)
            elif delta.x() < 0:
                #("Mouse dragged to the left")
                self.xloc-=1
                #print(self.xloc)
            if delta.y() > 0:
                #print("Mouse dragged down")
                self.yloc-=1
                #print(self.yloc)
            elif delta.y() < 0:
                #print("Mouse dragged up")
                self.yloc+=1
                #print(self.yloc)

        # Update the previous position for the next event
        self.prev_pos = event.pos()
        self.dragged.emit(self.xloc,self.yloc)

    def mouseReleaseEvent(self, event):
        self.prev_pos = None