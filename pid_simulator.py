# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
import pyqtgraph
import numpy as np

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.plot_data = { 'X':np.arange(0, 256), 'Y':np.full(256, 0), 'Y2':np.full(256, 0) }

        self.resize(600, 600)
        self.setStyleSheet("QMainWindow {background: 'white';}")

        # leyout
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout2)
        
        # pot widget
        self.plotwidget = PlotWidget(self)
        self.plotwidget.setBackground("#FFFFFFFF")
        plotitem = self.plotwidget.plotItem
        plotitem.setLabels(bottom='time', left='position')
        plotitem.getAxis('bottom').setPen( pyqtgraph.mkPen(color='#000000') )
        plotitem.getAxis('left').setPen( pyqtgraph.mkPen(color='#000000') )
        plotitem.setRange(yRange = (0, 50), padding = 0)

        # slider
        self.slider = QtWidgets.QSlider(self)
        self.slider.setMaximum(50)
        
        self.slider_kp = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_kp.setMaximum(100)
        self.slider_kp.setValue(30)
        self.slider_ki = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_ki.setMaximum(100)
        self.slider_ki.setValue(100)
        self.slider_kd = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider_kd.setMaximum(100)
        self.slider_kd.setValue(10)
        
        # leyout
        self.horizontalLayout.addWidget(self.slider)
        self.horizontalLayout.addWidget(self.plotwidget)
        self.horizontalLayout2.addWidget(QtWidgets.QLabel('Kp'))
        self.horizontalLayout2.addWidget(self.slider_kp)
        self.horizontalLayout2.addWidget(QtWidgets.QLabel('Ki'))
        self.horizontalLayout2.addWidget(self.slider_ki)
        self.horizontalLayout2.addWidget(QtWidgets.QLabel('Kd'))
        self.horizontalLayout2.addWidget(self.slider_kd)

        # timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(30)

    def update_data(self):
        # stop timer
        self.timer.stop()

        # clear
        self.plotwidget.clear()

        # increase data
        self.plot_data['X'] = np.append( self.plot_data['X'][1:], self.plot_data['X'][-1] + 1 )
        self.plot_data['Y'] = np.append( self.plot_data['Y'][1:], self.slider.value() )

        # PID calculation
        kp, ki, kd = self.slider_kp.value() * 0.01, self.slider_ki.value() * 0.01, self.slider_kd.value() * 0.01
        e0, e1, e2 = self.slider.value(), self.plot_data['Y2'][-1], self.plot_data['Y2'][-2]
        move_value = kp * (e0 - e1) + ki * e0 + kd * ( (e0 - e1) - (e1 - e2) )
        self.plot_data['Y2'] = np.append( self.plot_data['Y2'][1:], round(move_value, 3) )

        # set data
        self.plotwidget.addItem(
            pyqtgraph.PlotDataItem(
                x=self.plot_data['X'], 
                y=self.plot_data['Y'], 
                pen=pyqtgraph.mkPen(color='#FF0000', width=1), 
                antialias=True
            )
        )
        
        # set data 2
        self.plotwidget.addItem(
            pyqtgraph.PlotDataItem(
                x=self.plot_data['X'], 
                y=self.plot_data['Y2'], 
                pen=pyqtgraph.mkPen(color='#0000FF', width=1), 
                antialias=True
            )
        )
        
        # start timer
        self.timer.start(30)

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = MainWindow(None)
    mainwindow.show()
    app.exec()

if __name__ == '__main__':
    main()
