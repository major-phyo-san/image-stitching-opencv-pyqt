import sys
import os.path
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QAction, qApp, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl

from Backend import ImageStitcher


class AppLayout(QMainWindow):

    appTitle = "Image Stitching App with OpenCV"
    appMarginLeft = 100
    appMarginTop = 100
    appWidth = 640
    appHeight = 480

    fileNames = None
    imageStitcher = ImageStitcher()
    ## imstcher = ImageStitcher()
    status = None
    firstFileName = None
    saveDir = None

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
        vBoxLayout = QHBoxLayout()
        self.centralWidget.setLayout(vBoxLayout)
        self.setCentralWidget(self.centralWidget)

        self.stitchBtn = QPushButton("Stitch Images")
        self.stitchBtn.clicked.connect(self.stitchImages)
        vBoxLayout.addWidget(self.stitchBtn)

        cropBtn = QPushButton("Smooth stitched image")
        cropBtn.clicked.connect(self.cropStitchedImage)
        vBoxLayout.addWidget(cropBtn)

        saveOutputImageBtn = QPushButton("Save Output Image")
        saveOutputImageBtn.clicked.connect(self.saveOutputImage)
        vBoxLayout.addWidget(saveOutputImageBtn)


    def openFileDialog(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        fileDialog.setViewMode(QFileDialog.List)
        filter = "Images *.jpg; *.png; *.bmp"
        fileDialogTitle = "Load Images"
        initialDir = "c:\\users"
        self.fileNames, _filter = fileDialog.getOpenFileNames(self.centralWidget, fileDialogTitle, initialDir, filter)
        self.firstFileName = None
        if not self.fileNames:
            print("No files")
        else:
            print(str(len(self.fileNames))+ " files selected")
            self.imageStitcher.load_images(self.fileNames)
            self.firstFileName = QUrl.fromLocalFile(self.fileNames[0]).fileName()
            self.saveDir = os.path.dirname(self.fileNames[0])            
            print("First file name "+self.firstFileName)
            print("Path " + os.path.dirname(self.fileNames[0]))

    def stitchImages(self):
        if not self.fileNames:
            print("No files to stitch")
        else:
            self.status = self.imageStitcher.stitch_images()

    def cropStitchedImage(self):
        self.imageStitcher.smooth_stitched_image()

    def saveOutputImage(self):
        self.imageStitcher.save_output_image(self.firstFileName, self.saveDir)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AppLayout()
    ex.show()
    sys.exit(app.exec_())
