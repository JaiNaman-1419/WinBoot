from sys import argv, exit
from PyQt5.uic import loadUi
from src.buttons import Buttons
from src.usb_drive import DriveProperties
from PyQt5.QtWidgets import QApplication, QDialog, QHeaderView  # , QStackedWidget


class MainWindow(QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Class objects or references
        self.__drive = DriveProperties()
        self.__button = Buttons(self, self.__drive)

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
        self.add_button.clicked.connect(self.__button.add_iso_file)
        self.drive_button.clicked.connect(self.__button.select_usb_drive)
        self.start_button.clicked.connect(self.__button.start_flash_button)
        self.refresh_button.clicked.connect(self.__button.refresh_drive_table)
        self.apply_button.clicked.connect(self.__button.apply_btn_in_drive_frame)
        self.remove_file_button.clicked.connect(self.__button.remove_file_button)
        self.cancel_button.clicked.connect(self.__button.cancel_btn_in_drive_frame)
        self.change_drive_button.clicked.connect(self.__button.change_drive_button)
        self.drive_table.itemClicked.connect(self.__button.drive_selected)

    def set_drive_table_properties(self):
        self.drive_table.setColumnWidth(0, 240)
        self.drive_table.setColumnWidth(1, 120)
        self.drive_table.setColumnWidth(2, 180)
        self.drive_table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)


if __name__ == '__main__':
    application = QApplication(argv)
    # widgets = QStackedWidget()
    main_window = MainWindow()
    main_window.show()
    exit(application.exec())
