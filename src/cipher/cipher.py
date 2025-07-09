import string
from abc import ABC, abstractmethod
import os
from src.cipher.user_interface import UserInterface


class CipherStrategy(ABC):

    @abstractmethod
    def encrypt(self, content : str) -> str:
        pass

    @abstractmethod
    def decrypt(self, content : str) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def validate_content()
        pass


class ROT13Strategy(CipherStrategy):

    def __init__(self):
        self.offset = 13
        self.name = "rot13"
        self.non_latin_chars, self.non_latin_index = [], []
        self.content = None
        self.cipher_content = None
        self.non_latin_chars = []
        non_latin_chars, non_latin_index = [], []

    def decrypt(self, content : str) -> str:
        pass

    def get_name(self) -> str:
        return self.name

    def execute(self, content) -> str:
        self.content = content
        self.validate_content()
        self.cipher()
        return self.cipher_content

    def cipher(self):
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
        for char_ in self.content:
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

    def validate_content(self):
        """
        returns original or adjusted content
        """

        if not self.content:
            raise ValueError("No content to cipher provided")

        self.check_content()

        if not self.non_latin_chars:
            return self.content
        else:
            return self.change_unallowed_characters()

    def check_content(self):
        # checks if content contains any no allowed chars
        for (idx, c) in enumerate(self.content, start=0):
            if c not in string.ascii_lowercase:
                if c == " ":
                    self.non_latin_chars.append("space")
                else:
                    self.non_latin_chars.append(c)
                self.non_latin_index.append(idx)

    def change_unallowed_characters(self):
        # replace not allowed characters with " * "
        if UserInterface.show_replace_option():
            non_cipher_content_replaced = list(self.content)
            for pos_ in self.non_latin_index:
                non_cipher_content_replaced[pos_] = "*"
            non_cipher_content_replaced = "".join(non_cipher_content_replaced)
        else:
            raise ValueError("User abort cipher")
        return non_cipher_content_replaced

class ROT47Strategy(CipherStrategy):
    pass

class CipherFactory:

    @staticmethod
    def get_cipher(method : str) -> CipherStrategy:

        if method == "rot13":
            return ROT13Strategy()
        elif method == "rot47":
            return ROT47Strategy()

        raise ValueError(f"Unknown cipher method: {method}")


class CipherManager:
    rot_methods = ["rot13", "rot47"]

    @staticmethod
    def execute() -> tuple:
        """
        task : shows tutorial, fetch content from user, create and execute right cipher method
        args : None
        return : tuple, cipher and non cipher version of the same provided content
        """
        UserInterface.show_tutorial()
        method = UserInterface.method_choice()
        cipher = CipherFactory.get_cipher(method)
        content = UserInterface.provide_content()
        cipher_content = cipher.encrypt(content)

        return content, cipher_content
