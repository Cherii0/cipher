import os

from src.cipher.cipher import CipherManager


class UserInterface:

    @staticmethod
    def show_tutorial():
        os.system("cls")
        print("\n")
        print(" * for method rot13 provide  content that contains only letters A-Z not even space allowed\n")
        print(" * for method rot47 provide only content that contains ASCII characters\n\n")

    @staticmethod
    def method_choice() -> str:

        methods = [method.name for method in CipherManager.rot_methods.values()]

        print(" -  METHODS AVALIABLE  - \n\n")
        for idx, method in enumerate(methods, start = 1):
            print(f"{idx}. {method}\n")

        method_choice = input("Your method declaration : ")

        while int(method_choice) not in range(1, len(methods)+1):
            method_choice = input("Your method declaration : ")

        return method_choice

    @staticmethod
    def provide_content():
        content = input("Provide text to cipher : ")
        return content

    @staticmethod
    def show_replace_option(non_latin_chars : list, non_latin_index : list) -> bool:
        print("\n")
        print("Found non allowed characters at given positions : \n")
        for (char_, pos_) in zip(non_latin_chars, non_latin_index):
            print(f"{char_} : {pos_}")
        print("\n")
        replace = input("Change above occurrences with '*' ?  YES \\ NO  : ")
        print("\n")
        return True if "Yes" else False
