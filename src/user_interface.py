import os
import re


class UserInterface:
    cipher_filepath = "../cipher_files"

    @staticmethod
    def show_tutorial(method: str):
        print("\n" * 100)
        print("\n")
        match method:
            case "rot13":
                print(
                    " * For method rot13 provide  content that contains only letters A-Z not even space allowed\n"
                )
            case "rot47":
                print(
                    " * For method rot47 provide ASCII characters within the range of 33 to 126, which excludes spaces, newlines\n\n"
                )
            case _:
                raise ValueError(f"There is no such method as {method}")

    @staticmethod
    def show_method_choice() -> list:
        print("\n" * 100)
        from strategy import CipherFactory

        methods = CipherFactory.get_rot_methods()
        print("\n -  METHODS AVALIABLE  - \n\n")
        for idx, method in enumerate(methods, start=1):
            print(f"{idx}. {method}\n")
        return methods

    @staticmethod
    def method_choice(methods: list) -> str:
        try:
            example_method = methods[0]
        except IndexError:
            raise IndexError("No rot methods found")

        method_choice = input("Your method declaration : ")

        while True:
            if method_choice not in methods:
                method_choice = input(
                    f"Provide correct method for example {example_method} : "
                )
            else:
                break
        return method_choice

    @staticmethod
    def provide_content() -> str:
        return input("Provide content to cipher : ")

    @staticmethod
    def choice_filepath() -> str:
        print("\n" * 100)
        try:
            os.chdir(UserInterface.cipher_filepath)
        except FileNotFoundError:
            os.mkdir("../cipher_files")
        files = os.listdir()
        p = r"(?P<file_path>\w{1,})(\.)(?P<extension>txt|json)"
        files_filtered = UserInterface._filter_files(files, p)
        UserInterface._show_avaliable_files(files_filtered)
        return UserInterface._type_filepath(files_filtered)

    @staticmethod
    def _type_filepath(files_filtered: list) -> str:
        filepath = input("\nProvide filepath : ")
        while True:
            if filepath in files_filtered:
                break
            else:
                filepath = input("Provide correct filepath : ")
        return filepath

    @staticmethod
    def _show_avaliable_files(files_filtered: list) -> None:
        if not files_filtered:
            print(
                f"There is no match files in current directory {UserInterface.cipher_filepath[3:]}"
            )
            return
        print("\nAVALIABLE FILES : \n")
        for idx, file in enumerate(files_filtered, start=1):
            print(f"{idx}. {file}")

    @staticmethod
    def _filter_files(files: list, p: str) -> list:
        if not files:
            return []
        if not p or not isinstance(p, str):
            raise ValueError("Incorrect pattern value")
        files_filtered = []
        for file in files:
            match = re.match(pattern=p, string=file)
            if match:
                files_filtered.append(match.string)
        return files_filtered

    @staticmethod
    def show_replace_option(non_latin_chars: list, non_latin_index: list) -> None:
        if not non_latin_chars or not non_latin_index:
            return
        print("\n Found non allowed characters at given positions : \n")
        for char_, pos_ in zip(non_latin_chars, non_latin_index):
            print(f"{char_} : {pos_}")

    @staticmethod
    def replace_option() -> bool:
        replace = input("\nChange above occurrences with '*' ?  YES \\ NO  : \n")
        return True if replace == "YES" else False
