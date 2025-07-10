from src.cipher.user_interface import UserInterface
from src.cipher.strategy import CipherFactory

class CipherManager:

    @staticmethod
    def execute() -> tuple:
        """
        task : shows tut, fetch method from user, create object from factory, cipher and returns content
        args : None
        return : tuple : decipher and cipher content
        """
        UserInterface.show_tutorial()
        method = UserInterface.method_choice()
        cipher = CipherFactory.get_cipher(method)
        content = UserInterface.provide_content()
        cipher_content = cipher.execute(content)

        return content, cipher_content
