from os import getcwd
from subprocess import check_output


class FormatUSB:

    def __init__(self, data):
        self.__working_directory = getcwd()
        self.__USB_LABEL = "WINDOWS"
        self.__USB_DEVICE = data.get_drive_device()

    # sudo wipefs --all --force /dev/sdb
    # sudo parted -s -a optimal -- /dev/sdb mklabel msdos
    # sudo parted -s -a optimal -- /dev/sdb mkpart primary fat32 1MiB 100%
    # sudo parted -s -- /dev/sdb align-check optimal 1
    # sudo mkfs.vfat -F32 /dev/sdb1
    # sudo mkfs.vfat -F 32 -n 'name_for_your_pendrive' /dev/sdy1

    def __erase_partition_signature(self):
        check_output(["sudo", "wipefs", "--all", "--force", f"{self.__USB_DEVICE[:-1]}"])

    def __create_partition_table(self):
        check_output(["sudo", "parted", "-s", "-a", "optimal", "--", f"{self.__USB_DEVICE[:-1]}", "mklabel", "gpt"])

    def __create_new_partition(self):
        check_output(["sudo", "parted", "-s", "-a", "optimal", "--", f"{self.__USB_DEVICE[:-1]}", "mkpart", "primary", "fat32", "1MiB", "100%"])

    def __disk_align_check(self):
        check_output(["sudo", "parted", "-s", "--", f"{self.__USB_DEVICE[:-1]}", "align-check", "optimal", "1"])

    def __format_new_partition(self):
        check_output(["sudo", "mkfs.vfat", "-F32", "-n", f"{self.__USB_LABEL}", f"{self.__USB_DEVICE}"])

    def format_usb_drive(self):
        self.__erase_partition_signature()
        self.__create_partition_table()
        self.__create_new_partition()
        self.__disk_align_check()
        self.__format_new_partition()
