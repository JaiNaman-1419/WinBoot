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

    def __show_alert_box(self, dialog=None, icon=QMessageBox.Critical, text="Error", message=None, title="Error occurred"):
        alert = QMessageBox(dialog)
        alert.setStyleSheet("color: #FFFFFF; font-size: 20px; background-color: #121212;")
        alert.setIcon(icon)
        alert.setText(text)
        alert.setInformativeText(message)
        alert.setWindowTitle(title)
        alert.setStandardButtons(QMessageBox.Ok)
        alert.buttonClicked.connect(lambda: alert.hide())
        alert.show()

    def __create_directory(self, directory):
        try:
            if not exists(directory):
                mkdir(directory)
                self.__dir = True
            return True

        except Exception:
            self.__show_alert_box("Error occurred while creating directory!!\n[Flash_USB, Line number: 36]")
            return False

    def __remove_directory(self):
        if self.__dir:
            rmdir(self.__data.get_iso_mount_point())

    def mount_iso_file(self, flash_screen):
        if not self.__create_directory(self.__data.get_iso_mount_point()):
            # TODO change message of alert box!
            self.__show_alert_box("Error occurred while mounting iso file!!\n[Flash_USB, Line Number: 46]")
            exit()
        check_output(["mount", join(self.__data.get_file_path(), self.__data.get_file_name()),
                      f"{self.__data.get_iso_mount_point()}"])
        flash_screen.flash_bar.setFormat('%.02f%%' % 8.00)
        flash_screen.flash_bar.setValue(8.00)

    def __unmount_iso_file(self):
        try:
            check_output(["umount", f"{self.__data.get_iso_mount_point()}"])
        except Exception:
            # TODO change message of alert box!
            self.__show_alert_box("Error occurred while unmounting iso file!!\n[Flash_USB, Line number: 58]")
            exit()

        try:
            if exists(self.__data.get_iso_mount_point()):
                rmdir(self.__data.get_iso_mount_point())
        except Exception:
            # TODO change message of alert box!
            self.__show_alert_box("Error occurred while removing mounted directory!!\n[Flash_USB, Line number: 66]")
            exit()

    def convert_wim_to_swm(self, flash_screen):
        try:
            # print(getcwd())
            wim_lib = join(getcwd(), "Modules", "wimlib-imagex")
            check_output([wim_lib, "split", join(self.__data.get_iso_mount_point(), "sources/install.wim"),
                          "/media/install.swm", "4000"])
            flash_screen.flash_bar.setFormat('%.02f%%' % 10.00)
            flash_screen.flash_bar.setValue(10.00)
        except Exception:
            # TODO change message of alert box!
            self.__show_alert_box("Error occurred while converting wim to swm!!\n[Flash_USB, Line number: 79]")
            exit()

    def __calculate_copied_size(self):
        replica = Replica()
        folder_size = replica.get_folder_size(self.__data.get_drive_path())
        iso_file_size = replica.get_folder_size(self.__data.get_iso_mount_point())
        status = float("{:.2f}".format((folder_size / iso_file_size) * 90))
        if status == 90.00:
            return status - 1
        return status

    def __update_progress_bar(self, flash_screen):
        value = self.__calculate_copied_size() + 10.00
        flash_screen.flash_bar.setFormat('%.02f%%' % value)
        flash_screen.flash_bar.setValue(value)

    def __copy_items_to_usb(self, flash_screen):

        if self.__buttons_obj.is_flash_cancelled():
            return

        src = self.__data.get_iso_mount_point()
        dst = self.__data.get_drive_path()
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
                remove(src)
            except Exception:
                self.__show_alert_box("Error occurred while copying swm file!!\n[Flash_USB, Line number: 120]")

        del replica

    def __unmount_formatted_usb_drive(self, flash_screen):
        check_output(["sudo", "umount", self.__data.get_drive_device()])
        rmdir(self.__data.get_drive_path())
        self.__show_alert_box(flash_screen, QMessageBox.Information, "Congratulations!",
                              "Your USB drive is now bootable and already unmounted.\nTo use it just remove the USB "
                              "and plug it again!", "Information")
        # check_output(["sudo", "rmdir", self.__data.get_drive_path()])

    def start_flash(self, flash_screen):
        self.__copy_items_to_usb(flash_screen)
        self.__copy_swm_file_to_usb(flash_screen)
        self.__unmount_iso_file()
        self.__unmount_formatted_usb_drive(flash_screen)
        flash_screen.flash_bar.setFormat('%.02f%%' % 100.00)
        flash_screen.flash_bar.setValue(100.00)
        flash_screen.cancel_button.hide()
        flash_screen.completed_button.show()
