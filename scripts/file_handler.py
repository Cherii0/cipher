import re
import os
import time
from text import Text

TIME_SLEEPER = 2

class FileHandler:
    def __init__(self, files_catalog : str):
        self.files_catalog = files_catalog

        # collections of objects
        self.cipher_objs = dict()
        self.non_cipher_objs = dict()
        self.both_ver_objs = dict()


        # collections for file system - stores filepath not actual objects
        self._cipher_filepaths = []
        self._non_cipher_filepaths = []
        self._both_ver_filepaths = []
        self._untracked_filepaths = []

    # GETTERS

    @property
    def cipher_filepaths(self):
        self._cipher_filepaths.clear()
        for obj in self.cipher_objs:
            self._cipher_filepaths.append(obj.key())
        return self._cipher_filepaths

    @property
    def non_cipher_filepaths(self):
        self._non_cipher_filepaths.clear()
        for obj in self.non_cipher_objs:
            self.non_cipher_filepaths.append(obj.key())
        return self._non_cipher_filepaths

    @property
    def both_ver_filepaths(self):
        self._non_cipher_filepaths.clear()
        for obj in self.both_ver_objs:
            self._both_ver_filepaths.append(obj.key())
        return self._both_ver_filepaths

    @property
    def untracked_filepaths(self):
        self._untracked_filepaths.clear()
        filepaths = self.collect_all_filepaths()
        tracked = self.cipher_filepaths + self.non_cipher_filepaths + self.both_ver_filepaths
        for filepath in filepaths:
            if filepaths not in tracked:
                self._untracked_filepaths.append(filepath)
        return self._untracked_filepaths







    def update_cipher_objs(self, **kwargs):
        filepath = kwargs.get("filepath")
        content = kwargs.get("content")
        method = kwargs.get("method")
        if isinstance(filepath, str):
            if isinstance(content, str):
                text_obj = Text(_content = content, _rot_type=method, _encrypted=True)
                self._non_cipher_objs.update({filepath : text_obj})


    def update_non_cipher_objs(self, **kwargs):
        filepath = kwargs.get("filepath")
        content = kwargs.get("content")
        if isinstance(filepath, str):
            if isinstance(content, str):
                text_obj = Text(content)
                self._non_cipher_objs.update({filepath : text_obj})

    @staticmethod
    def append(filepath : str, content : str):
        with open(file = filepath, mode = "a", encoding="UTF-8") as file:
            file.write("\n")
            file.write(content)

    @staticmethod
    def write(filepath : str, content : str):
        with open(file = filepath, mode = "w", encoding="UTF-8") as file:
            file.write(content)

    def update_unknown_filepaths(self):
        self._unknown_status_filepaths.clear()
        filepaths = self.collect_all_filepaths()
        managed_filepaths = [self._cipher_objs.keys()] + [self._non_cipher_objs.keys()] + self._both_versions_filepaths
        for filepath in filepaths:
            if filepath not in managed_filepaths:
                self._unknown_status_filepaths.append(filepath)

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
        pass



    def choose_file(self, cipher : bool) -> str:
        self.update_texts_collections()
        if cipher:
            all_choices = [obj.file_path for obj in self.non_cipher_objs]
        else:
            all_choices = [obj.file_path for obj in self.cipher_objs]

        print(all_choices)
        choice = input("Provide file name to cipher : ")
        if choice not in all_choices:
            choice = input("Provide proper file name to cipher : ")
        return choice


    def show_cipher_files(self):
        pass


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






    def update(self, text_obj : Text):
        self.texts_collector.update({text_obj.file_path : text_obj})

