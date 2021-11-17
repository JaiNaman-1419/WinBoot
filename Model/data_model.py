from os.path import join


class Data:

    def __init__(self):

        self.__file_name = None
        self.__file_path = None
        self.__drive_name = None
        self.__drive_path = None
        self.__drive_device = None
        self.__iso_mount_point = "/media/Windows/"

    # Setters of Data Model

    def set_file_name(self, file_name):
        self.__file_name = file_name

    def set_file_path(self, file_path):
        self.__file_path = file_path

    def set_drive_name(self, drive_name):
        self.__drive_name = drive_name

    def set_drive_path(self, drive_path):
        if drive_path is not None:
            self.__drive_path = join(drive_path, "WINDOWS")
            return
        self.__drive_path = drive_path

    def set_drive_device(self, drive_device):
        self.__drive_device = drive_device

    # Getters of Data Model

    def get_file_name(self):
        return self.__file_name

    def get_file_path(self):
        return self.__file_path

    def get_drive_name(self):
        return self.__drive_name

    def get_drive_path(self):
        return self.__drive_path

    def get_drive_device(self):
        return self.__drive_device

    def get_iso_mount_point(self):
        return self.__iso_mount_point
