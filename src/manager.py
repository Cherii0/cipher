import os
from menu import Menu
from cipher_manager import CipherManager
from file_handler import FileHandler
import sys


class Manager:
    def __init__(self, menu : Menu, cipher_manager : CipherManager):
        self.menu = menu
        self.ciper_manager = cipher_manager
        self.content, self.cipher_content = None, None

    def execute(self):
        """
        execute menu front page and decide which functionality execute
        args : None
        return : None
        """
        while True:
            os.system("cls")
            match self.menu.show_front_menu():
                case 1:
                    pass
                case 2:
                    self.cipher("CIPHER")
                case 3:
                    self.decipher("DECIPHER")
                case 4:
                    self.menu.about("../about.txt")
                case 5:
                    sys.exit()
                case _:
                    pass

    def cipher(self, title : str):
        """
        decide how user will provide content
        args : None
        return : None
        """
        match self.menu.show_cipher_options(title):
            case 1:
                self.content, self.cipher_content = self.ciper_manager.execute(from_file = False)
                self.choice_saving()
            case 2:
                self.content, self.cipher_content =self.ciper_manager.execute(from_file = True)
                self.choice_saving()


    def decipher(self, title):
        self.cipher(title)


    def choice_saving(self):
        choice = self.menu.show_saving_choices()
        output_option = [1]
        single_filepath_option = [2,3,5]

        if choice in single_filepath_option:
            filepath = self.menu.type_saving_filepath()
            match choice:
                case 2:
                    FileHandler.write(filepath=filepath, content=self.content)
                case 3:
                    FileHandler.write(filepath=filepath, content=self.cipher_content)
                case 5:
                    content_concatenated = self.content+"\n"+self.cipher_content
                    FileHandler.write(filepath=filepath, content=content_concatenated)
                case _:
                    pass
        elif choice in output_option:
            match choice:
                case 1:
                    self.menu.show_both_versions(self.content, self.cipher_content)
                case _:
                    pass
        else:
            filepath_decipher, filepath_cipher = self.menu.type_saving_filepaths()
            match choice:
                case 4:
                    FileHandler.write(filepath=filepath_decipher, content=self.content)
                    FileHandler.write(filepath=filepath_cipher, content=self.content)
                case _:
                    pass
