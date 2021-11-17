from os.path import exists
from subprocess import check_output
from os import getcwd, system, mkdir


class FormatUSB:

    def __init__(self, data):
        self.__working_directory = getcwd()
        self.__USB_LABEL = "WINDOWS"
        self.__USB_DEVICE = data.get_drive_device()
        self.__USB_PATH = data.get_drive_path()

    def __create_directory(self, directory):
        if not exists(directory):
            mkdir(directory)

    def __unmount_usb_patitions(self):
        system(f"umount {self.__USB_DEVICE[:-1]}?")

    def __erase_partition_signature(self):
        check_output(["wipefs", "--all", "--force", f"{self.__USB_DEVICE[:-1]}"])

    def __create_partition_table(self):
        check_output(["parted", "-s", "-a", "optimal", "--", f"{self.__USB_DEVICE[:-1]}", "mklabel", "gpt"])

    def __create_new_partition(self):
        check_output(
            ["parted", "-s", "-a", "optimal", "--", f"{self.__USB_DEVICE[:-1]}", "mkpart", "primary", "fat32",
             "1MiB", "100%"])

    def __disk_align_check(self):
        check_output(["parted", "-s", "--", f"{self.__USB_DEVICE[:-1]}", "align-check", "optimal", "1"])

    def __format_new_partition(self):
        check_output(["mkfs.fat", "-F32", "-n", f"{self.__USB_LABEL}", f"{self.__USB_DEVICE}"])

    def __mount_formatted_drive(self):
        self.__create_directory(self.__USB_PATH)
        check_output(["sudo", "mount", self.__USB_DEVICE, self.__USB_PATH])

    def format_usb_drive(self, flash_screen):
        self.__unmount_usb_patitions()
        flash_screen.flash_bar.setFormat('%.02f%%' % 1.00)
        flash_screen.flash_bar.setValue(1.00)
        self.__erase_partition_signature()
        flash_screen.flash_bar.setFormat('%.02f%%' % 2.00)
        flash_screen.flash_bar.setValue(2.00)
        self.__create_partition_table()
        flash_screen.flash_bar.setFormat('%.02f%%' % 3.00)
        flash_screen.flash_bar.setValue(3.00)
        self.__create_new_partition()
        flash_screen.flash_bar.setFormat('%.02f%%' % 4.00)
        flash_screen.flash_bar.setValue(4.00)
        flash_screen.flash_bar.setFormat('%.02f%%' % 5.00)
        flash_screen.flash_bar.setValue(5.00)
        self.__disk_align_check()
        flash_screen.flash_bar.setFormat('%.02f%%' % 6.00)
        flash_screen.flash_bar.setValue(6.00)
        self.__format_new_partition()
        self.__mount_formatted_drive()
        flash_screen.flash_bar.setFormat('%.02f%%' % 7.00)
        flash_screen.flash_bar.setValue(7.00)
