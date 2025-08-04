import sys
sys.path.append("../")
from src.manager import Manager
from src.menu import Menu
from src.cipher_manager import CipherManager


def main():

    menu = Menu()
    cipher_manager = CipherManager()
    manager = Manager(menu=menu, cipher_manager=cipher_manager)
    manager.execute()


if __name__ == "__main__":
    main()
