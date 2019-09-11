import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QAction, qApp, QFileDialog, QLabel, QPushButton
from PyQt5.QtCore import QStringListModel
from PyQt5.QtGui import QIcon
from imageProcessor import ImageStitcher


class App(QMainWindow):

    appTitle = "Image Stitching with OpenCV"
    appMarginLeft = 100
    appMarginTop = 100
    appWidth = 640
    appHeight = 480

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.appTitle)
        self.setGeometry(self.appMarginLeft, self.appMarginTop, self.appWidth, self.appHeight)

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Z')
        exitAct.setStatusTip('Exit Appliction')
        exitAct.triggered.connect(qApp.quit)

        loadImages = QAction('&Open', self)
        loadImages.setStatusTip('Open Images')
        loadImages.triggered.connect(self.openFileDialog)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(loadImages)
        fileMenu.addAction(exitAct)

        self.addWidgets()

    def addWidgets(self):
        self.statusBar().showMessage('Ready')
        self.centralWidget = QWidget(self)
        vBoxLayout = QVBoxLayout()
        self.centralWidget.setLayout(vBoxLayout)
        self.setCentralWidget(self.centralWidget)

        label = QLabel("Hello World")
        vBoxLayout.addWidget(label)

    def openFileDialog(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        fileDialog.setViewMode(QFileDialog.List)
        filter = "Images *.jpg; *.png; *.bmp"
        fileDialogTitle = "Load Images"
        initialDir = "c:\\users"
        self.fileNames, _filter = fileDialog.getOpenFileNames(self.centralWidget, fileDialogTitle, initialDir, filter)
        if not self.fileNames:
            print("No files")
        else:
            print(len(self.fileNames))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())