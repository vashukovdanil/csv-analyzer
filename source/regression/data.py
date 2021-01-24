from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QPushButton,
                             QVBoxLayout, QWidget, QSpinBox, QListWidget)
from modules.notifications import NotificationWindow
import regression.dataprepare as dataprepare
import regression.score as score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class DataChoose(QWidget):
    def __init__(self, df, model, polynom, percentage):
        super().__init__()
        self.data = df
        self.modelType = model
        self.polynom = polynom
        self.percentage = percentage
        self.selected = []
        self.setUI()

    def setUI(self):
        # Выбор зависимой переменной
        self.depLabel = QLabel("Зависимая переменная:")
        self.depCombo = QComboBox()
        self.depCombo.addItems(self.data.columns)

        self.depLayout = QHBoxLayout()
        self.depLayout.addWidget(self.depLabel)
        self.depLayout.addWidget(self.depCombo)

        # Выбор независимых переменных
        self.indLabel = QLabel("Независимые переменные:")
        self.nonSelectedCols = QListWidget()
        items = [column for column in self.data.columns if column != self.depCombo.currentText()]
        self.nonSelectedCols.addItems(items)
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

        # Кнопка "Рассчитать"
        self.scoreButton = QPushButton("Рассчитать")

        # Основной слой
        self.mainL = QVBoxLayout()
        self.mainL.addLayout(self.depLayout)
        self.mainL.addWidget(self.indLabel)
        self.mainL.addLayout(self.columnLayer)
        self.mainL.addWidget(self.scoreButton)

        self.setLayout(self.mainL)
        self.setWindowTitle("Выбор данных")
        self.resize(350, 300)
        self.show()

        self.buttonAdd.clicked.connect(self.add)
        self.buttonDel.clicked.connect(self.delete)

        self.depCombo.activated.connect(self.newList)
        self.scoreButton.clicked.connect(self.score)

    def add(self):
        try:
            self.selectedCols.addItem(self.nonSelectedCols.currentItem().text())
            self.selected.append(self.nonSelectedCols.currentItem().text())
            self.nonSelectedCols.takeItem(self.nonSelectedCols.currentIndex().row())
        except:
            return

    def delete(self):
        try:
            self.nonSelectedCols.addItem(self.selectedCols.currentItem().text())
            self.selected.remove(self.selectedCols.currentItem().text())
            self.selectedCols.takeItem(self.selectedCols.currentIndex().row())
        except:
            return

    def clearLists(self):
        self.selectedCols.clear()
        self.nonSelectedCols.clear()
        self.selected = []

    def newList(self):
        self.clearLists()
        items = [column for column in self.data.columns if column != self.depCombo.currentText()]
        self.nonSelectedCols.addItems(items)

    def extract(self, lst):
        items = []
        for x in range(lst.count()):
            items.append(lst.item(x).text())
        return items

    def score(self):
        y = self.depCombo.currentText()
        selcols = self.extract(self.selectedCols)
        if not selcols:
            return
        new_data = self.data.drop(columns = self.extract(self.nonSelectedCols))
        new_data = dataprepare.fillMissingValues(new_data)
        new_data = dataprepare.categorialToAbsolute(new_data)
        new_data.dropna(inplace=True)
        train, test = train_test_split(new_data, test_size=(1-self.percentage/100))
        y_train = train[y]
        X_train = train.drop(columns = [y])

        y_test = test[y]
        X_test = test.drop(columns = [y])
        try:
            if self.modelType == "Logistic":
                print(new_data.nunique()[self.depCombo.currentText()])
                if new_data.nunique()[self.depCombo.currentText()] != 2:
                    self.notif = NotificationWindow("Зависимая переменная должна быть бинарной")
                    self.notif.show()
                    return
                else:
                    y_pred, r2_model, r2_pred = score.logReg(X_train, y_train, X_test, y_test)
            elif self.modelType == "Linear":
                y_pred, r2_model, r2_pred = score.linear(X_train, y_train, X_test, y_test)
            elif self.modelType == "Polynomial":
                y_pred, r2_model, r2_pred = score.polynomial(X_train, y_train, X_test, y_test, self.polynom)
            else:
                y_pred, r2_model, r2_pred = score.linear(X_train, y_train, X_test, y_test)
        except:
            return
        else:
            self.graph(y_test, y_pred, r2_model, r2_pred)

    def graph(self, y_test, y_pred, r2_model, r2_pred):
        x = [i for i in range(len(y_test))]
        plt.plot(x, y_test, alpha = 0.5)
        plt.plot(x, y_pred, alpha = 0.5, linestyle = "--")
        plt.title(f"R2 модели = {r2_model}\nR2 предсказания = {r2_pred}")
        plt.ylabel(self.depCombo.currentText())
        plt.legend(["Test", "Predicted"])
        plt.show()