from dataclasses import dataclass, field
import re
import os
import time

def iter_func(max):
    for n in range(1, max+1):
        yield n

class Menu:

    def __init__(self):
        self.files_filtered = dict()
        self.loaded_files_paths = []

    @staticmethod
    def show_menu():
        print("---------------------")
        print("        MENU        ")
        print("---------------------")
        print("1. read file")
        print("2. show loaded files")
        print("3. cipher file")
        print("4. about program")
        print("---------------------")

    @staticmethod
    def show_cipher_tab( texts_collection : dict) -> tuple:

        for key, value in texts_collection.items():
            print(key, value)


        print("loaded files status : ")
        print("----------------------")
        for file_path, file_obj in texts_collection.items():
            # TODO if ciphered then in what location
            if file_obj.encrypted:
                print(f"CIPHER version - {file_obj.cipher_path} | NON CIPHER - {file_path}")
            else:
                print(f"NON CIPHER - {file_path}")


        print("\n")
        file_to_cipher = input("Provide file name to cipher : ")
        while file_to_cipher not in texts_collection.keys():
            os.system("cls")
            file_to_cipher = input("Provide proper file name : ")
            if file_to_cipher == "4":
                break

        file_path_write = input(f"Provide file name to write {file_to_cipher} cipher version : ")

        return file_to_cipher, file_path_write





    def show_avaliable_files(self):
        os.chdir("../cipher_files")
        files =  os.listdir()

        idx_gen = iter_func(len(files))
        p = r"(?P<file_path>\w{1,})(\.)(?P<extension>txt|json)"

        for file in files:
            match = re.match(pattern = p, string = file)
            if match:
                self.files_filtered.update({next(idx_gen): match.string})
        ff_len = len(self.files_filtered)

        Menu.show_read_tab()
        print("avaliable files")
        for idx, file in self.files_filtered.items():
            print(f"{idx} - {file}")
            if idx == ff_len:
                print(f"{idx+1} - back")

        choice = int(input("Provide file path : "))
        if ff_len+1 == choice:
            return None
        return self.files_filtered[choice]


    @staticmethod
    def show_read_tab():
        print("---------------------")
        print("      READ MENU        ")
        print("---------------------")

@dataclass
class Text:
    __file_path_non_cipher : str
    __file_path_cipher : str

    __content_non_cipher : str
    __content_cipher : str

    #__content_non_cipher : str = field(repr = False, init = True)
    #__content_cipher : str = field(repr = False, init = False)

    __encrypted : bool
    __rot_type : str






    @property
    def content_cipher(self):
        return self.__content_cipher

    @content_cipher.setter
    def content_cipher(self, value : str):
        self.__content_cipher = value



    @property
    def cipher_path(self):
        return self.__file_path_cipher

    @cipher_path.setter
    def cipher_path(self, value : str):
        self.__file_path_cipher = value


    @property
    def non_cipher_file_path(self):
        return self.__file_path_non_cipher


    @property
    def encrypted(self):
        return self.__encrypted

    @encrypted.setter
    def encrypted(self, value : bool):
        self.__encrypted = value




class CipherAlgorithm:

    def __init__(self):
        pass

    @staticmethod
    def cipher(cipher_path : str, text_obj : Text):
        """
        Cipher path is guaranteed proper
        Text object changed in place
        """

        text_obj.cipher_path = cipher_path
        text_obj.content_cipher = "CIPHED concent"
        text_obj.encrypted = True

        # TODO write to file with file_path = cipher_path and content =
        # TODO whatever comes from cipher algorithm






class FileHandler:

    def __init__(self):
        self.texts_collector = dict()

    def get_text(self, file_path : str) -> Text | None:
        if file_path in self.texts_collector.keys():
            return self.texts_collector[file_path]
        return None

    def describe(self) -> None:
        if not self.texts_collector:
            print("----------------------------")
            print("there is no files loaded yet")
            print("----------------------------")
            time.sleep(2)
        else:
            print("loaded files into system : ")
            for text in self.texts_collector.values():
                print(f" - {text.non_cipher_file_path}")
            print("\n")
            input("Press any key to go back... ")
        os.system("cls")


    def read_file(self, file_path : str) -> None :
        """
        read file from given filepath and append to texts collector
        """
        text = ""
        char = True

        with open(file=file_path, mode="r", encoding="UTF-8") as file:

            # string not empty
            while char:
                char = file.read(1)
                if not char.isascii():
                    char = "*"
                elif re.match(pattern = r"[\n]", string = char):
                    char = " "

                text += char

        self.texts_collector.update({file_path : Text(file_path, "", text, "", False, "rot32" )})
        print("-------------------------")
        print(f"file {file_path} loaded")
        time.sleep(1)


class Manager:

    def __init__(self, menu : Menu, file_h : FileHandler, cipher : CipherAlgorithm):
        self.menu = menu if Menu else Menu()
        self.file_handler = file_h if file_h else FileHandler()
        self.cipher = cipher if cipher else CipherAlgorithm()

    def execute(self):
        os.system("cls")
        self.menu.show_menu()
        while True:
            choice = int(input("Provide choice : "))
            os.system("cls")
            match choice:
                case 1:
                    file_path = self.menu.show_avaliable_files()
                    if not file_path:
                        pass
                    else:
                        self.file_handler.read_file(file_path)
                    os.system("cls")
                case 2:
                    self.file_handler.describe()
                case 3:
                    file_path_to_cipher, file_path_ciphered = self.menu.show_cipher_tab(self.file_handler.texts_collector)
                    obj = self.file_handler.texts_collector[file_path_to_cipher]
                    self.cipher.cipher(file_path_ciphered, obj) # in place
                case _:
                    break

            self.menu.show_menu()
