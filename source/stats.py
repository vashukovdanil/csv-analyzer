import pandas as pd
from PyQt5.QtWidgets import (QHeaderView, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QWidget)


class Statistics(QWidget):
    def __init__(self, df):
        super().__init__()
        self._data = df.describe()
        self.setUI()

    def setUI(self):
        self.table = QTableWidget()

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.addWidget(self.table)
        self.resize(1200, 500)
        self.setWindowTitle('Статистика')
        self.show()

        self.fillTable()

    def fillTable(self):
        df = self._data

        self.table.setColumnCount(len(list(df.columns)))
        self.table.setRowCount(len(df))

        self.table.setHorizontalHeaderLabels(list(df.columns))
        self.table.setVerticalHeaderLabels(list(df.index))
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for i in range(len(df)):
            for j in range(len(list(df.columns))):
                self.table.setItem(i, j, QTableWidgetItem(str(df.iloc[i, j])))
