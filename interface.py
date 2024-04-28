from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton,QLCDNumber,QLabel,QCheckBox
from pyqtgraph import PlotWidget
#from mplwidget import MplWidget
import pyqtgraph
import functions
from functions import ImageObj
from PyQt5 import QtCore
#from classes import channelLine
from PIL import Image,ImageEnhance
import PIL
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
import os,shutil


def initConnectors(self):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Expiration Monitor")
    
    self.minimum=(9999999999,999999999)
    self.minimumIndex=-1
    for i in range(4): #This action deletes the old files used in the previous run
       if os.path.exists(f'{i}'):
           shutil.rmtree(f'{i}')

    self.img1=self.findChild(QtWidgets.QLabel , "img1") 
    self.img2=self.findChild(QtWidgets.QLabel , "img2") 
    self.img3=self.findChild(QtWidgets.QLabel , "img3") 
    self.img4=self.findChild(QtWidgets.QLabel , "img4") 
    
    
    self.img1.doubleClicked.connect(lambda:ImageObj.Browse(self,0))
    self.img2.doubleClicked.connect(lambda:ImageObj.Browse(self,1))
    self.img3.doubleClicked.connect(lambda:ImageObj.Browse(self,2))
    self.img4.doubleClicked.connect(lambda:ImageObj.Browse(self,3))
    
    self.img1.dragged.connect(lambda xloc,yloc:ImageObj.change_brightness_contrast(self,xloc,yloc,0))
    self.img2.dragged.connect(lambda xloc,yloc:ImageObj.change_brightness_contrast(self,xloc,yloc,1))
    self.img3.dragged.connect(lambda xloc,yloc:ImageObj.change_brightness_contrast(self,xloc,yloc,2))
    self.img4.dragged.connect(lambda xloc,yloc:ImageObj.change_brightness_contrast(self,xloc,yloc,3))


    
    self.component1=self.findChild(QtWidgets.QLabel , "component1") 
    self.component2=self.findChild(QtWidgets.QLabel , "component2") 
    self.component3=self.findChild(QtWidgets.QLabel , "component3") 
    self.component4=self.findChild(QtWidgets.QLabel , "component4") 
    
    self.component1.dragged.connect(lambda xloc,yloc:ImageObj.change_brightness_contrast(self, xloc, yloc, 0, 1))
    self.component2.dragged.connect(lambda xloc,yloc:ImageObj.change_brightness_contrast(self, xloc, yloc, 1, 1))
    self.component3.dragged.connect(lambda xloc,yloc:ImageObj.change_brightness_contrast(self, xloc, yloc, 2, 1))
    self.component4.dragged.connect(lambda xloc,yloc:ImageObj.change_brightness_contrast(self, xloc, yloc, 3, 1))
    
    self.output1=self.findChild(QtWidgets.QLabel , "output1") 
    self.output2=self.findChild(QtWidgets.QLabel , "output2") 
    self.output1.dragged.connect(lambda xloc,yloc:ImageObj.change_brightness_contrast(self,xloc,yloc,0,0,1))
    self.output2.dragged.connect(lambda xloc,yloc:ImageObj.change_brightness_contrast(self,xloc,yloc,1,0,1))

    self.outputLabelList=[]
    self.outputLabelList.append(self.output1)
    self.outputLabelList.append(self.output2)

    for i in range(2):
        self.outputLabelList[i].setPixmap(QtGui.QPixmap('outputplaceholder.png'))
    
    self.selection1=self.findChild(QtWidgets.QComboBox , "selection1") 
    self.selection2=self.findChild(QtWidgets.QComboBox , "selection2") 
    self.selection3=self.findChild(QtWidgets.QComboBox , "selection3") 
    self.selection4=self.findChild(QtWidgets.QComboBox , "selection4") 
    
    self.image1=ImageObj(self.img1,self.component1,self.selection1)
    self.image2=ImageObj(self.img2,self.component2,self.selection2)
    self.image3=ImageObj(self.img3,self.component3,self.selection3)
    self.image4=ImageObj(self.img4,self.component4,self.selection4)

    self.imageList=[]
    self.imageList.append(self.image1)
    self.imageList.append(self.image2)
    self.imageList.append(self.image3)
    self.imageList.append(self.image4)
    
    for i in range(4):
        self.imageList[i].label.setPixmap(QtGui.QPixmap('placeholder.png'))
    
    self.selection1.activated.connect(lambda:ImageObj.switchComponent(self,0))
    self.selection2.activated.connect(lambda:ImageObj.switchComponent(self,1))
    self.selection3.activated.connect(lambda:ImageObj.switchComponent(self,2))
    self.selection4.activated.connect(lambda:ImageObj.switchComponent(self,3))

    self.rectangleSlider=self.findChild(QtWidgets.QSlider , "rectangleSlider") 
    
    self.MixBox1=self.findChild(QtWidgets.QComboBox , "component1MixerBox") 
    self.MixBox2=self.findChild(QtWidgets.QComboBox , "component2MixerBox")
    self.MixBox3=self.findChild(QtWidgets.QComboBox , "component3MixerBox")
    self.MixBox4=self.findChild(QtWidgets.QComboBox , "component4MixerBox")
    
    self.MixBoxList=[]
    self.MixBoxList.append(self.MixBox1)
    self.MixBoxList.append(self.MixBox2)
    self.MixBoxList.append(self.MixBox3)
    self.MixBoxList.append(self.MixBox4) 
    
    self.MixBox1.activated.connect(lambda:ImageObj.switchMixerComponent(self,0))
    self.MixBox2.activated.connect(lambda:ImageObj.switchMixerComponent(self,1))
    self.MixBox3.activated.connect(lambda:ImageObj.switchMixerComponent(self,2))
    self.MixBox4.activated.connect(lambda:ImageObj.switchMixerComponent(self,3))
    
    self.MixSlider1=self.findChild(QtWidgets.QSlider , "component1MixerSlider") 
    self.MixSlider2=self.findChild(QtWidgets.QSlider , "component2MixerSlider") 
    self.MixSlider3=self.findChild(QtWidgets.QSlider , "component3MixerSlider") 
    self.MixSlider4=self.findChild(QtWidgets.QSlider , "component4MixerSlider") 
    
    self.MixSlider1.valueChanged.connect(lambda:ImageObj.sliderFunction(self,0))
    self.MixSlider2.valueChanged.connect(lambda:ImageObj.sliderFunction(self,1))
    self.MixSlider3.valueChanged.connect(lambda:ImageObj.sliderFunction(self,2))
    self.MixSlider4.valueChanged.connect(lambda:ImageObj.sliderFunction(self,3))
    
    self.MixSlider1.valueChanged.connect(lambda:ImageObj.Mixer(self))
    self.MixSlider2.valueChanged.connect(lambda:ImageObj.Mixer(self))
    self.MixSlider3.valueChanged.connect(lambda:ImageObj.Mixer(self))
    self.MixSlider4.valueChanged.connect(lambda:ImageObj.Mixer(self))
    
    self.slidersList=[]
    self.slidersList.append(self.MixSlider1)
    self.slidersList.append(self.MixSlider2)
    self.slidersList.append(self.MixSlider3)
    self.slidersList.append(self.MixSlider4)
    
    self.rectangleSlider=self.findChild(QtWidgets.QSlider , "rectangleSlider") 
    self.rectangleSlider.valueChanged.connect(lambda:ImageObj.selected_region(self))
    
    self.inner_region_button=self.findChild(QtWidgets.QRadioButton,"InnerRegion")
    self.outer_region_button=self.findChild(QtWidgets.QRadioButton,"OuterRegion") 
    
    self.inner_region_button.toggled.connect(lambda:ImageObj.selected_region(self))
    self.outer_region_button.toggled.connect(lambda:ImageObj.selected_region(self))
    
    self.regionlist=[]
    self.regionlist.append(self.inner_region_button)
    self.regionlist.append(self.outer_region_button)
    
    
    self.percentage1=self.findChild(QtWidgets.QLabel,"slider1")
    self.percentage2=self.findChild(QtWidgets.QLabel,"slider2")
    self.percentage3=self.findChild(QtWidgets.QLabel,"slider3")
    self.percentage4=self.findChild(QtWidgets.QLabel,"slider4")
    
    self.percentageList=[]
    self.percentageList.append(self.percentage1)
    self.percentageList.append(self.percentage2)
    self.percentageList.append(self.percentage3)
    self.percentageList.append(self.percentage4)
    
    self.progressBar=self.findChild(QtWidgets.QProgressBar,"progressBar")
    
    self.output1Radio=self.findChild(QtWidgets.QRadioButton , "output1Radio") 
    self.output2Radio=self.findChild(QtWidgets.QRadioButton , "output2Radio") 
    
    self.combo1Radio=self.findChild(QtWidgets.QRadioButton , "combo1Radio") 
    self.combo2Radio=self.findChild(QtWidgets.QRadioButton , "combo2Radio") 
    
    self.percentage1Values,self.percentage2Values,self.percentage3Values,self.percentage4Values=([0,0] for i in range(4))
    self.percentageValuesList=[self.percentage1Values,self.percentage2Values,self.percentage3Values,self.percentage4Values]
    
    
    self.combo1Radio.toggled.connect(lambda:ImageObj.toggleCombo1(self))
    self.combo2Radio.toggled.connect(lambda:ImageObj.toggleCombo2(self))
    
    self.outputRadioList=[]
    self.outputRadioList.append(self.output1Radio)
    self.outputRadioList.append(self.output2Radio)
    

    
