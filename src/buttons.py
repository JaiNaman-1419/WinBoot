from PyQt5.QtCore import Qt
from src.flash_usb import FlashUSB
from src.format_name import Format
from src.format_usb import FormatUSB
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox


class Buttons:

    def __init__(self, widget, drive):

        # Class objects
        self.__format = Format()
        self.__drive = drive

        # Class Attributes
        self.__is_cancelled = False
        self.__checkbox_list = list()

        # Single reference of class MainWindow in main file.
        self.__widget = widget

    def __show_alert_box(self, message):
        alert = QMessageBox()
        alert.setStyleSheet("color: #FFFFFF; font-size: 20px; background-color: #121212;")
        alert.setIcon(QMessageBox.Critical)
        alert.setText("Error")
        alert.setInformativeText(f"{message}")
        alert.setWindowTitle("Warning!")
        alert.setStandardButtons(QMessageBox.Ok)
        alert.buttonClicked.connect(lambda: alert.hide())
        alert.show()

    def add_iso_file(self, window, data):
        file = QFileDialog.getOpenFileName(window, "Select .iso file", filter="ISO File(*.iso)")[0]
        if file == '' or file is None:
            self.__show_alert_box("Please select Windows iso file!")
            return
        file_path, file_name = self.__format.format_filepath(file)
        data.set_file_name(file_name)
        data.set_file_path(file_path)
        self.change_addfile_and_filenamelabel_state(window, data)
        window.remove_file_button.show()
        window.drive_button.setDisabled(False)

    def remove_file_button(self, window, data):
        data.set_file_name(None)
        data.set_file_path(None)
        data.set_drive_name(None)
        data.set_drive_path(None)
        data.set_drive_device(None)
        window.remove_file_button.hide()
        window.change_drive_button.hide()
        window.file_name_label.hide()
        window.drive_name_label.hide()
        window.add_button.show()
        window.drive_button.show()
        window.drive_button.setEnabled(False)
        window.start_button.setEnabled(False)

    def select_usb_drive(self, window):
        if self.refresh_drive_table(window):
            window.drive_frame.show()
        else:
            self.__show_alert_box("Please enter USB Drive!")

    def change_drive_button(self, window, data):
        data.set_drive_name(None)
        data.set_drive_path(None)
        data.set_drive_device(None)
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
                window.drive_table.setItem(index, 0, name)
                window.drive_table.setItem(index, 1, QTableWidgetItem(size))
                window.drive_table.setItem(index, 2, QTableWidgetItem(location))
                index += 1

    def drive_selected(self, window, data, drive):
        data.set_drive_name(f"{drive.text()}\n({drive.size})")
        data.set_drive_device(drive.device)
        for index, disk in enumerate(self.__checkbox_list):

            if drive.device == disk.device:
                if disk.checkState() == Qt.Checked:
                    disk.setCheckState(Qt.Unchecked)
                    data.set_drive_name(None)
                    data.set_drive_device(None)
                    window.apply_button.setEnabled(False)
                else:
                    disk.setCheckState(Qt.Checked)
                    window.apply_button.setDisabled(False)

                continue

            disk.setCheckState(Qt.Unchecked)

    def refresh_drive_table(self, window):
        if window.drive_table.rowCount() > 0:
            window.drive_table.removeRow(window.drive_table.rowCount() - 1)
            self.__drive.remove_dictionary_element()
            self.__drive.reduce_disk_count()

        self.__checkbox_list.clear()
        if not self.__drive.get_disk_properties():
            return False
        self.__assign_drive_properties_in_table(window)
        return True

    def apply_btn_in_drive_frame(self, window, data):
        window.drive_frame.hide()
        window.drive_button.hide()
        window.drive_name_label.setText(data.get_drive_name())
        window.drive_name_label.show()
        window.change_drive_button.show()
        window.start_button.setDisabled(False)
        disks = self.__drive.get_disk_list()
        data.set_drive_path(self.__format.format_drive_path(disks[data.get_drive_device()]))

    def cancel_btn_in_drive_frame(self, window, data):
        data.set_drive_name(None)
        data.set_drive_path(None)
        data.set_drive_device(None)
        window.drive_frame.hide()

    def start_flash_button(self, window, data, flash_screen):
        self.switch_to_flashing_screen()
        self.set_cancelled_status(False)
        self.__start_usb_flash(data, flash_screen)
        self.remove_file_button(window, data)

    def change_addfile_and_filenamelabel_state(self, window, data):
        window.add_button.hide()
        window.file_name_label.setText(self.__format.format_string_label(data.get_file_name()))
        window.file_name_label.show()

    def change_drivebtn_and_drivelabel_state(self, window):
        window.drive_button.hide()
        window.drive_name_label.setText(self.__format.format_string_label(window.get_drive_name()))
        window.drive_name_label.show()

    def switch_to_flashing_screen(self):
        self.__widget.setCurrentIndex(self.__widget.currentIndex() + 1)

    # Buttons of Flash Screen starts

    def set_cancelled_status(self, status):
        self.__is_cancelled = status

    def is_flash_cancelled(self):
        return self.__is_cancelled

    def __start_usb_flash(self, data, flash_screen):
        usb_format = FormatUSB(data)
        usb_flash = FlashUSB(data, self)
        usb_format.format_usb_drive(flash_screen)
        usb_flash.mount_iso_file(flash_screen)
        usb_flash.convert_wim_to_swm(flash_screen)
        usb_flash.start_flash(flash_screen)

    def cancel_flash_button(self):
        self.set_cancelled_status(True)
        self.switch_to_main_screen()

    def completed_flash_button(self, flash_screen):
        self.switch_to_main_screen()
        flash_screen.cancel_button.show()
        flash_screen.completed_button.hide()

    def switch_to_main_screen(self):
        self.__widget.setCurrentIndex(self.__widget.currentIndex() - 1)
