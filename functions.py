from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout,QMessageBox, QSlider, QLabel, QPushButton, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from PIL import Image,ImageEnhance
import PIL
from PyQt5.QtGui import QPixmap
import cv2
import os
import shutil
from scipy.fft import fft
from scipy.fft import rfft ,rfftfreq, irfft
from PyQt5.QtGui import QPainter, QPen, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QRect 
from scipy import fftpack
import logging
import threading

logging.basicConfig(filename='Basic.txt',level=logging.INFO)

class ImageObj:
    def __init__(self,label,component,selection,imaginary_original=0,real_original=0,magnitude_original=0,phase_original=0,magnitude=0,phase=0,real=0,imaginary=0,paths=0,actualimage=0,loaded=False):
        self.label=label
        self.component=component
        self.selection=selection
        self.actualimage=actualimage
        self.magnitude=magnitude
        self.phase=phase
        self.real=real
        self.imaginary=imaginary
        self.loaded=False
        self.magnitude_original=magnitude_original
        self.phase_original=phase_original
        self.real_original=real_original
        self.imaginary_original=imaginary_original
        
    
    def Browse(self,n):
        if self.imageList[n].loaded:
            if os.path.exists(f'{n}'):
                shutil.rmtree(f'{n}')
            self.imageList[n].loaded=False
            ImageObj.Browse(self,n)
        else:
            options = QFileDialog.Options()
            self.file_name1, _ = QFileDialog.getOpenFileName(self, "Open File", "", "JPG Files (*.jpeg);;PNG Files(*.png)", options=options)
            if self.file_name1:
                logging.info(f"Image loaded successfuly in {n}")
                grayscale_image=Image.open(self.file_name1).convert('L')
                
                
                self.imageList[n].actualimage=grayscale_image
                
                #check minimum here
                os.mkdir(f'{n}')
                image=f'{n}\{n}.png'
                
                
                if grayscale_image.width*grayscale_image.height<self.minimum[0]*self.minimum[1]:
                    logging.info(f'Image {n} is the new smallest size, resizing all')
                    self.minimumIndex=n
                    self.minimum=(grayscale_image.width,grayscale_image.height)
                    grayscale_image.save(f'{n}\{n}.png')
                    grayscale_image.save(f'{n}\{n}_original.png')
                    ImageObj.resize_all(self)
                else:
                    logging.info(f'Another image is smaller than Image {n}. Resizing now.')
                    grayscale_image=grayscale_image.resize(self.minimum, PIL.Image.Resampling.LANCZOS)
                    grayscale_image.save(f'{n}\{n}.png')
                    grayscale_image.save(f'{n}\{n}_original.png')
                    ImageObj.FourierTransform(self,image,n)
                    
                    self.imageList[n].label.setPixmap(QtGui.QPixmap(image))   
    
    def FourierTransform(self,image_path,n):
        img = cv2.imread(image_path, 0)
        ft = np.fft.fft2(img)
        fourier_shift = np.fft.fftshift(ft)
        magnitude = np.multiply(np.log10(1+np.abs(fourier_shift)), 20)
        
        phase = np.angle(fourier_shift)
        real = np.real(fourier_shift)
        imaginary = np.imag(fourier_shift)
        
        magnitude_normalized,phase_normalized,real_normalized,imaginary_normalized=ImageObj.normalize(self,magnitude,phase,real,imaginary)
        magnitude = np.abs(fourier_shift)
        self.imageList[n].magnitude_original=magnitude.copy()
        self.imageList[n].phase_original=phase.copy()
        self.imageList[n].real_original=real.copy()
        self.imageList[n].imaginary_original=imaginary.copy()
        
        logging.info('Successfully generated Magnitude, Phase, Real, Imaginary and normalized for viewing')
        cv2.imwrite(f"{n}\{n}_magnitude.png", magnitude_normalized)
        cv2.imwrite(f"{n}\{n}_phase.png", phase_normalized)
        cv2.imwrite(f"{n}\{n}_real.png", real_normalized)
        cv2.imwrite(f"{n}\{n}_imaginary.png", imaginary_normalized)
        paths=[]
        paths.append(f"{n}\{n}_magnitude.png")
        paths.append(f"{n}\{n}_phase.png")
        paths.append(f"{n}\{n}_real.png")
        paths.append(f"{n}\{n}_imaginary.png")
        
        self.imageList[n].paths=paths
        self.imageList[n].magnitude=magnitude
        self.imageList[n].phase=phase
        self.imageList[n].real=real
        self.imageList[n].imaginary=imaginary
        self.imageList[n].loaded=True
        
        displayed_component=self.imageList[n].selection.currentIndex()

        self.imageList[n].component.setPixmap(QPixmap(self.imageList[n].paths[displayed_component]))
        
        if self.rectangleSlider.value():
            ImageObj.selected_region(self)
        logging.info(f'Successfully displayed in Image {n}')
        
    def normalize(self,magnitude,phase,real,imaginary):
        magnitude_normalized = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        phase_normalized = cv2.normalize(phase, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        real_normalized = cv2.normalize(real, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        imaginary_normalized = cv2.normalize(imaginary, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        logging.info('Created normalized versions of requested image')
        return magnitude_normalized,phase_normalized,real_normalized,imaginary_normalized
    
    def reconstruct(self,real,imaginary,ri=0):
        if ri==0:
            Mixed_FT = real + 1j * imaginary
        else:
            Mixed_FT = np.multiply(real, np.exp(1j *imaginary))
        Inverse_fourier_image = np.real(np.fft.ifft2(np.fft.ifftshift(Mixed_FT))) 
        Inverse_fourier_image = cv2.normalize(Inverse_fourier_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        logging.info('Successful inverse fourier on real and imaginary values')
        return Inverse_fourier_image
    

           
    def resize_all(self):
            
            for i in range(4):
                if self.imageList[i].actualimage:
                    self.imageList[i].actualimage=self.imageList[i].actualimage.resize(self.minimum)
                    image=f'{i}\{i}.png'
                    self.imageList[i].actualimage.save(image)
                    ImageObj.FourierTransform(self,image,i)
                    self.imageList[i].label.setPixmap(QtGui.QPixmap(image))   
            logging.info('Resized all existing images')

    def switchComponent(self,caller):
        image=self.imageList[caller]
        path=image.paths
        display=path[image.selection.currentIndex()]
        image.component.setPixmap(QPixmap(display))
        if self.rectangleSlider.value():
            ImageObj.selected_region(self)
        logging.info(f'Selected another component to display (#{image.selection.currentIndex()})')
        
    def sliderFunction(self,caller):
        val=self.MixBoxList[caller].currentIndex()
        self.percentageValuesList[caller][val]=self.slidersList[caller].value()
        self.percentageList[caller].setText(str(self.slidersList[caller].value())+'%')
        logging.info(f'Mixing Slider #{caller} updated value {val} to {self.percentageValuesList[caller][val]}')
        
    def switchMixerComponent(self,caller):
        self.slidersList[caller].setValue(self.percentageValuesList[caller][self.MixBoxList[caller].currentIndex()])
        self.percentageValuesList[caller]
        logging.info(f'Mixing SLider #{caller} now controls {self.MixBoxList[caller].currentIndex()}')
        
    def Mixer(self):
        
        zerovalues=(self.minimum[1],self.minimum[0])
        values=[np.zeros(zerovalues),np.zeros(zerovalues)]
        for i in range(4):
            if self.imageList[i].loaded:
                if self.combo2Radio.isChecked():
                        logging.info('Now working on Magnitude and Phase:')
                        values[0]+=(self.imageList[i].magnitude *(self.percentageValuesList[i][0]/100))
                        values[1]+=(self.imageList[i].phase*(self.percentageValuesList[i][1]/100))
                elif self.combo1Radio.isChecked():
                        logging.info('Now working on Real and Imaginary:')
                        values[0]+=(self.imageList[i].real *(self.percentageValuesList[i][0])/100)
                        values[1]+=(self.imageList[i].imaginary*(self.percentageValuesList[i][1])/100)
        for i in range(2):
            if self.outputRadioList[i].isChecked():
                output=self.outputRadioList[i]
                logging.info(f'Displaying on output #{i+1}:')
                number=i+1
                break
        image=ImageObj.reconstruct(self,values[0],values[1],self.combo2Radio.isChecked())
        image= cv2.resize(image,dsize=(340,295),interpolation=cv2.INTER_CUBIC)
        #image=cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        cv2.imwrite(f'output\output{number}.png',image)
        cv2.imwrite(f'output\output{number}_original.png',image)
        image2 = Image.open(f'output\output{number}.png')
        path=f'output\output{number}.png'
        
        self.outputLabelList[number-1].setPixmap(QtGui.QPixmap(path))
        logging.info(f'Successfuly displayed image on output {number}')
    def toggleCombo1(self):
        logging.info(f'Switched combo to Real, Imaginary pairs')
        for i in range(4):
            self.MixBoxList[i].clear()
            self.MixBoxList[i].addItem('Real')
            self.MixBoxList[i].addItem('Imaginary')
            
    def toggleCombo2(self):
        logging.info(f'Switched combo to Magnitude, Phase pairs')
        for i in range(4):
            self.MixBoxList[i].clear()
            self.MixBoxList[i].addItem('Magnitude')
            self.MixBoxList[i].addItem('Phase')
        ImageObj.Mixer(self)
            
    # def mixer_thread(self):
    #     thread = threading.Thread(target=ImageObj.Mixer,args=(self,))
    #     thread.start()
        
    def selected_region(self): 
        dimension = self.rectangleSlider.value()
        
        rect = []
        for i in range(len(self.imageList)):
            rect.append(self.imageList[i].component)

        for i in range(2):
            if self.regionlist[i].isChecked():
                region = self.regionlist[i]
                number = i + 1
                break

        for i in range(len(self.imageList)):
            if self.imageList[i].loaded:
                rect[i].clear()
                displayed_component = self.imageList[i].selection.currentIndex()
                self.imageList[i].component.setPixmap(QPixmap(self.imageList[i].paths[displayed_component]))
               
                current_pixmap = self.imageList[i].component.pixmap()
                newpixmap=current_pixmap.copy()
                # Create a new pixmap if none exists
                if current_pixmap is None:
                    current_pixmap = QPixmap(self.imageList[i].component.size())
                    current_pixmap.fill(Qt.white)
                    #wholepixmap=current_pixmap
    
                if number == 1:
                    painter = QPainter(current_pixmap)
                    painter.setPen(Qt.red)
                    painter.setBrush(QBrush(Qt.red,Qt.DiagCrossPattern))
                    image_width = current_pixmap.width()
                    image_height = current_pixmap.height()
                    rect_width = int(max(image_width, image_height) * dimension / 100)
                    rect_height = int(min(image_width, image_height) * dimension / 100)
                    rect_x = (image_width - rect_width) // 2
                    rect_y = (image_height - rect_height) // 2
                    painter.drawRect(rect_x, rect_y, rect_width, rect_height)
                    painter.end()
                    newrect=QRect(rect_x,rect_y,rect_width,rect_height)
                    self.imageList[i].component.setPixmap(current_pixmap)
                    newpixmap=newpixmap.copy(newrect)
                    newpixmap.save('new.png')
                    final=cv2.imread('new.png', cv2.IMREAD_GRAYSCALE)
                    dimensions=final.shape
                    newmin=[self.minimum[1],self.minimum[0]]
                    expanded=np.zeros(newmin)
                    
                    start_row = (self.minimum[1] - dimensions[0]) // 2
                    start_col = (self.minimum[0] - dimensions[1]) // 2
                    expanded[start_row:start_row+dimensions[0], start_col:start_col+dimensions[1]] = final
                    expanded[expanded>=1]=1
                    self.imageList[i].magnitude=self.imageList[i].magnitude_original*expanded
                    self.imageList[i].phase=self.imageList[i].phase_original*expanded
                    self.imageList[i].real=self.imageList[i].real_original*expanded
                    self.imageList[i].imaginary=self.imageList[i].imaginary_original*expanded
                    
                else:
                    painter2 = QPainter(current_pixmap)
                    painter2.setPen(Qt.red)
                    painter2.setBrush(QBrush(Qt.red,Qt.DiagCrossPattern))
                    
                    image_width = current_pixmap.width()
                    image_height = current_pixmap.height()
                    rect_width2 = image_width
                    rect_height2 = image_height
                    rect_width = int(max(image_width, image_height) * dimension / 100)
                    rect_height = int(min(image_width, image_height) * dimension / 100)
                    rect_x = (image_width - rect_width) // 2
                    rect_y = (image_height - rect_height) // 2

            
                    # Create a QPainterPath for the dashed lines
                    path = QPainterPath()
                    path.addRect(0, 0, rect_width2, rect_height2)
    
                    # Exclude the expanding rectangle from the dashed lines
                    path.addRect(rect_x, rect_y, rect_width, rect_height)
    
                    # Fill the entire pixmap with dashed lines, excluding the expanding rectangle
                    painter2.setBrush(QBrush(Qt.red,Qt.DiagCrossPattern))
                    painter2.drawPath(path)
                    newrect=QRect(rect_x,rect_y,rect_width,rect_height)
                    painter2.end()
                    self.imageList[i].component.setPixmap(current_pixmap)
                    
                    painter3=QPainter(newpixmap)
                    painter3.fillRect(newrect,Qt.black)
                    painter3.drawRect(rect_x, rect_y, rect_width, rect_height)
                    painter3.end()
                    newpixmap.save('new.png')
                    final=cv2.imread('new.png', cv2.IMREAD_GRAYSCALE)
                    final[final>=1]=1
                    self.imageList[i].magnitude=self.imageList[i].magnitude_original*final
                    self.imageList[i].phase=self.imageList[i].phase_original*final
                    self.imageList[i].real=self.imageList[i].real_original*final
                    self.imageList[i].imaginary=self.imageList[i].imaginary_original*final
                 
        for i in range(2):
            if self.outputLabelList[i].pixmap:
                ImageObj.Mixer(self)
                    
    def change_brightness_contrast(self,x,y,caller,component=False,output=False):
        
            x=(x+60)/60 #Normalizing values to 1
            y=(y+60)/60
            if output:
     
                img=Image.open(f'output\output{caller+1}_original.png')
                
                brightness = ImageEnhance.Brightness(img)
                brightness.enhance(y).save(f'output\output{caller+1}_enhanced.png')
                img2=Image.open(f'output\output{caller+1}_enhanced.png')
                contrast=ImageEnhance.Contrast(img2)
                contrast.enhance(x).save(f'output\output{caller+1}.png')
                self.outputLabelList[caller].setPixmap(QPixmap(f"output\output{caller+1}.png"))
                logging.info(f'Adjusted brightness/contrast for image {caller+1}')
                
            else:
                if component:
                    name=self.imageList[caller].selection.currentText().lower()
                    index=self.imageList[caller].selection.currentIndex()
                    shutil.copyfile(f'{caller}\{caller}_{name}.png',f'{caller}\{caller}_{name}_enhanced.png')
                    img=Image.open(f'{caller}\{caller}_{name}.png')
                    brightness = ImageEnhance.Brightness(img)
                    brightness.enhance(y).save(f'{caller}\{caller}__{name}_enhanced.png')
                    img2=Image.open(f'{caller}\{caller}_{name}_enhanced.png')
                    contrast=ImageEnhance.Contrast(img2)
                    contrast.enhance(x).save(f'{caller}\{caller}_{name}_final.png')
                    self.imageList[caller].component.setPixmap(QPixmap(f"{caller}\{caller}_{name}_final.png"))
                    logging.info(f'Adjusted brightness/contrast for component {caller+1}')
                else:
                    img=Image.open(f'{caller}\{caller}_original.png')
                    brightness = ImageEnhance.Brightness(img)
                    brightness.enhance(y).save(f'{caller}\{caller}_enhanced.png')
                    img2=Image.open(f'{caller}\{caller}_enhanced.png')
                    contrast=ImageEnhance.Contrast(img2)
                    contrast.enhance(x).save(f'{caller}\{caller}.png')
                    self.imageList[caller].label.setPixmap(QPixmap(f"{caller}\{caller}.png"))
                    logging.info(f'Adjusted brightness/contrast for image {caller+1}')
               
            # if component:
            #     name=self.imageList[caller].selection.currentText().lower()
            #     index=self.imageList[caller].selection.currentIndex()
            #     shutil.copyfile(f'{caller}\{caller}_{name}.png',f'{caller}\{caller}_{name}_enhanced.png')
            #     img=Image.open(f'{caller}\{caller}_{name}.png')
            #     brightness = ImageEnhance.Brightness(img)
            #     brightness.enhance(y).save(f'{caller}\{caller}__{name}_enhanced.png')
            #     img2=Image.open(f'{caller}\{caller}_{name}_enhanced.png')
            #     contrast=ImageEnhance.Contrast(img2)
            #     contrast.enhance(x).save(f'{caller}\{caller}_{name}_final.png')
            #     inverse=reconstruct(self.imageList[caller].real,self.imageList[caller].imaginary)
            #     self.imageList[caller].component.setPixmap(QPixmap(f"{caller}\{caller}_{name}_final.png"))
    
            # else:
               
            #     img=Image.open(f'{caller}\{caller}_original.png')
            #     brightness = ImageEnhance.Brightness(img)
            #     brightness.enhance(y).save(f'{caller}\{caller}_enhanced.png')
            #     img2=Image.open(f'{caller}\{caller}_enhanced.png')
            #     contrast=ImageEnhance.Contrast(img2)
            #     contrast.enhance(x).save(f'{caller}\{caller}.png')
            #     self.imageList[caller].label.setPixmap(QPixmap(f"{caller}\{caller}.png"))
            #     FourierTransform(self,f'{caller}\{caller}.png',caller)
        