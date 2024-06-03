import sys
from tkinter import * 
from tkinter.ttk import * 
from time import strftime 
import pyqtgraph as pg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsEllipseItem,QApplication,QPushButton,QGraphicsGridLayout,QGraphicsScene
from PyQt5.QtGui import QTransform,QPen,QPolygonF,QImage, QIcon, QPixmap, QPalette, QBrush, QColor, QFontDatabase, QFont
from PyQt5.QtWidgets import QGraphicsPolygonItem,QApplication, QWidget, QProgressBar, QLabel, QTabWidget, QGridLayout, QVBoxLayout, \
QHBoxLayout, QSizePolicy, QSpacerItem, QStyle, QStyleFactory, QPushButton, QFrame, QFontDialog, QStackedWidget
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from PyQt5.QtCore import QPointF,Qt
class Main(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        loadUi("untitled.ui",self)
        self.comboBox.currentIndexChanged.connect(self.alegeforma)
        self.comboBox_2.currentIndexChanged.connect(self.alegetransformarea)
        self.pushButton.clicked.connect(self.deseneaza_imaginea_translata)
        self.pushButton.clicked.connect(self.deseneaza_imaginea_rotita)
        self.scene = QGraphicsScene()
        self.scene_2 = QGraphicsScene()
        self.graphicsView_2.setScene(self.scene_2)
        self.graphicsView.setScene(self.scene)
        self.label_2.setVisible(False)
        self.label.setVisible(False)
        self.grid()
        self.axe()
        self.unghi=0
        self.x=0
        self.y=0
        self.saved_figure = None

    def alegeforma(self):
        self.scene.clear()
        self.scene_2.clear()
        self.grid()
        self.axe()
        shape = self.comboBox.currentText()
        if shape == "Patrat":
            self.deseneaza_patrat()
        elif shape == "Cerc":
            self.deseneaza_cerc()
        elif shape== "Triunghi":
            self.deseneaza_triunghi()
    def deseneaza_cerc(self):
        circle = QGraphicsEllipseItem(-10, -10, 20, 20) 
        circle.setPen(QPen(QColor('blue')))
        circle.setBrush(QBrush(QColor('blue'))) 
        self.scene_2.addItem(circle)
    def deseneaza_patrat(self):
        points = [
            QPointF(10, 10),
            QPointF(10, -10),
            QPointF(-10, -10),
            QPointF(-10, 10)
        ]
        patrat = QPolygonF(points)
        item = QGraphicsPolygonItem(patrat)
        item.setBrush(QBrush(QColor('red')))
        item.setPen(QPen(QColor('red')))
        self.scene_2.addItem(item)
    def deseneaza_triunghi(self):
        points = [
            QPointF(0, 10),
            QPointF(10, -10),
            QPointF(-10, -10)
        ]
        triunghi = QPolygonF(points)
        item = QGraphicsPolygonItem(triunghi)
        item.setBrush(QBrush(QColor('green')))
        item.setPen(QPen(QColor('green')))
        self.scene_2.addItem(item)
    def grid(self):
        spatiu = 10
        pen = QPen(QColor(200, 200, 200), 1, Qt.DotLine)
        for x in range(-300, 301, spatiu):
            self.scene.addLine(x, -300, x, 300, pen)
            self.scene_2.addLine(x, -300, x, 300, pen)
        for y in range(-300, 301, spatiu):
            self.scene.addLine(-300, y, 300, y, pen)
            self.scene_2.addLine(-300, y, 300, y, pen)
    def axe(self):
        pen = QPen(QColor(0, 0, 0), 2)
        self.scene.addLine(-300, 0, 300, 0, pen)
        self.scene.addLine(0, -300, 0, 300, pen)
        self.scene_2.addLine(-300, 0, 300, 0, pen)
        self.scene_2.addLine(0, -300, 0, 300, pen)
    def alegetransformarea(self):
        selectie = self.comboBox_2.currentText()
        if selectie == "Translatie":
            self.label_2.setVisible(True)
            self.label.setVisible(False)
            self.pushButton.clicked.disconnect()
            self.pushButton.clicked.connect(self.deseneaza_imaginea_translata) 
        elif selectie == "Rotatie":
            self.label.setVisible(True) 
            self.label_2.setVisible(False)
            self.pushButton.clicked.disconnect()
            self.pushButton.clicked.connect(self.deseneaza_imaginea_rotita)
    def deseneaza_imaginea_translata(self): 
        translatie=self.lineEdit.text()
        sub=translatie.split("&")
        xstring=sub[0]
        ystring=sub[1]
        self.x=float(xstring)
        self.y=float(ystring)
        items=self.scene_2.items()
        item=items[0]
        if isinstance(item, QGraphicsPolygonItem):
            translated_item = QGraphicsPolygonItem(item.polygon())
            for scene_item in self.scene.items():
                if isinstance(scene_item, QGraphicsPolygonItem):
                    self.scene.removeItem(scene_item)
            brush = item.brush()
            pen = item.pen()
            translated_item.setBrush(brush)
            translated_item.setPen(pen)
            translated_item.setPos(item.pos().x() + self.x, item.pos().y() + self.y)
            self.scene.addItem(translated_item)
        elif isinstance(item, QGraphicsEllipseItem):
            translated_item = QGraphicsEllipseItem(item.rect())
            for scene_item in self.scene.items():
                if isinstance(scene_item, QGraphicsEllipseItem):
                    self.scene.removeItem(scene_item)
            brush = item.brush()
            pen = item.pen()
            translated_item.setBrush(brush)
            translated_item.setPen(pen)
            translated_item.setPos(item.pos().x() + self.x, item.pos().y() + self.y)
            self.scene.addItem(translated_item)

    def deseneaza_imaginea_rotita(self):
        self.unghi = float(self.lineEdit.text())
        items = self.scene_2.items()
        if items: 
            item = items[0] 
            if isinstance(item, QGraphicsPolygonItem): 
                rotated_item = QGraphicsPolygonItem(item.polygon())
                x_center = rotated_item.boundingRect().center().x()
                y_center = rotated_item.boundingRect().center().y()
                rotated_item.setRotation(self.unghi)  # Rotește forma
                new_x_center = rotated_item.boundingRect().center().x()
                new_y_center = rotated_item.boundingRect().center().y()
                delta_x = x_center - new_x_center
                delta_y = y_center - new_y_center            
                for scene_item in self.scene.items():
                    if isinstance(scene_item, QGraphicsPolygonItem):
                        self.scene.removeItem(scene_item)      
                brush = item.brush()
                pen = item.pen()
                rotated_item.setBrush(brush)
                rotated_item.setPen(pen)
                rotated_item.setPos(rotated_item.x() + delta_x, rotated_item.y() + delta_y)
                self.scene.addItem(rotated_item)
            elif isinstance(item, QGraphicsEllipseItem): 
                rotated_item = QGraphicsEllipseItem(item.rect())
                x_center = rotated_item.boundingRect().center().x()
                y_center = rotated_item.boundingRect().center().y()
                rotated_item.setRotation(self.unghi)  
                new_x_center = rotated_item.boundingRect().center().x()
                new_y_center = rotated_item.boundingRect().center().y()
                delta_x = x_center - new_x_center
                delta_y = y_center - new_y_center
                for scene_item in self.scene.items():
                    if isinstance(scene_item, QGraphicsEllipseItem):
                        self.scene.removeItem(scene_item)
                brush = item.brush()
                rotated_item.setBrush(brush)
                rotated_item.setPos(rotated_item.x() + delta_x, rotated_item.y() + delta_y)
                self.scene.addItem(rotated_item)
if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    window = Main()
    window.resize
    window.show()
    app.exec_()
    