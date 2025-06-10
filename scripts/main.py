from classes import Manager, FileHandler, Menu, CipherAlgorithm

def main():
    file_handler = FileHandler()
    cipher = CipherAlgorithm(file_handler)
    menu = Menu(cipher, file_handler)
    manager = Manager(menu, file_handler, cipher)
    manager.execute()



if __name__ == "__main__":
    main()
