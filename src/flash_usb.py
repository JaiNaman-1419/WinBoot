from sys import exit
from src.replicate import Replica
from subprocess import check_output
from PyQt5.QtWidgets import QMessageBox
from os.path import isfile, exists, join
from shutil import copyfile, ignore_patterns
from os import listdir, mkdir, rmdir, remove


class FlashUSB:

    def __init__(self, data, button_obj):
        self.__data = data
        self.__dir = False
        self.__buttons_obj = button_obj

    def __show_alert_box(self, message):
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Critical)
        alert.setText("Error")
        alert.setInformativeText(message)
        alert.setWindowTitle("Error occurred!")
        alert.setStandardButtons(QMessageBox.Ok)
        alert.buttonClicked.connect(lambda: alert.hide())
        alert.show()

    def __show_message_box(self, msg):
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setText("Congratulations!")
        message.setInformativeText(msg)
        message.setWindowTitle("Flashed")
        message.setStandardButtons(QMessageBox.Ok)
        message.buttonClicked.connect(lambda: message.hide())
        message.show()

    def __create_directory(self, directory):
        try:
            if not exists(directory):
                mkdir(directory)
                self.__dir = True
            return True

        except Exception as e:
            self.__show_alert_box("Something went wrong!!\n[Line number: 26]")
            print(f"\n\nLine Number: 26\nError occurred: {e}")
            return False

    def __remove_directory(self):
        if self.__dir:
            rmdir(self.__data.get_iso_mount_point())

    def __mount_iso_file(self):
        if not self.__create_directory(self.__data.get_iso_mount_point()):
            # TODO change message of alert box!
            self.__show_alert_box("Something went wrong!!\n[Line number: 42]")
            exit()
        check_output(["sudo", "mount", f"{self.__data.get_file_path()}", f"{self.__data.get_iso_mount_point()}"])

    def __unmount_iso_file(self):
        try:
            check_output(["sudo", "umount", f"{self.__data.get_iso_mount_point()}"])
        except Exception as e:
            # TODO change message of alert box!
            self.__show_alert_box("Something went wrong!!\n[Line number: 49]")
            print(f"\n\nLine Number: 49\nError occurred: {e}")
            exit()

        try:
            if exists(self.__data.get_iso_mount_point()):
                rmdir(self.__data.get_iso_mount_point())
        except Exception as e:
            # TODO change message of alert box!
            self.__show_alert_box("Something went wrong!!\n[Line number: 57]")
            print(f"\n\nLine Number: 57\nError occurred: {e}")
            exit()

    def convert_wim_to_swm(self):
        try:
            check_output(["wimlib-imagex", "split", f"{self.__data.get_iso_mount_point()}/sources/install.wim",
                          "/media/install.swm", "4000"])
        except Exception as e:
            # TODO change message of alert box!
            self.__show_alert_box("Something went wrong!!\n[Line number: 67]")
            print(f"\n\nLine Number: 67\nError occurred: {e}")
            exit()

    def __calculate_copied_size(self):
        replica = Replica()
        folder_size = replica.get_folder_size(self.__data.get_drive_path())
        iso_file_size = replica.get_folder_size(self.__data.get_iso_mount_point())
        status = float("{:.2f}".format((folder_size / iso_file_size) * 100))
        return status - 1

    def __update_progress_bar(self, flash_screen):
        flash_screen.flash_bar.setValue(self.__calculate_copied_size())

    def __copy_items_to_usb(self, flash_screen):

        if self.__buttons_obj.is_flash_cancelled():
            return

        src = self.__data.get_file_path()
        dst = self.__data.get_iso_mount_point()
        replica = Replica()
        src_items = listdir(src)

        for item_name in src_items:
            if self.__buttons_obj.is_flash_cancelled():
                return

            item = join(src, item_name)

            if isfile(item):
                copyfile(item, join(dst, item_name))
                self.__update_progress_bar(flash_screen)
            else:
                replica.copytree(src=item, dst=join(dst, item_name), flash_screen=flash_screen,
                                 callback=self.__update_progress_bar, ignore=ignore_patterns("install.wim"))

        del replica

    def __copy_swm_file_to_usb(self, flash_screen):
        if self.__buttons_obj.is_flash_cancelled():
            return

        replica = Replica()
        for file in ["install.swm", "install2.swm"]:
            src = join("/media", file)
            dst = join(self.__data.get_iso_mount_point(), "sources", file)
            replica.copyfileobj(fsrc=src, fdst=dst, flash_screen=flash_screen, callback=self.__update_progress_bar)
            try:
                remove(src)
            except Exception as e:
                self.__show_alert_box("Something went wrong\n[Line number: 120]")
                print(f"\n\nLine Number: 120\nError occurred: {e}")

        del replica

    def start_flash(self, flash_screen):
        self.__mount_iso_file()
        self.__copy_items_to_usb(flash_screen)
        # self.convert_wim_to_swm()
        self.__copy_swm_file_to_usb(flash_screen)
        self.__unmount_iso_file()
        self.__remove_directory()
        flash_screen.flash_bar.setValue(100)
        self.__show_message_box("Congratulations!\nYour Windows bootable USB drive is ready.")
