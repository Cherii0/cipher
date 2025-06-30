import string
import time

from file_handler import FileHandler
from text import Text
from abc import ABC, abstractmethod
import os

"""
ContentValidator
UserInterface
CipherStrategy
ROT17Strategy(CipherStrategy)
CipherFactory
CipherManager -> uruchamia, userInterface w sobie itd. 
"""

class CipherManager:
    pass


class CipherStrategy(ABC):

    @abstractmethod
    def encrypt(self):
        pass

    @abstractmethod
    def decrypt(self):
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def validate_content(self, content: str) -> str:
        pass




class ROT13Strategy(CipherStrategy):

    def encrypt(self):
        pass

    def decrypt(self):
        pass

    def get_name(self) -> str:
        pass

    def validate_content(self, content: str) -> str:
        pass




class CipherAlgorithm:

    def __init__(self, file_handler : FileHandler):
        self.file_handler = file_handler
        self.rot13_offset = 13
        self.rot_methods = ["rot13", "rot17"]

    @staticmethod
    def show_tutorial():
        os.system("cls")
        print("\n")
        print(" * for method rot13 provide  content that contains only letters A-Z not even space allowed\n")
        print(" * for method rot47 provide only content that contains ASCII characters\n\n")

    @staticmethod
    def check_input(content : str) -> str:
        """
        returns original or adjusted content
        """
        if not content:
            raise ValueError("No content to cipher provided")

        non_latin_chars = []
        non_latin_index = []

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


    def perform_rot13(self, content : str) -> str:
        """
        the actual cipher algorithm, takes decipher content and returns cipher version
        """
        latin_bgn = 0
        latin_end = 26

        latin_codes = [c for c in range(latin_bgn, latin_end)]
        # [0, 1, 2 ... 25] # 26 total = 26 latin letters
        latin_letters_dict = {char_: code_ for (char_, code_) in zip(string.ascii_lowercase, latin_codes)}
        # {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11,
        # 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22,
        # 'x': 23, 'y': 24, 'z': 25}
        latin_codes_dict = {code_ : char_ for (char_, code_) in latin_letters_dict.items()}
        # {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l'
        # , 12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w',
        # 23: 'x', 24: 'y', 25: 'z'}



        non_cipher_content_codes = []
        for char_ in content:
            if char_ != "*":
                non_cipher_content_codes.append(latin_letters_dict[char_])
            else:
                non_cipher_content_codes.append(None)

        cipher_content_codes = []
        for code_ in non_cipher_content_codes:
            if code_ < self.rot13_offset:
                cipher_content_codes.append(code_ + self.rot13_offset)
            else:
                cipher_content_codes.append(code_ - self.rot13_offset)

        cipher_content = []
        for code_ in cipher_content_codes:

            if not code_:
                cipher_content.append("*")
            else:
                cipher_content.append(latin_codes_dict[code_])

        input(".")


        return "".join(cipher_content)

    def perform_rot47(self, content : str) -> str:
        pass

    def method_choice(self) -> str:
        method_choice = input("Your method declaration rot13/rot47: ")

        while method_choice not in self.rot_methods:
            method_choice = input("Your method declaration rot13/rot47: ")

        return method_choice

    def cipher_manager(self, * , method : str, content : str) -> str:
        """
        runs chosen rot cipher method
        """

        if method == "rot13":
            cipher_content = self.perform_rot13(content)
        elif method == "rot47":
            cipher_content = self.perform_rot47(content)
        else:
            ...
        text_obj = Text()
        print("file has been cipher...")
        time.sleep(2)
        return cipher_content
