# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Projects\Bill Printer\INFOPORT-Printer\UI\main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(670, 160)
        MainWindow.setMinimumSize(QtCore.QSize(670, 160))
        MainWindow.setMaximumSize(QtCore.QSize(670, 160))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.name_group = QtWidgets.QGroupBox(self.centralwidget)
        self.name_group.setGeometry(QtCore.QRect(0, 0, 401, 51))
        self.name_group.setObjectName("name_group")
        self.name_edit = QtWidgets.QLineEdit(self.name_group)
        self.name_edit.setGeometry(QtCore.QRect(10, 20, 381, 21))
        self.name_edit.setObjectName("name_edit")
        self.serial_group = QtWidgets.QGroupBox(self.centralwidget)
        self.serial_group.setGeometry(QtCore.QRect(0, 50, 401, 51))
        self.serial_group.setObjectName("serial_group")
        self.serial_edit = QtWidgets.QLineEdit(self.serial_group)
        self.serial_edit.setGeometry(QtCore.QRect(10, 20, 381, 21))
        self.serial_edit.setObjectName("serial_edit")
        self.warranty_group = QtWidgets.QGroupBox(self.centralwidget)
        self.warranty_group.setGeometry(QtCore.QRect(0, 100, 161, 51))
        self.warranty_group.setObjectName("warranty_group")
        self.warranty_combo = QtWidgets.QComboBox(self.warranty_group)
        self.warranty_combo.setGeometry(QtCore.QRect(10, 20, 141, 21))
        self.warranty_combo.setObjectName("warranty_combo")
        self.price_group = QtWidgets.QGroupBox(self.centralwidget)
        self.price_group.setGeometry(QtCore.QRect(160, 100, 120, 51))
        self.price_group.setObjectName("price_group")
        self.price_edit = QtWidgets.QLineEdit(self.price_group)
        self.price_edit.setGeometry(QtCore.QRect(10, 20, 71, 21))
        self.price_edit.setObjectName("price_edit")
        self.label = QtWidgets.QLabel(self.price_group)
        self.label.setGeometry(QtCore.QRect(90, 20, 21, 20))
        self.label.setObjectName("label")
        self.add_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_button.setGeometry(QtCore.QRect(290, 110, 51, 41))
        self.add_button.setObjectName("add_button")
        self.add_button.setIcon(QtGui.QIcon('UI\\add_icon.png'))
        self.print_button = QtWidgets.QPushButton(self.centralwidget)
        self.print_button.setGeometry(QtCore.QRect(350, 110, 51, 41))
        self.print_button.setObjectName("print_button")
        self.print_button.setIcon(QtGui.QIcon('UI\print_icon.png'))
        self.elements_view = QtWidgets.QListView(self.centralwidget)
        self.elements_view.setGeometry(QtCore.QRect(410, 10, 256, 141))
        self.elements_view.setObjectName("elements_view")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Печать талонов на отправку"))
        self.name_group.setTitle(_translate("MainWindow", "Название"))
        self.serial_group.setTitle(_translate("MainWindow", "Серийный номер"))
        self.warranty_group.setTitle(_translate("MainWindow", "Гарантия"))
        self.price_group.setTitle(_translate("MainWindow", "Цена"))
        self.label.setText(_translate("MainWindow", "грн."))
        self.add_button.setText(_translate("MainWindow", ""))
        self.print_button.setText(_translate("MainWindow", ""))