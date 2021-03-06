from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog
from src.buttons import Buttons


class FlashScreen(QDialog):

    def __init__(self, widget_obj, drive_obj, data_obj):
        super(FlashScreen, self).__init__()

        # Loading UI
        loadUi("./ui/flash_screen.ui", self)

        # class objects or references
        self.__data = data_obj
        self.__flash_button = Buttons(widget_obj, drive_obj)

        # Class Method calls
        self.flash_auto_call_methods()

    def flash_auto_call_methods(self):
        self.completed_button.hide()
        self.flash_button_connectors()

    def flash_button_connectors(self):
        self.cancel_button.clicked.connect(lambda: self.__flash_button.cancel_flash_button())
        self.completed_button.clicked.connect(lambda: self.__flash_button.completed_flash_button(self))
