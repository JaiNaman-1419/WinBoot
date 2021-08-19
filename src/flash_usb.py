from sys import exit
from subprocess import check_output
from shutil import copyfile, copytree
from os.path import isdir, isfile, exists
from os import listdir, mkdir, rmdir, getenv


class FlashUSB:

    # TODO create method which copy all files excluding install.wim to usb drive.

    def __init__(self, filepath, drivepath):
        self.__file_path = filepath
        self.__drive_path = drivepath
        self.__iso_mountpoint = "/media/Windows"

    def __create_directory(self, directory):
        try:
            if not exists(directory):
                mkdir(directory)
            return True

        except Exception as e:
            print(f"\n\nLine Number: 16\nError occurred: {e}")
            return False

    def __mount_iso_file(self):
        if not self.__create_directory(self.__iso_mountpoint):
            # TODO show dialog box that an error occurred!
            exit()
        check_output(["sudo", "mount", f"{self.__file_path}", f"{self.__iso_mountpoint}"])

    def __unmount_iso_file(self):
        try:
            check_output(["sudo", "umount", f"{self.__iso_mountpoint}"])
        except Exception as e:
            # TODO show dialog box that an error occurred!
            print(f"\n\nLine Number: 32\nError occurred: {e}")

        try:
            if exists(self.__iso_mountpoint):
                rmdir(self.__iso_mountpoint)
        except Exception as e:
            # TODO show dialog box that an error occurred!
            print(f"\n\nLine Number: 38\nError occurred: {e}")

    def __convert_wim_to_swm(self):
        try:
            check_output(["wimlib-imagex", "split", f"{self.__iso_mountpoint}/sources/install.wim", f"{self.__drive_path}/sources/install.swm", "4000"])
        except Exception as e:
            # TODO show dialog box that an error occurred!
            print(f"\n\nLine Number: 47\nError occurred: {e}")
