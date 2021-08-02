from sys import argv, exit
from PyQt5.uic import loadUi
from src.format import Format
from src.buttons import Buttons
from PyQt5.QtWidgets import QApplication, QDialog  # , QStackedWidget


class MainWindow(QDialog):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Class objects or references
        self.__format = Format()
        self.__button = Buttons(self)

        # Class attributes
        self.__file_name = None
        self.__file_path = None
        self.__drive_name = None
        self.__drive_path = None

        # Loading UI
        loadUi("./ui/main_screen.ui", self)

        # Class Method calls
        self.hide_window_attributes()

    def hide_window_attributes(self):
        self.drive_frame.hide()
        self.file_name_label.hide()
        self.drive_name_label.hide()

    def button_connectors(self):
        self.add_button.clicked.connect(self.__button.add_iso_file)
        self.drive_button.clicked.connect(self.__button.select_usb_drive)
        self.start_button.clicked.connect(self.__button.start_flash_button)
        self.refresh_button.clicked.connect(self.__button.refresh_drive_table)
        self.apply_button.clicked.connect(self.__button.apply_btn_in_drive_frame)
        self.cancel_button.clicked.connect(self.__button.cancel_btn_in_drive_frame)

    def change_addfile_and_filenamelabel(self):
        self.add_button.hide()
        self.__file_name = self.__button.get_file_name()
        self.file_name_label.setText(self.__format.format_string_label(self.__file_name))

    def change_drivebtn_and_drivelabel(self):
        self.drive_button.hide()
        self.__drive_name = self.__button.get_drive_name()
        self.drive_name_label.setText(self.__format.format_string_label(self.__drive_name))


if __name__ == '__main__':
    application = QApplication(argv)
    # widgets = QStackedWidget()
    main_window = MainWindow()
    main_window.show()
    exit(application.exec())
