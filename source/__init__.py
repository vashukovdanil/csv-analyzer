import sys

from PyQt5.QtWidgets import QApplication

from hub import Hub

if __name__ == "__main__":
    app = QApplication(sys.argv)

    hub = Hub()
    hub.show()

    sys.exit(app.exec_())