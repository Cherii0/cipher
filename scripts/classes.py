import string
from dataclasses import dataclass, field
import re
import os
import time

TIME_SLEEPER = 2

def iter_func(max):
    for n in range(1, max+1):
        yield n


@dataclass
class Text:
    _file_path : str = None
    _content : str = None
    _rot_type : str = field(init = False, default = None)
    _encrypted : bool = field(init = False, default = False)

    @property
    def content(self):
        return self._content

    @property
    def file_path(self):
        return self._file_path

    @property
    def encrypted(self):
        return self._encrypted

    @encrypted.setter
    def encrypted(self, value : bool):
        self._encrypted = value

    @property
    def rot_type(self):
        return self._rot_type

    @rot_type.setter
    def rot_type(self, value : str):
        self._rot_type = value



class FileHandler:

    def __init__(self):
        self.texts_collector = dict()
        self.cipher_objs, self.non_cipher_objs = [], []

    def get_text(self, file_path : str) -> Text | None:
        if file_path in self.texts_collector.keys():
            return self.texts_collector[file_path]
        return None

    def split_text_objects(self):
        cipher, non_cipher = [], []
        for text_obj in self.texts_collector.values():
            if text_obj.encrypted:
                cipher.append(text_obj)
            else:
                non_cipher.append(text_obj)
        return cipher, non_cipher



    def sort_text_objs(self, cipher : list, non_cipher : list) -> None:
        cipher.sort(key = lambda obj : obj.file_path)
        non_cipher.sort(key = lambda obj : obj.file_path)



    def choose_file(self, cipher : bool) -> str:
        if cipher:
            all_choices = self.non_cipher_objs
        else:
            all_choices = self.cipher_objs

        choice = input("Provide file name to cipher : ")
        if choice not in all_choices:
            choice = input("Provide proper file name to cipher : ")
        return choice


    def show_cipher_files(self):
        print("--------  CIPHER  ---------")
        print("\n")
        if self.cipher_objs:
            for text_obj in self.cipher_objs:
                print(f"    * file  {text_obj.file_path} has been cipher in location : ???" )
        else:
            print(f" * no cipher file in this system session")
        print("\n")

    def show_non_cipher_files(self):
        print("------  NON CIPHER  -------")
        print("\n")
        for text_obj in self.non_cipher_objs:
            print(f"    * file {text_obj.file_path}")



    def show_no_files_info(self):
            print("\n----------------------------")
            print("there is no files loaded yet")
            print("----------------------------")
            time.sleep(TIME_SLEEPER)
            os.system("cls")

    def show_file_system(self):
        if not self.texts_collector:
            self.show_no_files_info()
            return None

        self.cipher_objs, self.non_cipher_objs = self.split_text_objects()
        self.sort_text_objs(self.cipher_objs, self.non_cipher_objs)

        print("\n")
        print(" loaded files into system :")
        print("\n")
        self.show_cipher_files()
        self.show_non_cipher_files()
        print("\n")
        input("Press any key to go back... ")
        os.system("cls")
        return None



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
        self.texts_collector.update({file_path : text_obj})
        print("-------------------------")
        print(f"file {file_path} loaded")
        time.sleep(1.5)

    def update(self, text_obj : Text):
        self.texts_collector.update({text_obj.file_path : text_obj})



class CipherAlgorithm:

    def __init__(self, file_handler : FileHandler):
        self.file_handler = file_handler
        self.rot13_offset = 13


    def check_input(self, content : str) -> str | None:

        if not content:
            return None

        non_latin_chars = []
        non_latin_index = []
        for (idx, c) in enumerate(content, start=0):
            if c not in string.ascii_lowercase:
                if c == " ":
                    non_latin_chars.append("space")
                else:
                    non_latin_chars.append(c)
                non_latin_index.append(idx)


        if not non_latin_chars:
            return content


        print("\n")
        print("Found non allowed characters at given positions : \n")
        for (char_, pos_) in zip(non_latin_chars, non_latin_index):
            print(f"{char_} : {pos_}")
        print("\n")
        replace = input("Change above occurrences with '*' ? YES\\NO : ")
        print("\n")
        if replace:
            non_cipher_content_replaced = list(content)
            for pos_ in non_latin_index:
                non_cipher_content_replaced[pos_] = "*"
            non_cipher_content_replaced = "".join(non_cipher_content_replaced)
        else:
            return None

        try:
            print(f"Provided content after correction : \n")
            print(f"  {non_cipher_content_replaced}\n")
        except NameError:
            pass

        return non_cipher_content_replaced

    def perform_rot13(self, content : str) -> str:

        latin_bgn = 0
        latin_end = 26

        latin_codes = [c for c in range(latin_bgn, latin_end)]
        latin_letters_dict = {char_: code_ for (char_, code_) in zip(string.ascii_lowercase, latin_codes)}
        latin_codes_dict = {code_ : char_ for (char_, code_) in latin_letters_dict.items()}

        non_cipher_content_codes = []
        for char_ in content:
            if char_ != "*":
                non_cipher_content_codes.append(latin_letters_dict[char_])
            else:
                non_cipher_content_codes.append(None)

        cipher_content_codes = []
        for code_ in non_cipher_content_codes:
            if not code_:
                cipher_content_codes.append(None)
                continue
            if code_ < self.rot13_offset:
                cipher_content_codes.append(code_ + self.rot13_offset)
            else:
                cipher_content_codes.append(code_ - self.rot13_offset)

        cipher_content = []
        for code_ in cipher_content_codes:
            if not code_:
                cipher_content.append("*")
            else:
                cipher_content.append(latin_codes_dict[code_])

        return "".join(cipher_content)



    def cipher(self, content : str) -> str | None:
        """
        takes decipher content and returns cipher version
        runs proper rot cipher
        """

        if not content:
            return None

        method_choice = input("Your method declaration rot13/rot47: ")
        if method_choice == "rot13":
            content = self.check_input(content)
            if not content:
                print("\nthere is no content to cipher\n")
                return None
            cipher_content = self.perform_rot13(content)

        print(f"Correspond cipher version : {cipher_content}")

        # TODO write to file with file_path = cipher_path and content =
        # TODO whatever comes from cipher algorithm

        print("file has been cipher...")
        time.sleep(2)
        return cipher_content




    def show_tutorial(self):
        print("\n")
        print(" * for method rot13 provide  content that contains only letters A-Z not even space allowed\n")
        print(" * for method rot47 provide only content that contains ASCII characters\n\n")


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
        print("1. load file into file-system")
        print("2. show managed files")
        print("3. cipher file")
        print("4. decipher file")
        # print("4. create file")

        print("6. about program")
        print("---------------------")

    @staticmethod
    def show_about():
        print("about")

    def cipher_file(self):
        self.file_handler.show_non_cipher_files()
        file_path = self.file_handler.choose_file(cipher = True)
        choosen_text_obj_content = self.file_handler.texts_collector.get(file_path).content
        cipher_content = self.cipher.cipher(choosen_text_obj_content)
        cipher_obj = Text(file_path, cipher_content)
        self.file_handler.update(cipher_obj)

    def decipher_file(self):
        self.file_handler.show_cipher_files()
        self.file_handler.choose_file(cipher = False)
        # self.cipher.decipher(file_path)


    def show_cipher_tab(self):
        """
        prints out avaliable files, then ensures proper
        file name to cipher, saves ciper version into given path
        """

        self.choose_file()

        all_paths = []
        for attr in self.file_handler.texts_collector.values():
            if not attr.encrypted:
                all_paths.append(attr.file_path)

        file_to_cipher= input("Provide file name to cipher : ")

        while file_to_cipher not in all_paths:
            file_to_cipher = input("Provide proper file name to cipher : ")

        text_obj_to_cipher = None
        for text_obj_path, attr in self.file_handler.texts_collector.items():
            if attr.file_path == file_to_cipher:
                text_obj_to_cipher = self.file_handler.texts_collector.get(text_obj_path)
                break


        cipher_file_path = input(f"Provide file name to write {file_to_cipher} cipher version : ")
        try :
            content_cipher = self.cipher.cipher(text_obj_to_cipher.content)
        except AttributeError:
            return None

        cipher_text_obj = Text(cipher_file_path, content_cipher)
        self.file_handler.texts_collector.update({cipher_file_path : cipher_text_obj})
        return None

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

        print("\n\navaliable files")
        for idx, file in self.files_filtered.items():
            print(f"{idx} - {file}")
            if idx == ff_len:
                print(f"{idx+1} - back")

    def choose_file(self):
        self.show_avaliable_files()
        ff_len = len(self.files_filtered)
        choice = int(input("Provide file path choice : "))
        if ff_len+1 == choice:
            return None
        return self.files_filtered[choice]

    def show_create_tab(self):
        print("---------------------")
        print("     CREATE FILE     ")
        print("---------------------")
        self.cipher.show_tutorial()
        content = input("Provide content to cipher : ")
        content = self.cipher.check_input(content)
        file_path = input("Provide file path for non cipher version : ")
        choice = input("Combine both cipher and non cipher versions into one file?\nType YES\\NO : ")

        obj = Text(file_path, content)
        self.file_handler.update(obj)

        if choice.upper() == "NO":
            cipher_file_path = input("Provide file path for cipher version : ")
            self.cipher.cipher(cipher_file_path, obj)
        else:
            self.cipher.cipher(file_path, obj)

        os.system("cls")

    def load_file(self):
        file_path = self.choose_file()
        if not file_path:
            return
        else:
            self.file_handler.read_file(file_path)
        os.system("cls")

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
                    self.menu.load_file()
                case 2:
                    self.file_handler.show_file_system()
                case 3:
                    self.menu.cipher_file()
                case 4:
                    self.menu.decipher_file()
                case 5:
                    self.menu.show_about()
                case _:
                    break
            self.menu.show_menu()

