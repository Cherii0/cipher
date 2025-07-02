import string
import time

from file_handler import FileHandler
from text import Text
from abc import ABC, abstractmethod
import os

"""

CipherFactory
"""

class UserInterface:

    @staticmethod
    def show_tutorial():
        os.system("cls")
        print("\n")
        print(" * for method rot13 provide  content that contains only letters A-Z not even space allowed\n")
        print(" * for method rot47 provide only content that contains ASCII characters\n\n")

    @staticmethod
    def method_choice() -> int:

        methods = [method.name for method in CipherManager.cipher_methods.values()]
        # [ rot13, rot47 ... ]

        print(" -  METHODS AVALIABLE  - \n\n")
        for idx, method in enumerate(methods, start = 1):
            print(f"{idx}. {method}\n")

        method_choice = input("Your method declaration : ")

        while int(method_choice) not in range(1, len(methods)+1):
            method_choice = input("Your method declaration : ")

        return int(method_choice)

    @staticmethod
    def provide_content():
        content = input("Provide text to cipher : ")
        return content




class CipherStrategy(ABC):

    @abstractmethod
    def encrypt(self, content : str) -> str:
        pass

    @abstractmethod
    def decrypt(self):
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def validate_content(self, content : str) -> str:
        pass




class ROT13Strategy(CipherStrategy):

    def __init__(self):
        self.offset = 13
        self.name = "rot13"

    def decrypt(self):
        pass

    def get_name(self) -> str:
        return self.name

    def encrypt(self, content : str) -> str:
        """
        the actual cipher algorithm, takes decipher content and returns cipher version
        Input : string with only ascii letters and " * "
        """

        latin_bgn, latin_end = 0, 26

        latin_codes = [c for c in range(latin_bgn, latin_end)]
        # [0, 1, 2 ... 25] # 26 total = 26 latin letters

        latin_letters_dict = {char_: code_ for (char_, code_) in zip(string.ascii_lowercase, latin_codes)}
        # {'a': 0, 'b': 1, ... 'z': 25}

        latin_codes_dict = {code_ : char_ for (char_, code_) in latin_letters_dict.items()}
        # {0: 'a', 1: 'b' ... 25: 'z'}

        non_cipher_content_codes = [] # 0, 24, 21, 11 etc
        for char_ in content:
            non_cipher_content_codes.append(latin_letters_dict.get(char_))

        cipher_content_codes = [] # 0, 12, None, 13, 21 etc

        for code_ in non_cipher_content_codes:
            if code_ is None:
                continue
            elif code_ < self.offset:
                cipher_content_codes.append(code_ + self.offset)
            else:
                cipher_content_codes.append(code_ - self.offset)

        cipher_content = []
        for code_ in cipher_content_codes:
            if code_ is None:
                cipher_content.append("*")
            else:
                cipher_content.append(latin_codes_dict[code_])

        return "".join(cipher_content)

    def validate_content(self, content : str) -> str:
        """
        returns original or adjusted content
        """
        if not content:
            raise ValueError("No content to cipher provided")

        non_latin_chars, non_latin_index = [], []

        # checks if content contains any no allowed chars
        for (idx, c) in enumerate(content, start=0):
            if c not in string.ascii_lowercase:
                if c == " ":
                    non_latin_chars.append("space")
                else:
                    non_latin_chars.append(c)
                non_latin_index.append(idx)

        if not non_latin_chars:
            return content

        print("\n")
        print("Found non allowed characters at given positions : \n")
        for (char_, pos_) in zip(non_latin_chars, non_latin_index):
            print(f"{char_} : {pos_}")
        print("\n")
        replace = input("Change above occurrences with '*' ?  YES \\ NO  : ")
        print("\n")

        if replace:
            non_cipher_content_replaced = list(content)
            for pos_ in non_latin_index:
                non_cipher_content_replaced[pos_] = "*"
            non_cipher_content_replaced = "".join(non_cipher_content_replaced)
        else:
            raise ValueError("User abort cipher")

        return non_cipher_content_replaced


class CipherManager:
    cipher_methods = {1: ROT13Strategy()}

    @staticmethod
    def encrypt_from_given_content() -> tuple:
        UserInterface.show_tutorial()
        method_choice = UserInterface.method_choice()

        match method_choice:
            case 1:
                method = CipherManager.cipher_methods.get(1)
            case _:
                pass

        content = UserInterface.provide_content()
        content = method.validate_content(content)
        cipher_content = method.encrypt(content)

        return content, cipher_content


    @staticmethod
    def encrypt_from_filesystem(content_ : str) -> str:
        UserInterface.show_tutorial()
        method_choice = UserInterface.method_choice()

        match method_choice:
            case 1:
                method = CipherManager.cipher_methods.get(1)
            case _:
                pass

        content = method.validate_content(content_)
        cipher_content = method.encrypt(content)
        return cipher_content

