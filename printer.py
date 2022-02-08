import os
import sys
import tempfile
from datetime import datetime

from fpdf import FPDF
from num2words import num2words
from pdf2image import convert_from_path
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QShortcut

from UI.Ui_main_ui import Ui_MainWindow


class Main_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()
        self.print_data = []

    def init_UI(self) -> None:
        self.ui.warranty_combo.addItems(
            [
                '1 месяц',
                '3 месяца',
                '6 месяцев',
                '12 месяцев'
            ]
        )
        self.ui.print_button.clicked.connect(self.create_temp_file)
        self.ui.add_button.clicked.connect(self.add_event)
        self.ui.elements_view.itemDoubleClicked.connect(self.edit_event)
        self.ui.edit_button.clicked.connect(self.edit)
        self.del_shortcut = QShortcut(QKeySequence('Shift+Del'), self)
        self.del_shortcut.activated.connect(self.delete_event)
#Добавление товара, а так же его параметров в список
#Введенные параметры проходят проверку при помощи метода "check"
    def add_event(self) -> None:
        if self.check() is True:
            pass
        else:
            return
        item_name = self.ui.name_edit.text()
        item_serial = self.ui.serial_edit.text().upper()
        item_warranty = self.ui.warranty_combo.currentText()
        item_price = self.ui.price_edit.text()
        self.ui.elements_view.addItem(
            f'{item_name}#{item_serial}#{item_warranty}#{item_price}'
        )
        self.print_data.append(
            f'{item_name}#{item_serial}#{item_warranty}#{item_price}'
        )
        self.ui.name_edit.clear()
        self.ui.serial_edit.clear()
        self.ui.warranty_combo.setCurrentIndex(0)
        self.ui.price_edit.clear()
#Функционал для комбинации клавиш редактирования товара
    def edit_event(self) -> None:
        data = self.ui.elements_view.currentItem().text().split('#')
        self.ui.name_edit.setText(data[0])
        self.ui.serial_edit.setText(data[1])
        self.ui.warranty_combo.setCurrentText(data[2])
        self.ui.price_edit.setText(data[3])
        self.ui.add_button.setVisible(False)
        self.ui.edit_button.setVisible(True)
#Само редактирование товара
#Так же проходит проверку при помощи метода "check"
    def edit(self) -> None:
        index = self.ui.elements_view.currentRow()
        item = self.ui.elements_view.currentItem()
        if self.check() is True:
            pass
        else:
            return
        item_name = self.ui.name_edit.text()
        item_serial = self.ui.serial_edit.text().upper()
        item_warranty = self.ui.warranty_combo.currentText()
        item_price = self.ui.price_edit.text()
        item.setText(
            f'{item_name}#{item_serial}#{item_warranty}#{item_price}'
        )
        self.print_data[index] = (
            f'{item_name}#{item_serial}#{item_warranty}#{item_price}'
        )
        self.ui.name_edit.clear()
        self.ui.serial_edit.clear()
        self.ui.warranty_combo.setCurrentIndex(0)
        self.ui.price_edit.clear()
        self.ui.add_button.setVisible(True)
        self.ui.edit_button.setVisible(False)
#Удаление товара
    def delete_event(self) -> None:
        item_index = self.ui.elements_view.currentIndex().row()
        self.print_data.__delitem__(item_index)
        self.ui.elements_view.takeItem(item_index)
#Проверка параметров на их отсутствие, а так же их длинну
#Проверка на длинну, нужна для того что бы не разъехался шаблон и ничего не вылезло за пределы файла
#Так же проверяется цена, что бы в ней присутствовали только числа
    def check(self) -> bool:
        if len(self.ui.name_edit.text()) < 1:
            self.show_error('empty_name')
            return False
        elif len(self.ui.name_edit.text()) > 40:
            self.show_error('long_name')
            return False
        elif len(self.ui.serial_edit.text()) < 1:
            self.show_error('empty_serial')
            return False
        elif len(self.ui.serial_edit.text()) > 30:
            self.show_error('long_serial')
            return False
        elif len(self.ui.price_edit.text()) < 1:
            self.show_error('empty_price')
            return False
        elif self.ui.price_edit.text().isdigit() is False:
            self.show_error('letters_in_price')
            return False
        else:
            return True
#Обработка ошибок
#В методе присутствует словарь с возможными ошибками
    def show_error(self, trouble) -> None:
        pattern = {
            'empty_name': 'Имя не может быть пустым.',
            'long_name': 'Имя не может быть больше 40 символов.',
            'empty_serial': 'Серийный номер не может быть пустым.',
            'long_serial': 'Серийный номер не может быть больше 30 символов.',
            'empty_price': 'Цена не может быть пустой.',
            'letters_in_price': 'Цена может состоять только из цифр.',
            'pdf_opened': 'Сперва нужно закрыть PDF файл'
        }
        error = QtWidgets.QMessageBox()
        error.setIcon(QtWidgets.QMessageBox.Warning)
        error.setWindowIcon(QtGui.QIcon('UI\\attention_icon.png'))
        error.setWindowTitle('Ошибка')
        error.setText(pattern[trouble])
        error.exec_()
#Создание временного файла PDF
#PDF был выбран ввиду того, что изначально программа генерировала док-ты для печати вручную
    def create_temp_file(self) -> None:
        try:
            pdf = FPDF(orientation='P', unit='mm', format='A5')
            pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
            pdf.set_font('DejaVu', '', 14)
            for item in self.print_data:
                data = item.split('#')
                pdf.add_page()
                pdf.cell(40, 10, 'Вирiб:', ln=True)
                pdf.cell(40, 10, f'{data[0]}', ln=True)
                pdf.cell(40, 10, f'Серiйний номер: {data[1]}', ln=True)
                pdf.cell(
                    40, 10,
                    f'Гарантiйний термiн: {data[2][0]} мiс',
                    ln=True
                    )
                pdf.cell(
                    40, 10,
                    f'Дата продажу: {datetime.today().date()}',
                    ln=True
                    )
                pdf.cell(
                    40, 10,
                    f'Продавець:{" " * 25}{"_" * 20} (пiдпис)',
                    ln=True
                    )
                pdf.cell(
                    40, 10,
                    f'Цiна: {data[3]}.00 грн.',
                    ln=True
                    )
                pdf.cell(
                    40, 10,
                    f'{num2words(data[3], lang="uk")} грн. 00 коп.'
                    )
            pdf.output('temp.pdf')
            self.ui.elements_view.clear()
            self.print_file()
            os.remove('temp.pdf')
            self.print_data.clear()
        except PermissionError:
            self.check('pdf_opened')
            return
#Собственно сама печать
    def print_file(self) -> None:
        with open('path.txt') as poppler:
            poppler_path = poppler.readline().strip()
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPaperSize(QPrinter.A5)
        printer.setPageSize(QPrinter.A5)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            with tempfile.TemporaryDirectory() as path:
                images = convert_from_path(
                    'temp.pdf',
                    dpi=600,
                    output_folder=path,
                    poppler_path=f'{poppler_path}'
                    )
                painter = QPainter()
                painter.begin(printer)
                for i, image in enumerate(images):
                    if i > 0:
                        printer.newPage()
                    rect = painter.viewport()
                    qtImage = ImageQt(image)
                    qtImageScaled = qtImage.scaled(
                        rect.size(),
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                        )
                    painter.drawImage(rect, qtImageScaled)
                painter.end()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main_UI()
    main.show()
    sys.exit(app.exec_())
