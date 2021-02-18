import matplotlib.pyplot as plt
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from notifications import NotificationWindow


class Graph(QWidget):
    def __init__(self, df):
        super().__init__()
        self.counter = 0
        df = df.reset_index()
        df = df.iloc[:, 1:]
        self.selected = []
        self._data = df.loc[:99]
        self.setUI()

    def setUI(self):

        self.openGraphButton = QPushButton("Построить график")

        # выбор гарфика
        self.graphType = QComboBox()
        self.graphType.addItems(['Bar', 'Box', 'Pie', 'Plot'])

        # выбор данных
        self.columnLabel = QLabel("Столбец:")
        self.columnLabel.setAlignment(Qt.AlignRight)
        self.dataColumn = QComboBox()
        itms = self._data.columns
        self.dataColumn.addItems(itms)
        self.dataRangeLabel = QLabel("Первые:")
        self.dataRangeLabel.setAlignment(Qt.AlignRight)
        self.dataRange = QSpinBox()
        self.dataRange.setMinimum(2)

        if len(self._data.index) < 100:
            self.dataRange.setMaximum(int(len(self._data.index)))
        else:
            self.dataRange.setMaximum(100)

        self.columnSettings = QHBoxLayout()
        self.columnSettings.addWidget(self.columnLabel)
        self.columnSettings.addWidget(self.dataColumn)
        self.columnSettings.setAlignment(Qt.AlignLeft)

        self.rangeSettings = QHBoxLayout()
        self.rangeSettings.addWidget(self.dataRangeLabel)
        self.rangeSettings.addWidget(self.dataRange)

        self.dataSettings = QHBoxLayout()
        self.dataSettings.addLayout(self.columnSettings)
        self.dataSettings.addLayout(self.rangeSettings)

        # ВЫБОР СТОЛБЦОВ
        self.dataLabel = QLabel("Данные:")
        self.nonSelectedCols = QListWidget()
        self.nonSelectedCols.addItems(list(self._data._get_numeric_data()))
        self.selectedCols = QListWidget()
        self.buttonAdd = QPushButton(">")
        self.buttonAdd.setFixedWidth(30)
        self.buttonDel = QPushButton("<")
        self.buttonDel.setFixedWidth(30)
        self.buttonLayer = QVBoxLayout()
        self.buttonLayer.addWidget(self.buttonAdd)
        self.buttonLayer.addWidget(self.buttonDel)

        self.columnLayer = QHBoxLayout()
        self.columnLayer.addWidget(self.nonSelectedCols)
        self.columnLayer.addLayout(self.buttonLayer)
        self.columnLayer.addWidget(self.selectedCols)

        # ОСНОВНОЙ СЛОЙ
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.graphType)
        self.mainLayout.addLayout(self.dataSettings)
        self.mainLayout.addWidget(self.dataLabel)
        self.mainLayout.addLayout(self.columnLayer)
        self.mainLayout.addWidget(self.openGraphButton)

        self.newList()
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Параметры графика")
        self.show()

        self.buttonAdd.clicked.connect(self.add)
        self.buttonDel.clicked.connect(self.delete)
        self.openGraphButton.clicked.connect(self.openGraph)
        
        self.dataColumn.activated.connect(self.newList)

    def add(self):
        try:
            self.selectedCols.addItem(
                self.nonSelectedCols.currentItem().text())
            self.selected.append(self.nonSelectedCols.currentItem().text())
            self.nonSelectedCols.takeItem(
                self.nonSelectedCols.currentIndex().row())
        except:
            self.error = NotificationWindow(
                "Необходимо выбрать данные для перемещения")
            self.error.show()

    def delete(self):
        try:
            self.nonSelectedCols.addItem(
                self.selectedCols.currentItem().text())
            self.selected.remove(self.selectedCols.currentItem().text())
            self.selectedCols.takeItem(self.selectedCols.currentIndex().row())
        except:
            self.error = NotificationWindow(
                "Необходимо выбрать данные для перемещения")
            self.error.show()


    def clearLists(self):
        self.selectedCols.clear()
        self.nonSelectedCols.clear()
        self.selected = []

    def newList(self):
        self.clearLists()
        items = [column for column in self._data._get_numeric_data() if column != self.dataColumn.currentText()]
        self.nonSelectedCols.addItems(items)


    def openGraph(self):
        if self.selected != []:
            self.drawGraph(column=self.dataColumn.currentText(), columnList=self.selected,
                           graphType=self.graphType.currentText(), top=self.dataRange.value())

    def drawGraph(self, column, columnList, graphType, top):
        plt.close()
        grouped_df = self._data[:top].groupby([str(column)])
        grouped_df = grouped_df.sum()
        grouped_df = grouped_df.reset_index()

        if graphType == "Bar":
            grouped_df.plot.bar(str(column), y = columnList)
        elif graphType == "Plot":
            grouped_df.plot(x = str(column), y = columnList)
        elif graphType == "Box":
            grouped_df.plot.box(x = str(column), y = columnList)
        else:
            grouped_df[columnList].plot.pie(
                subplots=True, labels=grouped_df[column])
        plt.show()
