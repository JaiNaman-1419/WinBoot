from sys import argv, exit
from PyQt5.uic import loadUi
from functools import partial
from PyQt5.QtGui import QIcon
from src.buttons import Buttons
from flash_screen import FlashScreen
from src.usb_drive import DriveProperties
from PyQt5.QtWidgets import QApplication, QDialog, QHeaderView, QStackedWidget


class MainWindow(QDialog):

    def __init__(self, widgets, drive):
        super(MainWindow, self).__init__()

        # Class objects or references
        self.__button = Buttons(widgets, drive)

        # Class attributes
        self.__file_name = None
        self.__file_path = None
        self.__drive_name = None
        self.__drive_path = None

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
        self.add_button.clicked.connect(lambda: self.__button.add_iso_file(self))
        self.drive_button.clicked.connect(lambda: self.__button.select_usb_drive(self))
        self.start_button.clicked.connect(lambda: self.__button.start_flash_button())
        self.refresh_button.clicked.connect(lambda: self.__button.refresh_drive_table(self))
        self.apply_button.clicked.connect(lambda: self.__button.apply_btn_in_drive_frame(self))
        self.remove_file_button.clicked.connect(lambda: self.__button.remove_file_button(self))
        self.cancel_button.clicked.connect(lambda: self.__button.cancel_btn_in_drive_frame(self))
        self.change_drive_button.clicked.connect(lambda: self.__button.change_drive_button(self))
        self.drive_table.itemClicked.connect(partial(self.__button.drive_selected, self))

    def set_drive_table_properties(self):
        self.drive_table.setColumnWidth(0, 240)
        self.drive_table.setColumnWidth(1, 120)
        self.drive_table.setColumnWidth(2, 180)
        self.drive_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)


def set_window_properties(widgets):
    favicon = QIcon("./assets/favicon.png")
    widgets.setWindowIcon(favicon)
    widgets.setFixedSize(1024, 650)
    widgets.setWindowTitle("WinBoot")


if __name__ == '__main__':
    application = QApplication(argv)
    widgets = QStackedWidget()
    drive = DriveProperties()
    main_window = MainWindow(widgets, drive)
    flash_screen = FlashScreen(widgets, drive)
    widgets.addWidget(main_window)
    widgets.addWidget(flash_screen)
    set_window_properties(widgets)
    widgets.show()
    exit(application.exec())
