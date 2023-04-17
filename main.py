from os import getenv
from PyQt5 import QtCore
from sys import argv, exit
from PyQt5.uic import loadUi
from functools import partial
from PyQt5.QtGui import QIcon
from src.buttons import Buttons
from Model.data_model import Data
from flash_screen import FlashScreen
from src.usb_drive import DriveProperties
from PyQt5.QtWidgets import QApplication, QDialog, QHeaderView, QStackedWidget, QMessageBox


class MainWindow(QDialog):

    def __init__(self, widgets_obj, drive_obj, data_obj, flash_obj):
        super(MainWindow, self).__init__()

        # Class objects or references
        self.__data = data_obj
        self.__flash_screen = flash_obj
        self.__button = Buttons(widgets_obj, drive_obj)

        # Loading UI
        loadUi("./ui/main_screen.ui", self)

        # Class Method calls
        self.auto_call_methods()

    def auto_call_methods(self):
        self.button_connectors()
        self.hide_window_attributes()
        self.set_drive_table_properties()

    def hide_window_attributes(self):
        self.drive_frame.hide()
        self.file_name_label.hide()
        self.drive_name_label.hide()
        self.remove_file_button.hide()
        self.change_drive_button.hide()

    def button_connectors(self):
        self.add_button.clicked.connect(lambda: self.__button.add_iso_file(self, self.__data))
        self.drive_button.clicked.connect(lambda: self.__button.select_usb_drive(self))
        self.start_button.clicked.connect(
            lambda: self.__button.start_flash_button(self, self.__data, self.__flash_screen))
        self.refresh_button.clicked.connect(lambda: self.__button.refresh_drive_table(self))
        self.apply_button.clicked.connect(lambda: self.__button.apply_btn_in_drive_frame(self, self.__data))
        self.remove_file_button.clicked.connect(lambda: self.__button.remove_file_button(self, self.__data))
        self.cancel_button.clicked.connect(lambda: self.__button.cancel_btn_in_drive_frame(self, self.__data))
        self.change_drive_button.clicked.connect(lambda: self.__button.change_drive_button(self, self.__data))
        self.drive_table.itemClicked.connect(partial(self.__button.drive_selected, self, self.__data))

    def set_drive_table_properties(self):
        self.drive_table.setColumnWidth(0, 240)
        self.drive_table.setColumnWidth(1, 120)
        self.drive_table.setColumnWidth(2, 180)
        self.drive_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)


def set_window_properties(widget):
    favicon = QIcon("./assets/favicon.png")
    widget.setWindowIcon(favicon)
    widget.setFixedSize(1024, 650)
    widget.setWindowTitle("WinBoot")


if __name__ == '__main__':
    # Instance of QApplication class
    application = QApplication(argv)
    # Instance of QStackedWidget class
    widgets = QStackedWidget()
    # Instance of DriveProperties class
    drive = DriveProperties()
    # Instance of Data class
    data = Data()
    # Instance of FlashScreen class
    flash_screen = FlashScreen(widgets, drive, data)
    # Instance of MainWindow class from main.py
    main_window = MainWindow(widgets, drive, data, flash_screen)
    # Adding main_window widget & flash_screen widget to MAIN STACKED WIDGET
    widgets.addWidget(main_window)
    widgets.addWidget(flash_screen)
    # Setting up main_window properties common for both main_window & flash_screen widget
    set_window_properties(widgets)
    # Starting & ending of app
    widgets.show()

    if getenv("USER") != "root":
        alert = QMessageBox(main_window)
        alert.setStyleSheet("""QMessageBox{
                            color: #FFFFFF; font-size: 20px; background-color: #121212; 
                            border: 2px solid #343434; border-radius: 5px;
                            }""")
        alert.setIcon(QMessageBox.Critical)
        alert.setText("Error!")
        alert.setInformativeText('Run WinBoot as "sudo".\nIt requires Administrator privileges.')
        alert.setWindowTitle("Error occurred")
        alert.setStandardButtons(QMessageBox.Ok)
        alert.buttonClicked.connect(lambda: exit())
        alert.setWindowFlags(alert.windowFlags() & QtCore.Qt.CustomizeWindowHint)
        alert.setStandardButtons(QMessageBox.Ok)
        alert.setDefaultButton(QMessageBox.Ok)
        alert.setEscapeButton(QMessageBox.Ok)
        alert.show()

    exit(application.exec())
# Error in converting wim file to swm.
