from file_handler import FileHandler
from cipher import CipherAlgorithm
from menu import Menu
from manager import Manager

def main():
    file_handler = FileHandler("../cipher_files")
    cipher = CipherAlgorithm(file_handler=file_handler)
    menu = Menu(file_handler=file_handler, cipher = cipher)
    manager = Manager(menu, file_handler, cipher)
    manager.execute()

if __name__ == "__main__":
    main()
