from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class NotificationWindow(QWidget):
    def __init__(self, text):
        super().__init__()
        self.setUI(text)

    def setUI(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        okButton = QPushButton("OK")

        mainL = QVBoxLayout()
        mainL.addWidget(label)
        mainL.addWidget(okButton)

        self.setLayout(mainL)
        self.setWindowTitle("Уведомление")
        self.resize(350, 100)
        self.show()

        okButton.clicked.connect(self.close)
