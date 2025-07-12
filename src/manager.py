import os
from menu import Menu
from cipher_manager import CipherManager
from file_handler import FileHandler
import sys
from text_manager import Text
from text_manager import TextManager


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
                    self.managed_files()
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

    def managed_files(self):
        self.menu.managed_files()

    def cipher(self, title : str):
        """
        decide how user will provide content
        args : None
        return : None
        """
        if title == "CIPHER":
            TextManager.set_params(encrypted=False)
        else:
            TextManager.set_params(encrypted=True)

        match self.menu.show_cipher_options(title):
            case 1:
                self.content, self.cipher_content = self.ciper_manager.execute(from_file=False)
                if not self.content:
                    return
                self.choice_saving()
            case 2: # case 2 means from filesystem -> create text obj
                self.content, self.cipher_content = self.ciper_manager.execute(from_file=True)
                TextManager.set_params(filepath=CipherManager.get_current_filepath(), content=self.content)
                TextManager.create_obj()
                if not self.content:
                    return
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
                    TextManager.set_params(filepath=filepath)
                    TextManager.create_obj()
                case 3:
                    TextManager.set_params(filepath=filepath, content=self.cipher_content, rot_type=CipherManager.get_current_method(), encrypted=True)
                    TextManager.create_obj()
                    FileHandler.write(filepath=filepath, content=self.cipher_content)
                case 5:
                    self.content = self.content+"\n"+self.cipher_content
                    TextManager.set_params(filepath=filepath, content=self.content, encrypted=False, rot_type=None)
                    TextManager.create_obj()
                    FileHandler.write(filepath=filepath, content=self.content)
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
                    FileHandler.write(filepath=filepath_cipher, content=self.content)
                    TextManager.set_params(filepath=filepath_cipher, content=self.cipher_content, encrypted=True, rot_type=CipherManager.get_current_method())
                    TextManager.create_obj()
                    FileHandler.write(filepath=filepath_decipher, content=self.content)
                    TextManager.set_params(filepath=filepath_decipher, content=self.content, rot_type="", encrypted=False)
                    TextManager.create_obj()
                case _:
                    pass
