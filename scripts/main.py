from classes import Manager, FileHandler, Menu, CipherAlgorithm

def main():
    menu = Menu()
    file_handler = FileHandler()
    cipher = CipherAlgorithm()
    manager = Manager(menu, file_handler, cipher)
    manager.execute()



if __name__ == "__main__":
    main()
