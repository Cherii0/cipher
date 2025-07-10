from file_handler import FileHandler
from menu import Menu
from src.cipher.strategy import

def main():

    file_handler = FileHandler("../cipher_files")
    cipher = Cip
    menu = Menu(file_handler=file_handler, cipher = cipher)
    menu.execute()

if __name__ == "__main__":
    main()
