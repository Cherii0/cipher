import os, re
from file_handler import FileHandler


class Menu:
    @staticmethod
    def show_front_menu() -> int:
        os.system("cls")
        print("---------------------")
        print("|        MENU       |")
        print("---------------------")
        print("1. managed files")
        print("2. cipher")
        print("3. decipher")
        print("4. about program")
        print("5. exit")
        print("---------------------")

        choice = input("Provide choice : ")
        while True:
            try:
                choice = int(choice)
                if 0 < choice < 6:
                    break
                else:
                    choice = input("Provide choice between 1 and 6: ")
            except ValueError:
                choice = input("Provide numerical choice : ")

        return choice


    @staticmethod
    def show_cipher_options(title : str) -> int:
        os.system("cls")
        print("---------------------")
        print(f"|      {title}       |")
        print("---------------------")
        print("1. from provided text")
        print("2. from file system")
        print("---------------------")

        choice = input("Your choice : ")
        while True:
            try:
                choice = int(choice)
                if 0 < choice < 3:
                    break
                else:
                    choice = int(input("Provide choice between 1 and 2"))
            except ValueError:
                choice = input("Type numerical choice: ")

        return int(choice)

    @staticmethod
    def show_saving_choices() -> int:
        os.system("cls")
        print("\nYour options for further content processing :\n")
        print("1. Show both versions")
        print("2. Save only non cipher to new location")
        print("3. Save only cipher to new location")
        print("4. Save to separate cipher and non cipher locations")
        print("5. Save into one file both versions\n")

        choice = input("Your choice : ")
        while True:
            try:
                choice = int(choice)
                if 0 < choice < 6:
                    break
                else:
                    choice = input("Provide choice between 1 and 5")
            except ValueError:
                choice = input("Provide numerical choice : ")

        return choice


    @staticmethod
    def show_both_versions(content : str, cipher_content : str) -> None:
        print(f"\nProvided content : {content}")
        print(f"Cipher  version  : {cipher_content}")
        input("\n\nPress any key to come back to menu... ")
        os.system("cls")

    @staticmethod
    def type_saving_filepath() -> str:
        cipher_filepath = "../cipher_files"
        os.system("cls")
        if os.getcwd() != cipher_filepath:
            os.chdir(cipher_filepath)

        files =  os.listdir()
        p = r"(?P<file_path>\w{1,})(\.)(?P<extension>txt|json)"
        files_filtered = []
        for file in files:
            match = re.match(pattern = p, string = file)
            if match:
                files_filtered.append(match.string)

        filepath = input("Provide filepath : ")
        while filepath in files_filtered:
            print(f"File path {filepath} not allowed because it already exists")
            filepath = input("Provide file path : ")

        pattern = r"(\w{1,})(\.)(txt|json)"
        while not re.match(string = filepath, pattern = pattern):
            print("wrong filepath name")
            filepath = input("Provide file path : ")

        return filepath

    @staticmethod
    def type_saving_filepaths() -> tuple:
        filepath_decipher = Menu.type_saving_filepath()
        filepath_cipher = Menu.type_saving_filepath()
        return filepath_decipher, filepath_cipher


    @staticmethod
    def about(filepath : str) -> None:
        content_about = FileHandler.read_about(filepath)
        os.system("cls")
        print("\n")
        for line in content_about:
            print(line)
        input("\n\nPress any key to comeback to menu...")
