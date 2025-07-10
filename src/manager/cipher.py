from src.manager.manager import Manager



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

