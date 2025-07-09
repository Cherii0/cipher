import sys
import re
import os
import time
from file_handler import FileHandler
from cipher import CipherManager


class Menu:
    def __init__(self, file_handler: FileHandler, cipher: CipherManager):
        self.file_handler = file_handler
        self.cipher_manager = cipher
        self.content = None
        self.cipher_content = None

    # ---------------------------------------- CIPHER METHODS ----------------------------------------

    def cipher(self):
        """
        decide how user will provide content
        args : None
        return : None
        """




        match Menu.show_cipher_options():
            case 1:
                self.cipher_from_provided_text()
            case 2:
                self.cipher_from_filesystem()



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


    # dekorator?
    def cipher_from_provided_text(self):
        """
        runs cipher manager, stores both versions and decide which saving option execute
        parameters : None
        return : None
        """

        # create new cipher object using factory method

        # run objects shift method that covers its class methods - then we dont have to execute all methods
        # that can differ from eachother

        self.content, self.cipher_content = CipherManager.encrypt_from_given_content()
        os.system("cls")
        match self.choice_after_cipher_text():
            case 1:
                self.show_both_versions()
            case 2:
                self.save_noncipher()
            case 3:
                self.save_cipher()
            case 4:
                self.save_both_sep_loc()
            case 5:
               self.save_both_same_loc()
            case _:
                pass

        print("Operation done successfully... ")
        time.sleep(1.5)
        os.system("cls")


    @staticmethod
    def choice_after_cipher_text() -> int:

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

    def save_noncipher(self):
        # create non cipher text object and save into new location
        filepath = input("Provide file path for non cipher version : ")
        filepath = self.check_filepath(filepath)
        self.file_handler.update_non_cipher_objs(filepath = filepath, content = self.content)
        self.file_handler.write(filepath = filepath, content = self.content)

    def save_cipher(self):
        # create cipher text object and save into new location
        filepath = input("Provide file path for cipher version : ")
        filepath = self.check_filepath(filepath)
        self.file_handler.update_cipher_objs(filepath = filepath, content = self.content)
        self.file_handler.write(filepath = filepath, content = self.cipher_content)

    def save_both_sep_loc(self):
        # create text objs and save into separate new locations
        # create non cipher text object and save into new location
        filepath = input("Provide file path for non cipher version : ")
        filepath = self.check_filepath(filepath)
        self.file_handler.update_non_cipher_objs(filepath = filepath, content = self.content)
        self.file_handler.write(filepath = filepath, content = self.content)
            # saving cipher into new location
        filepath = input("Provide file path for cipher version : ")
        filepath = self.check_filepath(filepath)
        self.file_handler.update_cipher_objs(filepath = filepath, content = self.cipher_content)
        self.file_handler.write(filepath = filepath, content = self.cipher_content)


    def save_both_same_loc(self):
        # create text objs and save into one new locations
        input("ccaca")
        filepath = input("Provide file path for both versions : ")
        filepath = self.check_filepath(filepath)
        content_con = self.content+self.cipher_content
        self.file_handler.update_both_ver_objs(filepath = filepath, content = content_con)
        self.file_handler.write(filepath=filepath, content = content_con)



    def cipher_from_filesystem(self):
        filepath = self.file_choice()
        self.read_file(filepath)
        cipher_content = CipherManager.encrypt_from_filesystem(self.content)
        choice = Menu.choices_after_cipher_file()
        self.after_cipher_file(choice, filepath)


    def file_choice(self):
        os.system("cls")
        print("Avaliable files in directory : \n")
        avaliable_filepaths = self.file_handler.non_cipher_filepaths + self.file_handler.untracked_filepaths
        for filepath in avaliable_filepaths:
            print(f"* {filepath}")
        filepath = input("\nProvide filepath to cipher : ")
        while filepath not in avaliable_filepaths:
            filepath = input("Provide proper filepath to cipher : ")
        return filepath

    def read_file(self, filepath : str):
        content = self.file_handler.read_file(filepath)
        self.file_handler.update_non_cipher_objs(filepath = filepath, content = content)
        time.sleep(1)
        os.system("cls")


    @staticmethod
    def choices_after_cipher_file() -> int:
        os.system("cls")
        print("\nYour options for further content processing :\n")
        print("1. Simply show cipher version")
        print("2. Save to same location")
        print("3. Save to new location\n")

        choice = input("Your choice : ")
        while choice not in ["1", "2", "3"]:
            choice = input("Your choice : ")
        return int(choice)


    def after_cipher_file(self, choice : int, filepath : str):
        match choice:
            case 1:
                self.show_both_versions()
            case 2:
                self.file_handler.update_cipher_objs(filepath = filepath, content = self.cipher_content)
                self.file_handler.append(filepath, self.cipher_content)
            case 3:
                filepath = input("Provide file path : ")
                filepath = self.check_filepath(filepath)
                self.file_handler.update_cipher_objs(filepath = filepath, content = self.cipher_content)
                self.file_handler.write(filepath = filepath, content = self.cipher_content)


    # ---------------------------------------- DECIPHER METHODS ----------------------------------------


    def decipher(self):
        """
        decide how user will provide content
        args : None
        return : None
        """
        match Menu.show_cipher_options():
            case 1:
                self.decipher_from_provided_text()
            case 2:
                self.decipher_from_filesystem()


    def decipher_from_provided_text(self):
        self.content, self.cipher_content = CipherManager.dencrypt_from_given_content()
        os.system("cls")
        match self.choice_after_cipher_text():
            case 1:
                self.show_both_versions()
            case 2:
                self.save_noncipher()
            case 3:
                self.save_cipher()
            case 4:
                self.save_both_sep_loc()
            case 5:
               self.save_both_same_loc()
            case _:
                pass

        print("Operation done successfully... ")
        time.sleep(1.5)
        os.system("cls")

    def decipher_from_filesystem(self):
        pass

    def encode():
        self._shift()

    def decode():
        self._shift()

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
        if self.file_handler.cipher_filepaths:
            for filepath in self.file_handler.cipher_filepaths:
                print(f" * file  {filepath}" )
        else:
            print(f" * no cipher files in this system session")
        print("\n")

    def show_non_cipher_files(self) -> None:
        print("------  NON CIPHER  -------")
        print("\n")
        if self.file_handler.non_cipher_filepaths:
            for filepath in self.file_handler.non_cipher_filepaths:
                print(f" * file  {filepath}" )
        else:
            print(f" * no decipher files in this system session")
        print("\n")

    def show_both_version_files(self) -> None:
        print("------  BOTH VERSIONS  ------")
        print("\n")
        if self.file_handler.both_ver_filepaths:
            for filepath in self.file_handler.both_ver_filepaths:
                print(f" * file  {filepath}" )
        else:
            print(f" * no both versions files in this system session")
        print("\n")

    def show_untracked_files(self) -> None:
        print("------  UNTRACKED FILES  ------")
        print("\n")
        if self.file_handler.untracked_filepaths:
            for filepath in self.file_handler.untracked_filepaths:
                print(f" * file  {filepath}" )
        else:
            print(f" * no unknown status files in this system session")
        print("\n")

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
        if self.file_handler.cipher_filepaths:
            for filepath in self.file_handler.cipher_filepaths:
                print(f" * file  {filepath}" )
        else:
            print(f" * no cipher files in this system session")
        print("\n")

    def show_non_cipher_files(self) -> None:
        print("------  NON CIPHER  -------")
        print("\n")
        if self.file_handler.non_cipher_filepaths:
            for filepath in self.file_handler.non_cipher_filepaths:
                print(f" * file  {filepath}" )
        else:
            print(f" * no decipher files in this system session")
        print("\n")

    def show_both_version_files(self) -> None:
        print("------  BOTH VERSIONS  ------")
        print("\n")
        if self.file_handler.both_ver_filepaths:
            for filepath in self.file_handler.both_ver_filepaths:
                print(f" * file  {filepath}" )
        else:
            print(f" * no both versions files in this system session")
        print("\n")

    def show_untracked_files(self) -> None:
        print("------  UNTRACKED FILES  ------")
        print("\n")
        if self.file_handler.untracked_filepaths:
            for filepath in self.file_handler.untracked_filepaths:
                print(f" * file  {filepath}" )
        else:
            print(f" * no unknown status files in this system session")
        print("\n")



    # ---------------------------------------- OTHER MENU METHODS ----------------------------------------

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



















    def check_filepath(self, filepath : str) -> str:

        pattern = r"(\w{1,})(\.)(txt|json)"
        all_filepaths = self.file_handler.collect_all_filepaths()

        while filepath in all_filepaths:
            print(f"File path {filepath} not allowed because it already exists")
            filepath = input("Provide file path : ")

        while not re.match(string = filepath, pattern = pattern):
            print("wrong filepath name")
            filepath = input("Provide file path : ")

        return filepath








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


