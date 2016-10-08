from PySide.QtCore import *
from PySide.QtGui import *

class FileSelectWidget(QWidget):
    fileSelected = Signal(str)

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.field = QLineEdit()
        self.selectFileBtn = QPushButton('...')
        self.layout.addWidget(self.field)
        self.layout.addWidget(self.selectFileBtn)

        self.selectFileBtn.clicked.connect(self.selectFile)

    def selectFile(self):
        filename = QFileDialog().getOpenFileName()[0]
        self.field.setText(filename)
        self.fileSelected.emit(filename)