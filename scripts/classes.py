from dataclasses import dataclass, field
import re
import os
import time

def iter_func(max):
    for n in range(1, max+1):
        yield n


@dataclass
class Text:
    __file_path_non_cipher : str
    __file_path_cipher : str = field(init = False, default = None)

    __content_non_cipher : str
    __content_cipher : str = field(init = False, default = None)

    __rot_type : str = field(init = False, default = None)
    __encrypted : bool = field(init = False, default = False)

    # properties used inside cipher function in order to change objects attr in place
    @property
    def file_path_non_cipher(self):
        return self.__file_path_non_cipher

    @property
    def file_path_cipher(self):
        return self.__file_path_cipher

    @file_path_cipher.setter
    def file_path_cipher(self, value : str):
        self.__file_path_cipher = value

    @property
    def encrypted(self):
        return self.__encrypted

    @encrypted.setter
    def encrypted(self, value : bool):
        self.__encrypted = value


    @property
    def content_cipher(self):
        return self.__content_cipher

    @content_cipher.setter
    def content_cipher(self, value : str):
        self.__content_cipher = value


    @property
    def rot_type(self):
        return self.__rot_type

    @rot_type.setter
    def rot_type(self, value : str):
        self.__rot_type = value

    @property
    def path(self):
        if self.encrypted:
            return self.__file_path_cipher
        else:
            return self.__file_path_non_cipher


class FileHandler:

    def __init__(self):
        self.texts_collector = dict()

    def get_text(self, file_path : str) -> Text | None:
        if file_path in self.texts_collector.keys():
            return self.texts_collector[file_path]
        return None



    def describe(self) -> None:
        if not self.texts_collector:
            print("\n----------------------------")
            print("there is no files loaded yet")
            print("----------------------------")
            time.sleep(2)
            os.system("cls")
            return None


        # TODO split into cipher status
        # TODO sort prining
        # TODO split this func into multiple funcs

        cipher_objs = []
        non_cipher_objs = []


        for text_obj in self.texts_collector.values():
            if text_obj.encrypted:
                cipher_objs.append(text_obj)
            else:
                non_cipher_objs.append(text_obj)

        cipher_objs.sort(key = lambda obj : obj.path)
        non_cipher_objs.sort(key = lambda obj : obj.path)



        print("\n")
        print(" loaded files into system :")
        print("\n")
        print("--------  CIPHER  ---------")
        print("\n")
        if cipher_objs:
            for text_obj in cipher_objs:
                print(f"    * file  {text_obj.file_path_non_cipher} has been cipher in location : {text_obj.file_path_cipher}" )
        else:
            print(f" * no cipher file in this system session")
        print("\n")
        print("------  NON CIPHER  -------")
        print("\n")
        for text_obj in non_cipher_objs:
            print(f"    * file {text_obj.file_path_non_cipher}")



        print("\n")
        input("Press any key to go back... ")
        os.system("cls")


    def read_file(self, file_path : str) -> None :
        """
        read file from given filepath and append to texts collector
        """
        content = ""
        char = True

        with open(file=file_path, mode="r", encoding="UTF-8") as file:

            # string not empty
            while char:
                char = file.read(1)
                if not char.isascii():
                    char = "*"
                elif re.match(pattern = r"[\n]", string = char):
                    char = " "

                content += char

        text_obj = Text(file_path, content)
        self.texts_collector.update({id(text_obj) : text_obj})
        print("-------------------------")
        print(f"file {file_path} loaded")
        time.sleep(1.5)

    def update(self, text_obj : Text):
        self.texts_collector.update({id(text_obj) : text_obj})



class CipherAlgorithm:

    def __init__(self, file_handler : FileHandler):
        self.file_handler = file_handler

    def cipher(self, cipher_path : str, text_obj : Text):
        """
        Cipher path is guaranteed proper
        Text object changed in place
        """

        text_obj.file_path_cipher = cipher_path
        text_obj.content_cipher = "CIPHED concent"
        text_obj.encrypted = True
        text_obj.rot_type = "rot32"

        # TODO write to file with file_path = cipher_path and content =
        # TODO whatever comes from cipher algorithm

        print("file has been cipher...")
        time.sleep(2)




class Menu:

    def __init__(self, cipher : CipherAlgorithm, file_h : FileHandler):
        self.files_filtered = dict()
        self.loaded_files_paths = []
        self.cipher = cipher
        self.file_handler = file_h

    @staticmethod
    def show_menu():
        print("---------------------")
        print("        MENU        ")
        print("---------------------")
        print("1. read file")
        print("2. cipher file")
        print("3. create file")
        print("4. show managed files")
        print("5. about program")
        print("---------------------")

    @staticmethod
    def show_about():
        print("about")


    def show_cipher_tab(self):
        """
        prints out avaliable files, then ensures proper
        file name to cipher, saves ciper version into given path
        """
        cipher_text_objs = []
        non_cipher_text_objs = []

        for text_obj in self.file_handler.texts_collector.values():
            if text_obj.encrypted:
                cipher_text_objs.append(f" * {text_obj.path} | NON CIPHER - {text_obj.file_path_non_cipher}")
            else:
                non_cipher_text_objs.append(f" * {text_obj.path}")

        # printing
        print("loaded files status : \n")
        print("CIPHER : \n")
        if not cipher_text_objs:
            print(" * missing cipher files in current session \n")
        else:
            for text_obj_desc in cipher_text_objs:
                print(text_obj_desc)

        print("\nNON CIPHER : \n")
        if not non_cipher_text_objs:
            print(" * missing non cipher files in current session \n")
        else:
            for text_obj_desc in non_cipher_text_objs:
                print(text_obj_desc)
        print("\n")


        # TODO cipher all at once
        if not non_cipher_text_objs:
            input("Press any key to back to menu... ")
            os.system("cls")
            return

        all_paths = []
        for attr in self.file_handler.texts_collector.values():
            all_paths.append(attr.file_path_non_cipher)

        file_to_cipher= input("Provide file name to cipher : ")


        while file_to_cipher not in all_paths:
            file_to_cipher = input("Provide proper file name to cipher : ")


        for obj_id, attr in self.file_handler.texts_collector.items():
            if attr.path == file_to_cipher:
                text_obj_to_cipher = self.file_handler.texts_collector.get(obj_id)
                break


        file_path_write = input(f"Provide file name to write {file_to_cipher} cipher version : ")
        self.cipher.cipher(file_path_write, text_obj_to_cipher)



    def show_avaliable_files(self):
        # TODO make indices
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

    def show_create_tab(self):
        print("---------------------")
        print("     CREATE FILE     ")
        print("---------------------")
        content = input("Provide content to cipher : ")
        file_path = input("Provide file path for non cipher version : ")
        choice = input("Combine both cipher and non cipher versions into one file?\nType YES\\NO : ")

        obj = Text(file_path, content)
        self.file_handler.update(obj)

        if choice.upper() == "NO":
            cipher_file_path = input("Provide file path for cipher version : ")
            self.cipher.cipher(cipher_file_path, obj)
        else:
            self.cipher.cipher(file_path, obj)







    @staticmethod
    def show_read_tab():
        print("---------------------")
        print("      READ MENU        ")
        print("---------------------")



class Manager:

    def __init__(self, menu : Menu, file_h : FileHandler, cipher : CipherAlgorithm):
        self.file_handler = file_h
        self.menu = menu
        self.cipher = cipher

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
                    self.menu.show_cipher_tab()
                case 3:
                    self.menu.show_create_tab()
                    os.system("cls")
                case 4:
                    self.file_handler.describe()
                case 5:
                    self.menu.show_about()
                case _:
                    break

            self.menu.show_menu()
