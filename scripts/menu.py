import sys
import re
import os

from file_handler import FileHandler
from cipher import CipherAlgorithm

class Menu:

    def __init__(self):
        pass

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


    def managed_files(self, file_handler : FileHandler):
        self.show_cipher_files(file_handler)
        self.show_non_cipher_files(file_handler)
        self.show_both_version_files(file_handler)
        self.show_unknown_status_files(file_handler)

    @staticmethod
    def show_cipher_files(file_handler : FileHandler) -> None:
        print("--------  CIPHER  ---------")
        print("\n")
        if file_handler.cipher_filepaths:
            for filepath in file_handler.cipher_filepaths:
                print(f"    * file  {filepath}" )
        else:
            print(f" * no cipher files in this system session")
        print("\n")

    @staticmethod
    def show_non_cipher_files(file_handler : FileHandler) -> None:
        print("------  NON CIPHER  -------")
        print("\n")
        if file_handler.non_cipher_filepaths:
            for filepath in file_handler.non_cipher_filepaths:
                print(f"    * file  {filepath}" )
        else:
            print(f" * no decipher files in this system session")
        print("\n")

    @staticmethod
    def show_both_version_files(file_handler : FileHandler) -> None:
        print("------  BOTH VERSIONS  ------")
        print("\n")
        if file_handler.both_versions_filepaths:
            for filepath in file_handler.both_versions_filepaths:
                print(f"    * file  {filepath}" )
        else:
            print(f" * no both versions files in this system session")
        print("\n")

    @staticmethod
    def show_unknown_status_files(file_handler : FileHandler) -> None:
        print("------  UNKNOWN STATUS  ------")
        print("\n")
        if file_handler.unknown_status_filepaths:
            for filepath in file_handler.unknown_status_filepaths:
                print(f"    * file  {filepath}" )
        else:
            print(f" * no unknown status files in this system session")
        print("\n")






    def cipher(self, cipher : CipherAlgorithm, file_handler : FileHandler):
        print("---------------------")
        print("       CIPHER        ")
        print("---------------------")
        print("1. from provided text")
        print("2. from file system")
        choice = input("Your choice : ")
        while choice not in ["1", "2"]:
            choice = input("Type proper choice : ")

        match int(choice):
            case 1:
                self.cipher_from_provided_text(cipher, file_handler)
            case 2:
                self.cipher_from_filesystem(cipher, file_handler)





    def cipher_from_filesystem(self, cipher : CipherAlgorithm, file_handler : FileHandler):

        avaliable_filepaths = file_handler.unknown_status_filepaths
        filepath = input("Provide filepath to cipher : ")
        while filepath not in avaliable_filepaths:
            filepath = input("Provide proper filepath to cipher : ")

        content = file_handler.read_file(filepath)
        file_handler.update_non_cipher_objs(filepath = filepath, content = content)

        content = cipher.check_input(content)
        method = cipher.method_choice()
        cipher_content = cipher.cipher_manager(method = method, content = content)
        print(f"Correspond cipher version : {cipher_content}")

        match self.choice_after_cipher_file():
            case 1:
                print(f"Provided content : {content}")
                print(f"Cipher  version  : {cipher_content}")
            case 2:
                file_handler.update_cipher_objs(filepath = filepath, content = cipher_content)
                file_handler.append(filepath, cipher_content)
            case 3:
                filepath = input("Provide file path : ")
                filepath = self.check_filepath(filepath, file_handler)
                file_handler.update_cipher_objs(filepath = filepath, content = cipher_content)
                file_handler.write(filepath = filepath, content = cipher_content)



    @staticmethod
    def choice_after_cipher_file() -> int:

        print("----------------")
        print("Your options for further content processing :")
        print("1. Simply show cipher version")
        print("2. Save to same location\n")
        print("2. Save to new location\n")

        choice = input("Your choice : ")
        while choice not in ["1", "2", "3"]:
            choice = input("Your choice : ")
        return int(choice)


    @staticmethod
    def choice_after_cipher_text() -> int:

        print("----------------")
        print("Your options for further content processing :")
        print("1. Simply show cipher version")
        print("2. Save to new location\n")

        choice = input("Your choice : ")
        while choice not in ["1", "2"]:
            choice = input("Your choice : ")
        os.system("cls")
        return int(choice)

    @staticmethod
    def check_filepath(filepath : str, file_handler : FileHandler) -> str:

        pattern = r"(\w{1,})(\.)(txt|json)"
        all_filepaths = file_handler.collect_all_filepaths()

        while filepath in all_filepaths:
            print(f"File path {filepath} not allowed because it already exists")
            filepath = input("Provide file path : ")

        while not re.match(string = filepath, pattern = pattern):
            print("wrong filepath name")
            filepath = input("Provide file path : ")

        return filepath

    def cipher_from_provided_text(self, cipher : CipherAlgorithm, file_handler : FileHandler):
        cipher.show_tutorial()
        content = input("Provide text to cipher : ")
        content = cipher.check_input(content)
        method = cipher.method_choice()
        cipher_content = cipher.cipher_manager(content = content, method = method)
        print(f"Correspond cipher version : {cipher_content}")

        match self.choice_after_cipher_text():
            case 1:
                print(f"\nProvided content : {content}")
                print(f"Cipher  version  : {cipher_content}")
                input("\n\nPress any key to come back to menu... ")
                os.system("cls")
            case 2:
                filepath = input("Provide file path : ")
                filepath = self.check_filepath(filepath, file_handler)
                file_handler.update_non_cipher_objs(filepath = filepath, content = content)

















    def decipher(self):
        pass

    @staticmethod
    def about():
        print("about")
        input("\n\n Press any to come back to menu... ")

    @staticmethod
    def exit():
        sys.exit()






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


