class Buttons:

    # Buttons of Main Window Dialog/
    # TODO define working of buttons in Main Window Dialog.

    def __init__(self, window):
        self.__main_window = window
        self.__file_name = None
        self.__file_path = None
        self.__drive_name = None
        self.__drive_path = None

    def add_iso_file(self):
        pass

    def select_usb_drive(self):
        pass

    def start_flash_button(self):
        pass

    def refresh_drive_table(self):
        pass

    def remove_file_button(self):
        pass

    def change_drive_button(self):
        pass

    def apply_btn_in_drive_frame(self):
        pass

    def cancel_btn_in_drive_frame(self):
        pass

    # Buttons of Flash Screen dialog.
    # TODO define working of buttons in Flash Screen Dialog.

    def go_back_button(self):
        pass

    def cancel_flash_button(self):
        pass

    # Getters & Setters

    def get_file_name(self):
        return self.__file_name

    def get_file_path(self):
        return self.__file_path

    def get_drive_name(self):
        return self.__drive_name

    def get_drive_path(self):
        return self.__drive_path
