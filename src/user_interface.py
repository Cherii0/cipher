import os
import re

class UserInterface:
    cipher_filepath = "../cipher_files"

    @staticmethod
    def show_tutorial(method : str):
        os.system("cls")
        print("\n")
        match method:
            case "rot13":
                print(" * For method rot13 provide  content that contains only letters A-Z not even space allowed\n")
            case "rot47":
                print(" * For method rot47 provide ASCII characters within the range of 33 to 126, which excludes spaces, newlines\n\n")

    @staticmethod
    def method_choice() -> str:
        os.system("cls")
        from strategy import CipherFactory
        methods = CipherFactory.get_rot_methods()
        print("\n -  METHODS AVALIABLE  - \n\n")
        for idx, method in enumerate(methods, start = 1):
            print(f"{idx}. {method}\n")

        method_choice = input("Your method declaration : ")

        while True:
            if method_choice not in methods:
                try:
                    example_method = methods[0]
                except IndexError:
                    raise "No rot methods found"
                method_choice = input(f"Provide correct method for example {example_method} : ")
            else:
                break

        return method_choice

    @staticmethod
    def provide_content():
        content = input("Provide text to cipher : ")
        return content


    @staticmethod
    def choice_filepath() -> str:
        os.system("cls")
        print("\nAVALIABLE FILES : \n")
        os.chdir(UserInterface.cipher_filepath)
        files =  os.listdir()
        p = r"(?P<file_path>\w{1,})(\.)(?P<extension>txt|json)"
        files_filtered = []
        for file in files:
            match = re.match(pattern = p, string = file)
            if match:
                files_filtered.append(match.string)

        for idx, file in enumerate(files_filtered, start=1):
            print(f"{idx}. {file}")

        filepath = input("\nProvide filepath : ")
        while True:
            if filepath in files_filtered:
                break
            else:
                filepath = input("Provide correct filepath : ")

        return filepath


    @staticmethod
    def show_replace_option(non_latin_chars : list, non_latin_index : list) -> bool:
        print("\n")
        print("Found non allowed characters at given positions : \n")
        for (char_, pos_) in zip(non_latin_chars, non_latin_index):
            print(f"{char_} : {pos_}")
        print("\n")
        replace = input("Change above occurrences with '*' ?  YES \\ NO  : ")
        print("\n")
        return True if replace=="YES" else False
