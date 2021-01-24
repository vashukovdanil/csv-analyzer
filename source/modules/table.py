import os
from datetime import datetime

import pandas as pd
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QHeaderView, QLabel,
                             QLineEdit, QProgressBar, QPushButton,
                             QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QWidget)

from modules.graphs import Graph
from modules.notifications import NotificationWindow
from modules.stats import Statistics
from regression.model import ChooseModel


class Reader(QWidget):
    def __init__(self, df):
        super().__init__()
        self.dataFrame = df

        now = datetime.now()
        self.month = now.strftime("%m")
        self.day = now.strftime("%d")
        self.time = now.strftime("%H_%M_%S")

        try:
            if self.dataFrame.iloc[1, 0] == (self.dataFrame.iloc[0, 0] + 1):
                self.dataFrame = self.dataFrame.iloc[:, 1:]
        except:
            self.dataFrame = self.dataFrame

        self.dataSet = None
        self.counter = 0
        self.temp = None
        self.operatorStatus = None
        self.setUI()

    def setUI(self):

        # Кнопки инструментов
        self.exportToExcel = QPushButton()
        self.exportToCSV = QPushButton()
        self.exportToExcel.setIcon(QtGui.QIcon('icons/excel.png'))
        self.exportToCSV.setIcon(QtGui.QIcon('icons/csv.png'))
        self.exportToExcel.setFixedSize(30, 30)
        self.exportToCSV.setFixedSize(30, 30)
        self.regressionButton = QPushButton()
        self.regressionButton.setIcon(QtGui.QIcon('icons/regression.png'))

        self.toolsLayout = QHBoxLayout()
        self.toolsLayout.addWidget(self.exportToExcel)
        self.toolsLayout.addWidget(self.exportToCSV)
        self.toolsLayout.addWidget(self.regressionButton)
        self.toolsLayout.setAlignment(Qt.AlignLeft)

        # элементы
        self.table = QTableWidget()
        self.searchLine = QLineEdit()
        self.progressBar = QProgressBar()
        self.progressBar.hide()

        # быстрые статистики
        self.countLabel = QLabel()
        self.countLabel.hide()
        self.unique = QLabel()
        self.unique.hide()
        self.avg = QLabel()
        self.avg.hide()

        # быстрые статистики (слой)
        self.stat = QHBoxLayout()
        self.stat.setAlignment(Qt.AlignRight)
        self.stat.addWidget(self.countLabel)
        self.stat.addWidget(self.unique)
        self.stat.addWidget(self.avg)

        # кнопка поиска
        self.buttonSearch = QPushButton()
        self.buttonSearch.setIcon(QtGui.QIcon('icons/loupe.png'))

        # кнопка сброса
        self.buttonRefresh = QPushButton()
        self.buttonRefresh.setIcon(QtGui.QIcon('icons/clear.png'))

        # кнопка графиков
        self.buttonGraph = QPushButton()
        self.buttonGraph.setIcon(QtGui.QIcon('icons/chart.png'))

        # кнопка статистики
        self.buttonStatistic = QPushButton()
        self.buttonStatistic.setIcon(QtGui.QIcon('icons/sum.png'))

        self.comboSearch = QComboBox()
        self.comboSearch.addItems(list(self.dataFrame))

        self.comboOperators = QComboBox()
        self.comboOperators.addItems(['=', '<', '>'])
        self.comboOperators.hide()

        # поиск
        self.searchLayout = QHBoxLayout()
        self.searchLayout.addWidget(self.searchLine)
        self.searchLayout.addWidget(self.comboOperators)
        self.searchLayout.addWidget(self.comboSearch)
        self.searchLayout.addWidget(self.buttonSearch)
        self.searchLayout.addWidget(self.buttonRefresh)
        self.searchLayout.addWidget(self.buttonGraph)
        self.searchLayout.addWidget(self.buttonStatistic)

        # основной слой
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addLayout(self.toolsLayout)
        self.mainLayout.addLayout(self.searchLayout)
        self.mainLayout.addWidget(self.table)
        self.mainLayout.addWidget(self.progressBar)
        self.mainLayout.addLayout(self.stat)

        self.setLayout(self.mainLayout)

        self.resize(1200, 800)
        self.setWindowTitle('Таблица')
        self.show()

        self.fillTable()

        # логика кнопок
        self.buttonSearch.clicked.connect(self.search)
        self.buttonRefresh.clicked.connect(self.refresh)
        self.buttonStatistic.clicked.connect(self.openStatistics)
        self.buttonGraph.clicked.connect(self.graphOpen)
        self.exportToExcel.clicked.connect(self.exportExcel)
        self.exportToCSV.clicked.connect(self.exportCSV)
        self.regressionButton.clicked.connect(self.openRegression)

        self.table.itemSelectionChanged.connect(self.selectionChanged)

        # при изменении комбо боксов
        self.comboSearch.activated.connect(self.onChangeColumn)
        self.comboOperators.activated.connect(self.onChangeOperator)

        self.table.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)

    def exportExcel(self):
        if not os.path.exists("export/"):
            os.makedirs("export/")
        self.dataSet.to_excel(
            f"export/{self.day}_{self.month}_{self.time}.xlsx", index=False)

        self.error = NotificationWindow(
            "Файл успешно экспортирован")
        self.error.show()

    def exportCSV(self):
        if not os.path.exists("export/"):
            os.makedirs("export/")
        self.dataSet.to_csv(
            f"export/{self.day}_{self.month}_{self.time}.csv", index=False)
        self.error = NotificationWindow(
            "Файл успешно экспортирован")
        self.error.show()

    def selectionChanged(self):
        temp = self.dataSet.iloc[:, self.table.currentColumn()]
        temp = temp.describe()
        try:
            self.avg.hide()
            self.unique.setText("Уникальных значений: " +
                                str(temp.loc["unique"]))
        except:
            self.avg.show()
            self.avg.setText("AVG: " + str(round(float(temp.loc["mean"]), 3)))
            self.unique.setText("Значений: " + str(int(temp.loc["count"])))

        self.unique.show()

    def onHeaderClicked(self, logicalIndex):
        col = list(self.dataFrame.columns)
        self.fillTable(qwery=self.searchLine.text(), column=self.comboSearch.currentText(
        ), operator=self.operatorStatus, orderby=col[logicalIndex])

    def onChangeColumn(self):
        numeric = self.dataFrame._get_numeric_data()
        if self.comboSearch.currentText() in numeric.columns:
            self.comboOperators.show()
            self.operatorStatus = self.comboOperators.currentText()
        else:
            self.comboOperators.hide()
            self.buttonGraph.show()
            self.operatorStatus = None

    def onChangeOperator(self):
        self.operatorStatus = self.comboOperators.currentText()

    def graphOpen(self):
        self.graph = Graph(df=self.dataSet)
        self.graph.show()

    def search(self):
        if list(self.searchLine.text()):
            self.fillTable(qwery=self.searchLine.text(
            ), column=self.comboSearch.currentText(), operator=self.operatorStatus)

    def refresh(self):
        self.searchLine.setText("")
        self.fillTable()

    def openStatistics(self):
        self.statistic = Statistics(self.dataSet)
        self.statistic.show()
    
    def openRegression(self):
        self.reg = ChooseModel(self.dataSet)
        self.reg.show()

    def getDataSet(self, df, qwery=None, column=None, operator=None):
        # поиск
        if not str(qwery) or qwery == None:
            return df
        else:
            print(qwery)
            if operator == "=":
                df = df[df[column] == float(qwery)]
            elif operator == "<":
                df = df[df[column] < float(qwery)]
            elif operator == ">":
                df = df[df[column] > float(qwery)]
            else:
                df = df[df[column].astype(str).str.contains(qwery, na=False)]
        return df

    def fillTable(self, qwery=None, column=None, operator=None, orderby=None):

        df = self.getDataSet(df=self.dataFrame, qwery=qwery,
                             column=column, operator=operator)

        self.progressBar.setRange(0, len(df))
        self.progressBar.show()

        self.countLabel.hide()
        self.unique.hide()
        self.avg.hide()

        self.countLabel.setText("Строк: " + str(len(df)))

        self.table.setColumnCount(len(list(df.columns)))
        self.table.setRowCount(len(df))
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.setHorizontalHeaderLabels(list(df.columns))

        if orderby != None:
            if self.temp == orderby:
                if self.counter == 0:
                    df = df.sort_values(orderby)
                    self.counter = 1
                else:
                    df = df.sort_values(orderby, ascending=False)
                    self.counter = 0
            else:
                df = df.sort_values(orderby)
                self.counter = 1

            self.temp = orderby

        for i in range(len(df)):
            self.progressBar.setValue(i)
            for j in range(len(list(df.columns))):
                self.table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))

        self.progressBar.hide()
        self.countLabel.show()
        self.dataSet = pd.DataFrame(df)
