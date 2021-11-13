from sys import exit
from src.replicate import Replica
from subprocess import check_output
from PyQt5.QtWidgets import QMessageBox
from os.path import isfile, exists, join
from shutil import copyfile, ignore_patterns
from os import listdir, mkdir, rmdir, remove, getcwd


class FlashUSB:

    def __init__(self, data, button_obj):
        self.__data = data
        self.__dir = False
        self.__buttons_obj = button_obj

    def __show_alert_box(self, message):
        alert = QMessageBox()
        alert.setStyleSheet("color: #FFFFFF; font-size: 20px; background-color: #121212;")
        alert.setIcon(QMessageBox.Critical)
        alert.setText("Error")
        alert.setInformativeText(f"Error occurred {message}")
        alert.setWindowTitle("Error occurred!")
        alert.setStandardButtons(QMessageBox.Ok)
        alert.buttonClicked.connect(lambda: alert.hide())
        alert.show()

    def __show_message_box(self, msg):
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setText("Congratulations!")
        message.setInformativeText(msg)
        message.setWindowTitle("Information")
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
            self.__show_alert_box("Something went wrong!!\n[Line number: 38]")
            # print(f"\n\nLine Number: 39\nError occurred: {e}")
            return False

    def __remove_directory(self):
        if self.__dir:
            rmdir(self.__data.get_iso_mount_point())

    def mount_iso_file(self):
        if not self.__create_directory(self.__data.get_iso_mount_point()):
            # TODO change message of alert box!
            self.__show_alert_box("Something went wrong!!\n[Line number: 42]")
            exit()
        check_output(["mount", join(self.__data.get_file_path(), self.__data.get_file_name()),
                      f"{self.__data.get_iso_mount_point()}"])

    def __unmount_iso_file(self):
        try:
            check_output(["umount", f"{self.__data.get_iso_mount_point()}"])
        except Exception as e:
            # TODO change message of alert box!
            self.__show_alert_box("Something went wrong!!\n[Line number: 49]")
            # print(f"\n\nLine Number: 49\nError occurred: {e}")
            exit()

        try:
            if exists(self.__data.get_iso_mount_point()):
                rmdir(self.__data.get_iso_mount_point())
                # check_output(["pkexec", "rmdir", self.__data.get_iso_mount_point()])
        except Exception as e:
            # TODO change message of alert box!
            self.__show_alert_box("Something went wrong!!\n[Line number: 57]")
            # print(f"\n\nLine Number: 57\nError occurred: {e}")
            exit()

    def convert_wim_to_swm(self):
        try:
            # print(getcwd())
            wim_lib = join(getcwd(), "Modules", "wimlib-imagex")
            check_output([wim_lib, "split", join(self.__data.get_iso_mount_point(), "sources/install.wim"),
                          "/media/install.swm", "4000"])
        except Exception as e:
            # TODO change message of alert box!
            self.__show_alert_box("Something went wrong!!\n[Line number: 67]")
            # print(f"\n\nLine Number: 81\nError occurred: {e}")
            exit()

    def __calculate_copied_size(self):
        replica = Replica()
        folder_size = replica.get_folder_size(self.__data.get_drive_path())
        iso_file_size = replica.get_folder_size(self.__data.get_iso_mount_point())
        status = float("{:.2f}".format((folder_size / iso_file_size) * 100))
        if status == 100.00:
            return status - 1
        return status

    def __update_progress_bar(self, flash_screen):
        value = self.__calculate_copied_size()
        # print(value, end="\t")
        flash_screen.flash_bar.setFormat('%.02f%%' % value)
        flash_screen.flash_bar.setValue(value)

    def __copy_items_to_usb(self, flash_screen):

        if self.__buttons_obj.is_flash_cancelled():
            return

        src = self.__data.get_iso_mount_point()
        dst = self.__data.get_drive_path()
        print("Line 108:", src, dst)
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
            dst = join(self.__data.get_drive_path(), f"sources/{file}")
            fsrc = open(src, 'rb')
            fdst = open(dst, 'wb')
            replica.copyfileobj(fsrc=fsrc, fdst=fdst, flash_screen=flash_screen, callback=self.__update_progress_bar)
            try:
                # print("Removing file:", src)
                remove(src)
            except Exception as e:
                self.__show_alert_box("Something went wrong\n[Line number: 120]")
                # print(f"\n\nLine Number: 120\nError occurred: {e}")

        del replica

    def start_flash(self, flash_screen):
        # self.__mount_iso_file()
        # print("Start copying items to USB")
        self.__copy_items_to_usb(flash_screen)
        # self.convert_wim_to_swm()
        # print("Percentage before swm:", flash_screen.flash_bar.value())
        # print("Start copying swm files to USB")
        self.__copy_swm_file_to_usb(flash_screen)
        # print("Unmounting iso file")
        self.__unmount_iso_file()
        # print("Removing directory")
        # self.__remove_directory()
        flash_screen.flash_bar.setFormat('%.02f%%' % 100.00)
        flash_screen.flash_bar.setValue(100.00)
        # print("Your Windows bootable USB drive is ready.")
        self.__show_message_box("Congratulations!\nYour Windows bootable USB drive is ready.")
