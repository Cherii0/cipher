import os
from file_handler import FileHandler
from cipher import CipherManager
from menu import Menu

class Manager:

    def __init__(self, menu : Menu, file_h : FileHandler, cipher : CipherManager):
        self.file_handler = file_h
        self.menu = menu
        self.cipher = cipher

    def execute(self):
        os.system("cls")
        self.menu.menu()
        while True:
            choice = int(input("Provide choice : "))
            os.system("cls")
            match choice:
                case 1:
                    self.menu.managed_files()
                case 2:
                    self.menu.cipher()
                case 3:
                    self.menu.decipher()
                case 4:
                    self.menu.about()
                case 5:
                    self.menu.exit()
                case _:
                    pass
            self.menu.menu()
