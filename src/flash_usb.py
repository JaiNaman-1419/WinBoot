from sys import exit
from src.replicate import Replica
from subprocess import check_output
from os import listdir, mkdir, rmdir
from os.path import isfile, exists, join
from shutil import copyfile, ignore_patterns


class FlashUSB:

    # TODO create method which copy all files excluding install.wim to usb drive.

    def __init__(self, data, button_obj):
        self.__data = data
        self.__dir = False
        self.__buttons_obj = button_obj

    def __create_directory(self, directory):
        try:
            if not exists(directory):
                mkdir(directory)
                self.__dir = True
            return True

        except Exception as e:
            print(f"\n\nLine Number: 16\nError occurred: {e}")
            return False

    def __remove_directory(self):
        if self.__dir:
            rmdir(self.__data.get_iso_mount_point())

    def __mount_iso_file(self):
        if not self.__create_directory(self.__data.get_iso_mount_point()):
            # TODO show dialog box that an error occurred!
            exit()
        check_output(["sudo", "mount", f"{self.__data.get_file_path()}", f"{self.__data.get_iso_mount_point()}"])

    def __unmount_iso_file(self):
        try:
            check_output(["sudo", "umount", f"{self.__data.get_iso_mount_point()}"])
        except Exception as e:
            # TODO show dialog box that an error occurred!
            print(f"\n\nLine Number: 32\nError occurred: {e}")

        try:
            if exists(self.__data.get_iso_mount_point()):
                rmdir(self.__data.get_iso_mount_point())
        except Exception as e:
            # TODO show dialog box that an error occurred!
            print(f"\n\nLine Number: 38\nError occurred: {e}")

    def __convert_wim_to_swm(self):
        try:
            check_output(["wimlib-imagex", "split", f"{self.__data.get_iso_mount_point()}/sources/install.wim",
                          f"/media/install.swm", "4000"])
        except Exception as e:
            # TODO show dialog box that an error occurred!
            print(f"\n\nLine Number: 47\nError occurred: {e}")

    def __copy_items_to_usb(self):
        src = self.__data.get_file_path()
        dst = self.__data.get_iso_mount_point()
        replica = Replica()
        src_items = listdir(src)

        for item_name in src_items:
            item = join(src, item_name)

            if isfile(item):
                copyfile(item, join(dst, item_name))

            else:
                replica.copytree(src=item, dst=join(dst, item_name), callback=None,
                                 ignore=ignore_patterns("install.wim"))

        del replica

    def __copy_swm_file_to_usb(self):
        replica = Replica()
        for file in ["install.swm", "install2.swm"]:
            src = join("/media", file)
            dst = join(self.__data.get_iso_mount_point(), "sources", file)
            replica.copyfileobj(fsrc=src, fdst=dst, callback=None)

        del replica

    def start_flash(self):
        self.__mount_iso_file()
        self.__copy_items_to_usb()
        self.__convert_wim_to_swm()
        self.__copy_swm_file_to_usb()
        self.__unmount_iso_file()
        self.__remove_directory()
