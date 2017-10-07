import sys
from functools import partial
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QStyleFactory, QLineEdit, QLabel, QFileDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
 
class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'METRoWin - Rowan University'
        self.left = 50
        self.top = 50
        self.width = 640
        self.height = 480
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #Create text boxes for file selection
        boxesLeft = 25
        boxesTop = 25
        textBoxWidth = 300
        textBoxHeight = 30
        textBoxVSpacing = 15
        textBoxHSpacing = 105
        
        self.label_forecast = QLabel(self)
        self.label_forecast.setText('Forecast:')
        self.label_forecast.move(boxesLeft, boxesTop)
        self.label_forecast.setFont(QFont('SansSerif', 11))
        self.textBox_forecast = QLineEdit(self)
        self.textBox_forecast.move(boxesLeft + textBoxHSpacing, boxesTop)
        self.textBox_forecast.resize(textBoxWidth, textBoxHeight)
        self.textBox_forecast.setReadOnly(True)
        
        self.label_observation = QLabel(self)
        self.label_observation.setText('Observation:')
        self.label_observation.move(boxesLeft, boxesTop + textBoxHeight + textBoxVSpacing)
        self.label_observation.resize(textBoxWidth, textBoxHeight)
        self.label_observation.setFont(QFont('SansSerif', 11))
        self.textBox_observation = QLineEdit(self)
        self.textBox_observation.move(boxesLeft + textBoxHSpacing, boxesTop + textBoxHeight + textBoxVSpacing)
        self.textBox_observation.resize(textBoxWidth, textBoxHeight)
        self.textBox_observation.setReadOnly(True)

        self.label_config = QLabel(self)
        self.label_config.setText('Station Config:')
        self.label_config.move(boxesLeft, boxesTop + 2*(textBoxHeight + textBoxVSpacing))
        self.label_config.resize(textBoxWidth, textBoxHeight)
        self.label_config.setFont(QFont('SansSerif', 11))
        self.textBox_config = QLineEdit(self)
        self.textBox_config.move(boxesLeft + textBoxHSpacing, boxesTop + 2*(textBoxHeight + textBoxVSpacing))
        self.textBox_config.resize(textBoxWidth, textBoxHeight)
        self.textBox_config.setReadOnly(True)

        #Create buttons
        btnRun = QPushButton('Run', self)
        btnRun.setToolTip('Run METRoWin with current data')
        btnRun.move(self.width-120, self.height-50)
        btnRun.clicked.connect(self.on_click_btnRun)

        btnLeft = boxesLeft + textBoxHSpacing + textBoxWidth + 10
        btnForecast = QPushButton('Browse...', self)
        btnForecast.move(btnLeft, boxesTop)
        btnForecast.clicked.connect(partial(self.openFileNameDialog, self.textBox_forecast))

        btnObservation = QPushButton('Browse...', self)
        btnObservation.move(btnLeft, boxesTop + textBoxHeight + textBoxVSpacing)
        btnObservation.clicked.connect(partial(self.openFileNameDialog, self.textBox_observation))

        btnConfig = QPushButton('Browse...', self)
        btnConfig.move(btnLeft, boxesTop + 2*(textBoxHeight + textBoxVSpacing))
        btnConfig.clicked.connect(partial(self.openFileNameDialog, self.textBox_config))
        self.show()

    @pyqtSlot()
    def on_click_btnRun(self):
        print('METRo is running')

    # Saves selected filename and displays it in a QLineEdit
    @pyqtSlot()
    def openFileNameDialog(self, textBox):    
        filename = QFileDialog.getOpenFileName(self, 'Open file', 'C:/')
        textBox.setText(filename[0])
 
if __name__ == '__main__':
    QApplication.setStyle('Fusion')
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
