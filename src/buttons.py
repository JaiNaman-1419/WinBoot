from PyQt5.QtCore import Qt
from src.format_name import Format
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem


class Buttons:

    # Buttons of Main Window Dialog/
    # TODO define working of buttons in Main Window Dialog.

    def __init__(self, widget, drive):
        # Class Attributes
        self.__drive_device = None
        self.__checkbox_list = list()
        # Single reference of class MainWindow in main file.
        self.__widgets = widget
        # Class objects
        self.__format = Format()
        self.__drive = drive

    def add_iso_file(self, window):
        file = QFileDialog.getOpenFileName(window, "Select .iso file", filter="ISO File(*.iso)")[0]
        if file == '' or file is None:
            print("Please select Windows iso file!")
            return
        file_path, file_name = self.__format.format_filepath(file)
        window.set_file_name(file_name)
        window.set_file_path(file_path)
        self.change_addfile_and_filenamelabel_state(window)
        window.remove_file_button.show()
        window.drive_button.setDisabled(False)

    def remove_file_button(self, window):
        window.set_file_name(None)
        window.set_file_path(None)
        window.set_drive_name(None)
        window.set_drive_path(None)
        window.remove_file_button.hide()
        window.change_drive_button.hide()
        window.file_name_label.hide()
        window.drive_name_label.hide()
        window.add_button.show()
        window.drive_button.show()
        window.drive_button.setEnabled(False)
        window.start_button.setEnabled(False)

    def select_usb_drive(self, window):
        window.drive_frame.show()
        self.refresh_drive_table(window)

    def change_drive_button(self, window):
        window.set_drive_name(None)
        window.set_drive_path(None)
        window.change_drive_button.hide()
        window.drive_name_label.hide()
        window.drive_button.show()
        window.apply_button.setEnabled(False)
        window.start_button.setEnabled(False)

    def __assign_drive_properties_in_table(self, window):
        window.drive_table.setRowCount(self.__drive.get_disk_count())
        index = 0
        for location, value in self.__drive.get_disk_names_list().items():
            for size, name in value.items():
                if name == "Cruzer Blade":
                    name = "Sandisk " + name
                name = QTableWidgetItem(name)
                name.setFlags(Qt.ItemIsEnabled)
                name.setCheckState(Qt.Unchecked)
                name.device = location
                name.size = size
                self.__checkbox_list.append(name)
                print(self.__checkbox_list)
                window.drive_table.setItem(index, 0, name)
                window.drive_table.setItem(index, 1, QTableWidgetItem(size))
                window.drive_table.setItem(index, 2, QTableWidgetItem(location))
                index += 1

    def drive_selected(self, window, drive):
        window.set_drive_name(f"{drive.text()}\n({drive.size})")
        window.set_drive_path(drive.device)
        for index, disk in enumerate(self.__checkbox_list):

            if drive.device == disk.device:
                if disk.checkState() == Qt.Checked:
                    disk.setCheckState(Qt.Unchecked)
                    window.set_drive_name(None)
                    window.set_drive_path(None)
                    window.apply_button.setEnabled(False)
                else:
                    disk.setCheckState(Qt.Checked)
                    window.apply_button.setDisabled(False)

                print(f"Drive Name: {window.get_drive_name()}\nDrive Path: {window.get_drive_path()}")
                continue

            disk.setCheckState(Qt.Unchecked)

    def refresh_drive_table(self, window):
        if window.drive_table.rowCount() > 0:
            window.drive_table.removeRow(window.drive_table.rowCount() - 1)
            self.__drive.remove_dictionary_element()
            self.__drive.reduce_disk_count()

        self.__checkbox_list.clear()
        self.__drive.get_disk_properties()
        self.__assign_drive_properties_in_table(window)

    def apply_btn_in_drive_frame(self, window):
        window.drive_frame.hide()
        window.drive_button.hide()
        window.drive_name_label.setText(window.get_drive_name())
        window.drive_name_label.show()
        window.change_drive_button.show()
        window.start_button.setDisabled(False)
        disks = self.__drive.get_disk_list()
        window.set_drive_path(disks[self.__drive_path])
        print(f"Drive Name: {window.get_drive_name()}\nDrive Path: {window.get_drive_path()}")

    def cancel_btn_in_drive_frame(self, window):
        window.set_drive_name(None)
        window.set_drive_path(None)
        window.drive_frame.hide()
        print(f"Drive Name: {window.get_drive_name()}\nDrive Path: {window.get_drive_path()}")

    def start_flash_button(self):
        self.switch_to_flashing_screen()

    def change_addfile_and_filenamelabel_state(self, window):
        window.add_button.hide()
        window.file_name_label.setText(self.__format.format_string_label(window.get_file_name()))
        window.file_name_label.show()

    def change_drivebtn_and_drivelabel_state(self, window):
        window.drive_button.hide()
        window.drive_name_label.setText(self.__format.format_string_label(window.get_drive_name()))
        window.drive_name_label.show()

    def switch_to_flashing_screen(self):
        self.__widgets.setCurrentIndex(self.__widgets.currentIndex() + 1)

    # Buttons of Flash Screen dialog.
    # TODO define working of buttons in Flash Screen Dialog.

    def go_back_button(self, flash_screen):
        flash_screen.back_button.setEnabled(False)
        self.switch_to_main_screen()

    def cancel_flash_button(self, flash_screen):
        flash_screen.back_button.setDisabled(False)

    def switch_to_main_screen(self):
        self.__widgets.setCurrentIndex(self.__widgets.currentIndex() - 1)
