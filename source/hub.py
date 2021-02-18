import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFileDialog, QHBoxLayout, QLabel, QLineEdit,
                             QListWidget, QPushButton, QVBoxLayout, QWidget)

from table import Reader
from notifications import NotificationWindow


class Hub(QWidget):
    def __init__(self):
        super().__init__()
        self.getUnique()
        self.setUI()

    def setUI(self):

        # открыть файл
        self.openFileButton = QPushButton("...")
        self.openFileButton.setMaximumWidth(50)
        self.sepLabel = QLabel("Разделитель")
        self.sepLabel.setAlignment(Qt.AlignRight)
        self.separator = QLineEdit(",")
        self.separator.setMaximumWidth(100)
        self.openFileLayout = QHBoxLayout()
        self.openFileLayout.addWidget(self.sepLabel)
        self.openFileLayout.addWidget(self.separator)
        self.openFileLayout.addWidget(self.openFileButton)

        # таблица с прошлыми файлами
        self.tableFiles = QListWidget()
        self.tableFiles.addItems(self.getTempFiles())

        # открыть существующий файл
        self.openCurrent = QPushButton("Открыть")
        self.openCurrent.hide()
        self.openCurrentLayout = QHBoxLayout()
        self.openCurrentLayout.addWidget(self.openCurrent)

        # ОСНОВНОЙ СЛОЙ
        self.hubLayout = QVBoxLayout()
        self.hubLayout.addLayout(self.openFileLayout)
        self.hubLayout.addWidget(self.tableFiles)
        self.hubLayout.addLayout(self.openCurrentLayout)

        self.setLayout(self.hubLayout)
        self.setWindowTitle('Главное окно')
        self.resize(600, 700)
        self.show()

        # логика
        self.openFileButton.clicked.connect(self.openFile)
        self.openCurrent.clicked.connect(self.openCurrentFile)
        self.tableFiles.currentRowChanged.connect(self.selectedCahnged)

    def getTempFiles(self):
        try:
            with open("temp.txt", 'r') as f:
                l = [str(el)[:-1] for el in f.readlines()]
        except:
            l = []
        return l

    def selectedCahnged(self):
        self.openCurrent.show()

    def writeTempFiles(self, data=[]):
        with open("temp.txt", "a") as f:
            f.writelines(data[0] + '\n')
            self.tableFiles.addItem(data[0])

    def openFile(self):
        fname = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", ".csv(*.csv)")[0]
        if fname != "":
            self.writeTempFiles([fname])
            self.openTable(fname)

    def openCurrentFile(self):
        try:
            self.openTable(self.tableFiles.currentItem().text())
        except:
            self.tableFiles.takeItem(self.tableFiles.currentIndex().row())
            lfiles = self.getTempFiles()
            lfiles.pop(self.tableFiles.currentIndex().row())

            with open("temp.txt", "w") as f:
                for el in lfiles:
                    f.writelines(el + "\n")

            self.error = NotificationWindow(
                "Файла не существует")
            self.error.show()

    def openTable(self, path):
        sep = self.separator.text()
        df = pd.read_csv(path, sep)
        self.reader = Reader(df)
        self.reader.show()

    def getUnique(self):
        try:
            with open("temp.txt", "r") as f:
                l = [str(el)[:-1] for el in f.readlines()]

            unique = []
            for el in l:
                if el not in unique:
                    unique.append(el)

            with open('temp.txt', "w") as f:
                f.writelines([str(el) + "\n" for el in unique])
        except:
            with open('temp.txt', "w") as f:
                f.write('')
