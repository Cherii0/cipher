from file_handler import FileHandler
from src.cipher.manager import CipherManager
from src.manager.manager import Manager


def main():

    file_handler = FileHandler("../cipher_files")
    cipher_manager = CipherManager()
    manager = Manager(file_handler=file_handler, cipher_manager = cipher_manager)
    manager.execute()

if __name__ == "__main__":
    main()
