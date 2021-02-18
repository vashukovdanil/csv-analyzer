from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QPushButton,
                             QVBoxLayout, QWidget, QSpinBox)
from data import DataChoose


class ChooseModel(QWidget):
    def __init__(self, df):
        super().__init__()
        self.data = df
        self.setUI()

    def setUI(self):
        # Тип модели
        self.modelLabel = QLabel("Модель регрессии:")
        self.modelCombo = QComboBox()
        self.modelCombo.addItems(["Linear", "Logistic", "Polynomial", "Ridge"])

        self.modelLayout = QHBoxLayout()
        self.modelLayout.addWidget(self.modelLabel)
        self.modelLayout.addWidget(self.modelCombo)

        # Выбор полинома
        self.polynomLabel = QLabel("Полином:")
        self.polynomCount = QSpinBox()
        self.polynomCount.setMinimum(1)

        self.polynomLayout = QHBoxLayout()
        self.polynomLayout.addWidget(self.polynomLabel)
        self.polynomLayout.addWidget(self.polynomCount)

        if self.modelCombo.currentText() != "Polynomial":
            self.togglePolynomLayout(False)

        # Выбор доли обучающей выборки
        self.trainLabel = QLabel("Процент обучающей выборки")
        self.trainPercentage = QSpinBox()
        self.trainPercentage.setMaximum(99)
        self.trainPercentage.setMinimum(1)
        self.trainPercentageLabel = QLabel("%")

        self.trainLayout = QHBoxLayout()
        self.trainLayout.addWidget(self.trainLabel)
        self.trainLayout.addWidget(self.trainPercentage)
        self.trainLayout.addWidget(self.trainPercentageLabel)

        # Кнопка "Далее"
        self.nextButton = QPushButton("Далее")
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.nextButton)

        # Основной слой
        self.mainL = QVBoxLayout()
        self.mainL.addLayout(self.modelLayout)
        self.mainL.addLayout(self.polynomLayout)
        self.mainL.addLayout(self.trainLayout)
        self.mainL.addLayout(self.buttonLayout)

        self.setLayout(self.mainL)
        self.setWindowTitle("Выбор модели регрессии")
        self.resize(350, 150)
        self.show()

        self.modelCombo.activated.connect(self.onChangeModel)
        self.nextButton.clicked.connect(self.nextStep)


    def onChangeModel(self):
        if self.modelCombo.currentText() == "Polynomial":
            self.togglePolynomLayout()
        else:
            self.togglePolynomLayout(False)

    def togglePolynomLayout(self, show = True):
        if show == True:
            self.polynomLabel.setEnabled(True)
            self.polynomCount.setEnabled(True)
        else:
            self.polynomLabel.setEnabled(False)
            self.polynomCount.setEnabled(False)

    def nextStep(self):
        self.dataChoose = DataChoose(self.data, self.modelCombo.currentText(), self.polynomCount.value(), self.trainPercentage.value())
        self.dataChoose.show()
        self.close()