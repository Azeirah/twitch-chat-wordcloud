from PySide.QtCore import *
from PySide.QtGui import *

class DirectorySelectWidget(QWidget):
    directorySelected = Signal(str)

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.field = QLineEdit()
        self.selectDirBtn = QPushButton('...')
        self.layout.addWidget(self.field)
        self.layout.addWidget(self.selectDirBtn)

        self.selectDirBtn.clicked.connect(self.selectDirectory)

    def selectDirectory(self):
        dirname = QFileDialog().getExistingDirectory()
        self.field.setText(dirname)
        self.directorySelected.emit(dirname)