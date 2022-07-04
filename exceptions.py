from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon

def show_error(message: str) -> None:
    error = QMessageBox()
    error.setIcon(QMessageBox.Warning)
    error.setWindowIcon(QIcon("UI\\attention_icon.png"))
    error.setWindowTitle('Ошибка')
    error.setText(message)
    error.exec_()

class EmptyNameField(Exception):
    def __init__(self) -> None:
        self.message = "Имя не может быть пустым."
        show_error(message=self.message)
        super().__init__()

class TooLongName(Exception):
    def __init__(self) -> None:
        self.message = "Имя не может быть больше 40 символов."
        show_error(message=self.message)
        super().__init__(self.message)

class EmptySerialNumberField(Exception):
    def __init__(self) -> None:
        self.message = "Серийный номер не может быть пустым."
        show_error(message=self.message)
        super().__init__(self.message)

class TooLongSerialNumber(Exception):
    def __init__(self) -> None:
        self.message = "Серийный номер не может быть больше 30 символов."
        show_error(message=self.message)
        super().__init__(self.message)

class EmptyPriceField(Exception):
    def __init__(self) -> None:
        self.message = "Цена не может быть пустой."
        show_error(message=self.message)
        super().__init__(self.message)

class WrongPriceInput(Exception):
    def __init__(self) -> None:
        self.message = "Цена может состоять только из цифр."
        show_error(message=self.message)
        super().__init__(self.message)

class PDFAlreadyOpened(Exception):
    def __init__(self) -> None:
        self.message = "Сперва нужно закрыть PDF файл"
        show_error(message=self.message)
        super().__init__(self.message)