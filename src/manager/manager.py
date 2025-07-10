import sys
import re
import os
import time
from src.cipher.manager import CipherManager
from src.file_handler import FileHandler
from src.manager import cipher


class Manager:
    def __init__(self, file_handler : FileHandler, cipher_manager : CipherManager):
        self.cipher_manager = cipher_manager
        self.file_handler = file_handler
        self.content, self.cipher_content = None, None

    def execute(self):
        self.menu()
        while True:
            choice = int(input("Provide choice : "))
            os.system("cls")
            match choice:
                case 1:
                    self.managed_files()
                case 2:
                    self.cipher()
                case 3:
                    self.decipher()
                case 4:
                    self.about()
                case 5:
                    self.exit()
                case _:
                    pass
            self.menu()

    @staticmethod
    def menu():
        print("---------------------")
        print("|        MENU       |")
        print("---------------------")
        print("1. managed files")
        print("2. cipher")
        print("3. decipher")
        print("4. about program")
        print("5. exit")
        print("---------------------")

    # ---------------------------------------- CIPHER METHODS ----------------------------------------

    def cipher(self):
        """
        decide how user will provide content
        args : None
        return : None
        """

        match self.show_cipher_options():
            case 1:
                self.from_provided_text()
            case 2:
                self.from_filesystem()

    @staticmethod
    def show_cipher_options() -> int:
        print("---------------------")
        print("|      CIPHER       |")
        print("---------------------")
        print("1. from provided text")
        print("2. from file system")
        print("---------------------")
        choice = input("Your choice : ")
        while choice not in ["1", "2"]:
            choice = input("Type proper choice : ")
        return int(choice)

    def from_provided_text(self):
        """
        runs cipher manager, stores both versions and decide which saving option execute
        args : None
        return : None
        """
        self.content, self.cipher_content = self.cipher_manager.execute()
        self.file_handler.update_content(self.content, self.cipher_content)

        os.system("cls")

        filepath = input("Provide file path : ")
        filepath = self.file_handler.check_filepath(filepath)

        match self.after_cipher_text():
            case 1:
                self.show_both_versions()
            case 2:
                self.file_handler.save_noncipher(filepath)
            case 3:
                self.file_handler.save_cipher(filepath)
            case 4:
                self.file_handler.save_both_sep_loc(filepath)
            case 5:
                self.file_handler.save_both_same_loc(filepath)
            case _:
                pass

        print("Operation done successfully... ")
        time.sleep(1.5)
        os.system("cls")
        self.content, self.cipher_content = None, None


    @staticmethod
    def after_cipher_text() -> int:

        print("\nYour options for further content processing :\n")
        print("1. Simply show both version")
        print("2. Save only non cipher to new location")
        print("3. Save only to new cipher location")
        print("4. Save to separate cipher and non cipher locations")
        print("5. Save into one file both versions\n")

        choice = input("Your choice : ")
        while choice not in ["1", "2", "3", "4", "5"]:
            choice = input("Your choice : ")
        os.system("cls")
        return int(choice)

    def show_both_versions(self):
        print(f"\nProvided content : {self.content}")
        print(f"Cipher  version  : {self.cipher_content}")
        input("\n\nPress any key to come back to menu... ")
        os.system("cls")

    def from_filesystem(self):
        self.file_handler.show_avaliable_paths()
        filepath = input("provide file path")
        content = self.file_handler.read_file(filepath)
        self.cipher_manager.execute(content=content)