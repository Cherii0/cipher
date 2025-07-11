from file_handler import FileHandler
from strategy import CipherFactory
from user_interface import UserInterface


class CipherManager:

    @staticmethod
    def execute(from_file : bool) -> tuple:
        """
        shows tut, fetch method from user, create object from factory, cipher and returns content
        args : None
        return : tuple : decipher and cipher content
        """
        method = UserInterface.method_choice()
        cipher = CipherFactory.get_cipher(method)

        if from_file:
            filepath = UserInterface.choice_filepath()
            content = FileHandler.read(filepath)
        else:
            UserInterface.show_tutorial(method)
            content = UserInterface.provide_content()

        cipher_content = cipher.execute(content)

        return content, cipher_content
