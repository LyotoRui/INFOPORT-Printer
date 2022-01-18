from PyQt5 import QtCore, QtGui, QtWidgets
from fpdf import FPDF
from UI.Ui_main_ui import Ui_MainWindow
import sys


class Main_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

    def init_UI(self):
        self.ui.print_button.clicked.connect(self.print)

    def add_event(self):
        pass
    
    def print(self):
        pdf = FPDF()
        pdf.add_page(
            orientation='L',
            format='A5',
            same=False
        )
        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main_UI()
    main.show()
    sys.exit(app.exec_())
