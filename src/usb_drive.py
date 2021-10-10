from psutil import disk_partitions
from subprocess import check_output
from re import match, search, split


class DriveProperties:

    def __init__(self):
        self.__disks = dict()
        self.__disk_count = None
        self.__disk_names = dict()

    def __get_usb_list(self):
        pattern = r"/dev/sd[b-z]"
        disk_list = disk_partitions()
        for disk in disk_list:
            if match(pattern, disk.device):
                self.__disks[disk.device] = disk.mountpoint

        self.__disk_count = len(self.__disks.keys())

    def __get_usb_model(self):

        if self.__disks is None:
            print("Disk list is Empty!")
            return

        disk_number = 0

        try:
            device_model_list = check_output(["pkexec", "fdisk", "-l"]).decode('utf-8').split('\n')
        except Exception:
            device_model_list = None

        if device_model_list is None:
            return

        for index, device in enumerate(device_model_list):
            if disk_number < self.__disk_count:
                for disk in list(self.__disks.keys())[disk_number:]:
                    device_pattern = fr"Disk {disk[:-1]}: (.*B),"
                    model_pattern = r"Disk model: (.*)"
                    if search(device_pattern, device):
                        disk_number += 1
                        size = split(device_pattern, device)[1].strip()
                        self.__disk_names[disk] = {f"{size}": f"{split(model_pattern, device_model_list[index+1])[1].strip()}"}
                        break

            else:
                return

    def get_disk_properties(self):
        self.__get_usb_list()
        self.__get_usb_model()

    def get_disk_count(self):
        print(self.__disk_count)
        return self.__disk_count

    def reduce_disk_count(self):
        if self.__disk_count > 0:
            self.__disk_count -= 0

    def get_disk_list(self):
        return self.__disks

    def remove_dictionary_element(self):
        self.__disks.popitem()
        self.__disk_names.popitem()

    def get_disk_names_list(self):
        return self.__disk_names
