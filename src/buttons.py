from PyQt5.QtCore import Qt
from src.format import Format
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem


class Buttons:

    # Buttons of Main Window Dialog/
    # TODO define working of buttons in Main Window Dialog.

    def __init__(self, window, drive):
        # Class Attributes
        self.__file_name = None
        self.__file_path = None
        self.__drive_name = None
        self.__drive_path = None
        self.__checkbox_list = list()
        # Single reference of class MainWindow in main file.
        self.__main_window = window
        # Class objects
        self.__format = Format()
        self.__drive = drive

    def add_iso_file(self):
        file = QFileDialog.getOpenFileName(self.__main_window, "Select .iso file", filter="ISO File(*.iso)")[0]
        if file == '' or file is None:
            print("Please select Windows iso file!")
            return
        self.__file_path, self.__file_name = self.__format.format_filepath(file)
        self.change_addfile_and_filenamelabel_state()
        self.__main_window.remove_file_button.show()
        self.__main_window.drive_button.setDisabled(False)

    def remove_file_button(self):
        self.__file_name = None
        self.__file_path = None
        self.__drive_name = None
        self.__drive_path = None
        self.__main_window.remove_file_button.hide()
        self.__main_window.change_drive_button.hide()
        self.__main_window.file_name_label.hide()
        self.__main_window.drive_name_label.hide()
        self.__main_window.add_button.show()
        self.__main_window.drive_button.show()
        self.__main_window.drive_button.setEnabled(False)
        self.__main_window.start_button.setEnabled(False)

    def select_usb_drive(self):
        self.__main_window.drive_frame.show()
        self.refresh_drive_table()

    def change_drive_button(self):
        self.__drive_name = None
        self.__drive_path = None
        self.__main_window.change_drive_button.hide()
        self.__main_window.drive_name_label.hide()
        self.__main_window.drive_button.show()
        self.__main_window.apply_button.setEnabled(False)
        self.__main_window.start_button.setEnabled(False)

    def __assign_drive_properties_in_table(self):
        self.__main_window.drive_table.setRowCount(self.__drive.get_disk_count())
        index = 0
        for location, value in self.__drive.get_disk_names_list().items():
            for size, name in value.items():
                if name == "Cruzer Blade":
                    name = "Sandisk " + name
                name = QTableWidgetItem(name)
                name.setFlags(Qt.ItemIsEnabled)
                name.setCheckState(Qt.Unchecked)
                name.device = location
                self.__checkbox_list.append(name)
                print(self.__checkbox_list)
                self.__main_window.drive_table.setItem(index, 0, name)
                self.__main_window.drive_table.setItem(index, 1, QTableWidgetItem(size))
                self.__main_window.drive_table.setItem(index, 2, QTableWidgetItem(location))
                index += 1

    def drive_selected(self, drive):
        self.__drive_name = drive.text()
        self.__drive_path = drive.device
        for index, disk in enumerate(self.__checkbox_list):

            if drive.device == disk.device:
                if disk.checkState() == Qt.Checked:
                    disk.setCheckState(Qt.Unchecked)
                    self.__drive_name = None
                    self.__drive_path = None
                    self.__main_window.apply_button.setEnabled(False)
                else:
                    disk.setCheckState(Qt.Checked)
                    self.__main_window.apply_button.setDisabled(False)

                print(f"Drive Name: {self.__drive_name}\nDrive Path: {self.__drive_path}")
                continue

            disk.setCheckState(Qt.Unchecked)

    def refresh_drive_table(self):
        if self.__main_window.drive_table.rowCount() > 0:
            self.__main_window.drive_table.removeRow(self.__main_window.drive_table.rowCount() - 1)
            self.__drive.remove_dictionary_element()
            self.__drive.reduce_disk_count()

        self.__checkbox_list.clear()
        self.__drive.get_disk_properties()
        self.__assign_drive_properties_in_table()

    def apply_btn_in_drive_frame(self):
        self.__main_window.drive_frame.hide()
        self.__main_window.drive_button.hide()
        self.__main_window.drive_name_label.setText(self.__drive_name)
        self.__main_window.drive_name_label.show()
        self.__main_window.change_drive_button.show()
        self.__main_window.start_button.setDisabled(False)
        print(f"Drive Name: {self.__drive_name}\nDrive Path: {self.__drive_path}")

    def cancel_btn_in_drive_frame(self):
        self.__drive_name = None
        self.__drive_path = None
        self.__main_window.drive_frame.hide()
        print(f"Drive Name: {self.__drive_name}\nDrive Path: {self.__drive_path}")

    def start_flash_button(self):
        pass

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
