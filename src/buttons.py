from src.format import Format
from PyQt5.QtWidgets import QFileDialog


class Buttons:

    # Buttons of Main Window Dialog/
    # TODO define working of buttons in Main Window Dialog.

    def __init__(self, window):
        # Class Attributes
        self.__file_name = None
        self.__file_path = None
        self.__drive_name = None
        self.__drive_path = None
        # Single reference of class MainWindow in main file.
        self.__main_window = window
        # Class objects
        self.__format = Format()

    def add_iso_file(self):
        file = QFileDialog.getOpenFileName(self.__main_window, "Select .iso file", filter="ISO File(*.iso)")[0]
        if file == '' or file is None:
            print("Please select Windows iso file!")
            return
        self.__file_path, self.__file_name = self.__format.format_filepath(file)
        self.change_addfile_and_filenamelabel_state()
        self.__main_window.remove_file_button.show()
        self.__main_window.drive_button.setDisabled(False)


    def select_usb_drive(self):
        self.__main_window.drive_frame.show()

    def start_flash_button(self):
        pass

    def refresh_drive_table(self):
        pass

    def remove_file_button(self):
        self.__file_name = None
        self.__file_path = None
        self.__main_window.remove_file_button.hide()
        self.__main_window.file_name_label.hide()
        self.__main_window.add_button.show()
        self.__main_window.drive_button.setEnabled(False)

    def change_drive_button(self):
        pass

    def apply_btn_in_drive_frame(self):
        pass

    def cancel_btn_in_drive_frame(self):
        self.__main_window.drive_frame.hide()

    def change_addfile_and_filenamelabel_state(self):
        self.__main_window.add_button.hide()
        self.__main_window.file_name_label.setText(self.__format.format_string_label(self.__file_name))
        self.__main_window.file_name_label.show()

    def change_drivebtn_and_drivelabel_state(self):
        self.__main_window.drive_button.hide()
        self.__main_window.drive_name_label.setText(self.__format.format_string_label(self.__drive_name))
        self.__main_window.drive_name_label.show()

    # Buttons of Flash Screen dialog.
    # TODO define working of buttons in Flash Screen Dialog.

    def go_back_button(self):
        pass

    def cancel_flash_button(self):
        pass

    # Getters & Setters

    def get_file_name(self):
        return self.__file_name

    def get_file_path(self):
        return self.__file_path

    def get_drive_name(self):
        return self.__drive_name

    def get_drive_path(self):
        return self.__drive_path
