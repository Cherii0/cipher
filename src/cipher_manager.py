from file_handler import FileHandler
from strategy import CipherFactory
from user_interface import UserInterface
from text_manager import TextManager

class CipherManager:
    method = None
    filepath = None

    @classmethod
    def get_current_method(cls) -> str:
        return cls.method

    @classmethod
    def get_current_filepath(cls) -> str:
        return cls.filepath

    @staticmethod
    def execute(from_file : bool) -> tuple | None:
        """
        shows tut, fetch method from user, create object from factory, cipher and returns content, creates text obj
        args : None
        return : tuple : decipher and cipher content
        """
        CipherManager.method = UserInterface.method_choice()
        cipher = CipherFactory.get_cipher(CipherManager.method)

        if from_file:
            CipherManager.filepath = UserInterface.choice_filepath()
            if not CipherManager.filepath:
                input("Press any key to comeback to menu...")
                return None, None
            content = FileHandler.read(CipherManager.filepath)
            TextManager.set_params(filepath=CipherManager.filepath)
        else:
            UserInterface.show_tutorial(CipherManager.method)
            content = UserInterface.provide_content()

        cipher_content = cipher.execute(content)
        return content, cipher_content
