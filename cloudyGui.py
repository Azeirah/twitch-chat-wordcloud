#!/usr/bin/python
# python stdlib
import sys
import time

# qt imports
from PySide.QtCore import *
from PySide.QtGui import *
from PIL.ImageQt import ImageQt

# custom qt widgets
from fileSelectWidget import FileSelectWidget

# business logic
from confy import Confy
from cloudy import Cloudy

config = Confy('config.json')

class CloudyWorker(QObject):
    imgready = Signal(object)

    def __init__(self):
        super().__init__()

    def process(self):
        self.cloudy = Cloudy(config)
        self.stopped = False

        while not self.stopped:
            img = self.cloudy.generateImage()
            if img is not None:
                self.imgready.emit(img)
            time.sleep(0.05)

    def stop(self):
        self.stopped = True


class CloudyGui(QFrame):
    def __init__(self):
        super().__init__()

        self.refreshRate = config.get('refreshRate', 5.0)

        self.setWindowTitle('Twitch cloud')

        self.vlayout = QVBoxLayout(self)

        self.config_layout = QFormLayout()
        self.vlayout.addLayout(self.config_layout)

        self.nicknameLbl    = QLabel('Twitch chat username')
        self.oauthLbl       = QLabel('<a href="http://www.twitchapps.com/tmi/">Oauth</a>')
        self.oauthLbl.setOpenExternalLinks(True)
        self.channelLbl     = QLabel('Channel name')
        self.limitLbl       = QLabel('Maximum text length')
        self.imageLbl       = QLabel('Image mask')
        self.refreshRateLbl = QLabel('Refresh rate (in s)')

        self.nicknameField    = QLineEdit(self)
        self.oauthField       = QLineEdit(self)
        self.channelField     = QLineEdit(self)
        self.limitField       = QLineEdit(self)
        self.imageDirSelect   = FileSelectWidget()
        self.refreshRateField = QLineEdit(self)
        
        self.nicknameField.setText(config.get('nickname', ''))
        self.oauthField.setText(config.get('oauth', ''))
        self.channelField.setText(config.get('channel', ''))
        self.limitField.setText(str(config.get('limit', '1500')))
        self.imageDirSelect.field.setText(config.get('image', ''))
        self.refreshRateField.setText(str(config.get('refreshRate', '5.0')))

        self.config_layout.addRow(self.nicknameLbl,    self.nicknameField)
        self.config_layout.addRow(self.oauthLbl,       self.oauthField)
        self.config_layout.addRow(self.channelLbl,     self.channelField)
        self.config_layout.addRow(self.limitLbl,       self.limitField)
        self.config_layout.addRow(self.imageLbl,       self.imageDirSelect)
        self.config_layout.addRow(self.refreshRateLbl, self.refreshRateField)

        self.nicknameField.textChanged.connect(self.onNicknameChange)
        self.oauthField.textChanged.connect   (self.onOauthChange)
        self.channelField.textChanged.connect (self.onChannelChange)
        self.limitField.textChanged.connect   (self.onLimitChange)
        self.imageDirSelect.fileSelected.connect(self.selectImageFile)
        self.refreshRateField.textChanged.connect(self.onRefreshRateChange)

        self.startButton = QPushButton('Start')
        self.startButton.clicked.connect(self.startToggle)
        self.vlayout.addWidget(self.startButton)

        self.cloudImage = QLabel()
        self.vlayout.addWidget(self.cloudImage)

        self.init()
        self.show()

    def init(self):
        # debounce the rendering
        self.lastTime = 0

    def selectImageFile(self, file):
        config['image'] = file

    def imgready(self, img):
        if time.time() - self.refreshRate >= self.lastTime:
            image = QImage(ImageQt(img))
            pix = QPixmap.fromImage(image)
            self.cloudImage.setPixmap(pix)
            self.cloudImage.show()
            self.lastTime = time.time()

    def startToggle(self):
        if self.startButton.text() == 'Start':
            # start now
            self.cloudThread = QThread()
            self.cloudWorker = CloudyWorker()
            self.cloudWorker.moveToThread(self.cloudThread)
            self.cloudThread.started.connect(self.cloudWorker.process)
            self.cloudThread.start()

            self.cloudWorker.imgready.connect(self.imgready)
            self.startButton.setText('Stop')
        else:
            # stop now
            self.startButton.setText('Start')
            self.cloudWorker.stop()

    def onNicknameChange(self, value):
        config['nickname'] = value

    def onOauthChange(self, value):
        config['oauth'] = value

    def onChannelChange(self, value):
        config['channel'] = value

    def onLimitChange(self, value):
        config['limit'] = int(value)

    def onRefreshRateChange(self, value):
        config['refreshRate'] = float(value)


# Create a Qt application
app = QApplication(sys.argv)
ui = CloudyGui()
# Create a Label and show it
# Enter Qt application main loop
app.exec_()
config.save()
sys.exit()