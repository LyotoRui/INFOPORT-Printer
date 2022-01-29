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
        self.ui.warranty_combo.addItems(
            [
                '1 месяц',
                '3 месяца',
                '6 месяцев',
                '12 месяцев'
            ]
        )
        self.ui.print_button.clicked.connect(self.print)
        self.ui.add_button.clicked.connect(self.add_event)
        self.ui.elements_view.itemDoubleClicked.connect(self.delete_event)

    def add_event(self):
        item_name = self.ui.name_edit.text()
        if len(item_name) > 0:
            pass
        else:
            self.check('empty_name')
            return
        item_serial = self.ui.serial_edit.text().upper()
        if len(item_serial) > 0:
            pass
        else:
            self.check('empty_serial')
            return
        item_warranty = self.ui.warranty_combo.currentText()
        item_price = self.ui.price_edit.text()
        if len(item_price) < 1:
            self.check('empty_price')
            return
        elif item_price.isdigit() == False:
            self.check('letters_in_price')
            self.ui.price_edit.clear()
            return
        else:
            pass
        self.ui.elements_view.addItem(
            f'{item_name}/{item_serial}/{item_warranty}/{item_price}'
        )
        self.ui.name_edit.clear()
        self.ui.serial_edit.clear()
        self.ui.warranty_combo.setCurrentIndex(0)
        self.ui.price_edit.clear()

    def delete_event(self):
        item_index = self.ui.elements_view.currentIndex().row()
        self.ui.elements_view.takeItem(item_index)

    def check(self, trouble):
        pattern = {
            'empty_name': 'Имя не может быть пустым.',
            'empty_serial': 'Серийный номер не может быть пустым.',
            'empty_price': 'Цена не может быть пустой.',
            'letters_in_price': 'Цена может состоять только из цифр.'
        }
        error = QtWidgets.QMessageBox()
        error.setIcon(QtWidgets.QMessageBox.Warning)
        error.setWindowIcon(QtGui.QIcon('UI\\attention_icon.png'))
        error.setWindowTitle('Ошибка')
        error.setText(pattern[trouble])
        error.exec_()

    def print(self):
        pdf = FPDF(orientation='P', unit='mm', format='A5')
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main_UI()
    main.show()
    sys.exit(app.exec_())
