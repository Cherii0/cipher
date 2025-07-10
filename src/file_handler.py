import re
import os
import time
from text import Text

TIME_SLEEPER = 2


class FileHandler:
    def __init__(self, files_catalog : str):
        self.content, self.cipher_content = None, None

    @staticmethod
    def show_avaliable_paths():
        print("AVALIABLE FILES : ")
        for file in os.listdir():
            print(file)


    # ---------------------------------------- READ / WRITE METHODS ----------------------------------------

    @staticmethod
    def read_file(filepath : str) -> str:
        content = ""
        char = True
        with open(file=filepath, mode="r", encoding="UTF-8") as file:
            while char:
                char = file.read(1)
                if not char.isascii():
                    char = "*"
                elif re.match(pattern = r"[\n]", string = char):
                    char = " "
                content += char
        print(f"\nfile {filepath} loaded\n")
        return content

    @staticmethod
    def append(filepath : str, content : str):
        with open(file = filepath, mode = "a", encoding="UTF-8") as file:
            file.write("\n")
            file.write(content)

    @staticmethod
    def write(filepath : str, content : str):
        with open(file = filepath, mode = "w", encoding="UTF-8") as file:
            file.write(content)


    # ---------------------------------------- MANAGE FILES METHODS ----------------------------------------

    def managed_files(self):
        print("\n")
        self.show_cipher_files()
        self.show_non_cipher_files()
        self.show_both_version_files()
        self.show_untracked_files()
        input("\nPress any key to comeback to menu...")
        os.system("cls")

    def show_cipher_files(self) -> None:
        print("--------  CIPHER  ---------")
        print("\n")
        if self.cipher_filepaths:
            for filepath in self.cipher_filepaths:
                print(f" * file  {filepath}" )
        else:
            print(f" * no cipher files in this system session")
        print("\n")

    def show_non_cipher_files(self) -> None:
        print("------  NON CIPHER  -------")
        print("\n")
        if self.non_cipher_filepaths:
            for filepath in self.non_cipher_filepaths:
                print(f" * file  {filepath}" )
        else:
            print(f" * no decipher files in this system session")
        print("\n")

    def show_both_version_files(self) -> None:
        print("------  BOTH VERSIONS  ------")
        print("\n")
        if self.both_ver_filepaths:
            for filepath in self.both_ver_filepaths:
                print(f" * file  {filepath}" )
        else:
            print(f" * no both versions files in this system session")
        print("\n")

    def show_untracked_files(self) -> None:
        print("------  UNTRACKED FILES  ------")
        print("\n")
        if self.untracked_filepaths:
            for filepath in self.untracked_filepaths:
                print(f" * file  {filepath}" )
        else:
            print(f" * no unknown status files in this system session")
        print("\n")


    # ---------------------------------------- SAVING METHODS ----------------------------------------

    def update_content(self, content : str, cipher_content : str) -> None:
        self.content = content
        self.cipher_content = cipher_content

    def collect_all_filepaths(self) -> list:
        os.chdir(self.files_catalog)
        files =  os.listdir()
        p = r"(?P<file_path>\w{1,})(\.)(?P<extension>txt|json)"
        files_filtered = []
        for file in files:
            match = re.match(pattern = p, string = file)
            if match:
                files_filtered.append(match.string)
        return files_filtered


    def check_filepath(self, filepath : str) -> str:

        pattern = r"(\w{1,})(\.)(txt|json)"
        all_filepaths = self.collect_all_filepaths()

        while filepath in all_filepaths:
            print(f"File path {filepath} not allowed because it already exists")
            filepath = input("Provide file path : ")

        while not re.match(string = filepath, pattern = pattern):
            print("wrong filepath name")
            filepath = input("Provide file path : ")

        return filepath

    def save_noncipher(self, filepath : str) -> None:
        self.update_non_cipher_objs(filepath=filepath, content=self.content)
        self.write(filepath=filepath, content=self.content)

    def save_cipher(self, filepath : str) -> None:
        self.update_cipher_objs(filepath=filepath, content=self.cipher_content)
        self.write(filepath=filepath, content=self.cipher_content)

    def save_both_sep_loc(self, filepath : str) -> None:
        self.update_non_cipher_objs(filepath=filepath, content=self.content)
        self.write(filepath=filepath, content=self.content)
        filepath = input("Provide another file path : ")
        filepath = self.check_filepath(filepath)
        self.update_cipher_objs(filepath=filepath, content=self.cipher_content)
        self.write(filepath=filepath, content=self.cipher_content)

    def save_both_same_loc(self, filepath : str) -> None:
        content_con = self.content+self.cipher_content
        self.update_both_ver_objs(filepath=filepath, content=content_con)
        self.write(filepath=filepath, content=content_con)


    # ---------------------------------------- TEXT OBJECT CREATION ----------------------------------------

    def update_both_ver_objs(self, **kwargs):
        filepath, content, method = kwargs.get("filepath"),  kwargs.get("content"), kwargs.get("method")
        if isinstance(filepath, str) and isinstance(content, str):
            text_obj = Text(_content = content, _rot_type=method, _encrypted=True)
            self.both_ver_objs.update({filepath : text_obj})

    def update_cipher_objs(self, **kwargs):
        filepath, content, method = kwargs.get("filepath"),  kwargs.get("content"), kwargs.get("method")
        if isinstance(filepath, str) and isinstance(content, str):
            text_obj = Text(_content = content, _rot_type=method, _encrypted=True)
            self.cipher_objs.update({filepath : text_obj})

    def update_non_cipher_objs(self, **kwargs):
        filepath, content = kwargs.get("filepath"), kwargs.get("content")
        if isinstance(filepath, str) and isinstance(content, str):
            text_obj = Text(_content = content, _encrypted=False)
            self.non_cipher_objs.update({filepath : text_obj})

