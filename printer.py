import os
import sys
import tempfile
from datetime import datetime

from fpdf import FPDF
from loguru import logger
from num2words import num2words
from pdf2image import convert_from_path
from PIL.ImageQt import ImageQt
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QShortcut

from exceptions import (
    EmptyNameField,
    EmptyPriceField,
    EmptySerialNumberField,
    PDFAlreadyOpened,
    TooLongName,
    TooLongSerialNumber,
    WrongPriceInput,
)
from models import Product
from UI.Ui_main_ui import Ui_MainWindow

logger.add("debug.log", format="{time} {level} {message}", level="ERROR", compression='zip')


class Main_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()
        self.print_data = []

    def init_UI(self) -> None:
        self.ui.warranty_combo.addItems(
            ["1 месяц", "3 месяца", "6 месяцев", "12 месяцев"]
        )
        self.ui.print_button.clicked.connect(self.create_temp_file)
        self.ui.add_button.clicked.connect(self.add_event)
        self.ui.elements_view.itemDoubleClicked.connect(self.__fill_fields_for_edit)
        self.ui.edit_button.clicked.connect(self.edit)
        self.del_shortcut = QShortcut(QKeySequence("Shift+Del"), self)
        self.del_shortcut.activated.connect(self.delete_event)

    def __clear_ui(self) -> None:
        self.ui.name_edit.clear()
        self.ui.serial_edit.clear()
        self.ui.warranty_combo.setCurrentIndex(0)
        self.ui.price_edit.clear()

    def add_event(self) -> bool:
        '''Добавление товара, а так же его параметров в список
        Введенные параметры проходят проверку при помощи метода "__check"'''
        product = Product(
            name=self.ui.name_edit.text(),
            serial=self.ui.serial_edit.text().upper(),
            warranty=self.ui.warranty_combo.currentText(),
            price=self.ui.price_edit.text(),
        )
        if not self.__check(product=product):
            return False
        self.ui.elements_view.addItem(product.__repr__())
        self.print_data.append(product)
        self.__clear_ui()
        return True

    def __fill_fields_for_edit(self) -> None:
        """Функционал для комбинации клавиш редактирования товара"""
        index = self.ui.elements_view.currentIndex().row()
        item: Product = self.print_data[index]
        self.ui.name_edit.setText(item.name)
        self.ui.serial_edit.setText(item.serial)
        self.ui.warranty_combo.setCurrentText(item.warranty)
        self.ui.price_edit.setText(item.price)
        self.ui.add_button.setVisible(False)
        self.ui.edit_button.setVisible(True)

    def edit(self) -> bool:
        '''Само редактирование товара
        Также проходит проверку при помощи метода "__check"'''
        index = self.ui.elements_view.currentRow()
        item = self.ui.elements_view.currentItem()
        if self.check():
            pass
        else:
            return
        product = Product(
            name=self.ui.name_edit.text(),
            serial=self.ui.serial_edit.text().upper(),
            warranty=self.ui.warranty_combo.currentText(),
            price=self.ui.price_edit.text(),
        )
        if not self.__check(product=product):
            return False
        item.setText(product.__repr__())
        self.print_data[index] = product
        self.__clear_ui()
        self.ui.add_button.setVisible(True)
        self.ui.edit_button.setVisible(False)
        return True

    def delete_event(self) -> None:
        """Удаление товара"""
        item_index = self.ui.elements_view.currentIndex().row()
        self.print_data.__delitem__(item_index)
        self.ui.elements_view.takeItem(item_index)

    def __check(self, product: Product) -> bool:
        """Проверка параметров на их отсутствие, а так же их длинну
        Проверка на длинну, нужна для того что бы не разъехался шаблон и ничего не вылезло за пределы файла
        Так же проверяется цена, что бы в ней присутствовали только числа"""
        try:
            if product.name.__len__() < 1:
                raise EmptyNameField
            elif product.name.__len__() > 40:
                raise TooLongName
            elif product.serial.__len__() < 1:
                raise EmptySerialNumberField
            elif product.serial.__len__() > 40:
                raise TooLongSerialNumber
            elif product.price.__len__() < 0:
                raise EmptyPriceField
            elif not product.price.isnumeric():
                raise WrongPriceInput
        except Exception:
            return False
        return True

    def create_temp_file(self) -> None:
        """Создание временного файла PDF
        PDF был выбран ввиду того, что изначально программа генерировала док-ты для печати вручную"""
        try:
            pdf = FPDF(orientation="P", unit="mm", format="A5")
            pdf.add_font("DejaVu", "", "UI\\DejaVuSansCondensed.ttf", uni=True)
            pdf.set_font("DejaVu", "", 14)
            for product in self.print_data:
                product: Product
                pdf.add_page()
                pdf.cell(40, 10, "Вирiб:", ln=True)
                pdf.cell(40, 10, f"{product.name}", ln=True)
                pdf.cell(40, 10, f"Серiйний номер: {product.serial}", ln=True)
                pdf.cell(
                    40,
                    10,
                    f"Гарантiйний термiн: {product.warranty.split()[0]} мiс",
                    ln=True,
                )
                pdf.cell(40, 10, f"Дата продажу: {datetime.today().date()}", ln=True)
                pdf.cell(40, 10, f'Продавець:{" " * 25}{"_" * 20} (пiдпис)', ln=True)
                pdf.cell(40, 10, f"Цiна: {product.price}.00 грн.", ln=True)
                pdf.cell(40, 10, f'{num2words(product.price, lang="uk")} грн. 00 коп.')
            pdf.output("temp.pdf")
            self.ui.elements_view.clear()
            self.print_file()
            os.remove("temp.pdf")
            self.print_data.clear()
        except PermissionError:
            raise PDFAlreadyOpened
        except Exception as e:
            logger.error(e)

    def print_file(self) -> None:
        """Собственно сама печать"""
        try:
            with open("path.txt") as poppler:
                poppler_path = poppler.readline().strip()
            printer = QPrinter(QPrinter.HighResolution.lower())
            printer.setPaperSize(QPrinter.A5)
            printer.setPageSize(QPrinter.A5)
            dialog = QPrintDialog(printer, self)
            if dialog.exec_() == QPrintDialog.Accepted:
                with tempfile.TemporaryDirectory() as path:
                    images = convert_from_path(
                        "temp.pdf",
                        dpi=600,
                        output_folder=path,
                        poppler_path=f"{poppler_path}",
                    )
                    painter = QPainter()
                    painter.begin(printer)
                    for i, image in enumerate(images):
                        if i > 0:
                            printer.newPage()
                        rect = painter.viewport()
                        qtImage = ImageQt(image)
                        qtImageScaled = qtImage.scaled(
                            rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                        )
                        painter.drawImage(rect, qtImageScaled)
                    painter.end()
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Main_UI()
    main.show()
    sys.exit(app.exec_())
