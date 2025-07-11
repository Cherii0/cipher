from abc import ABC, abstractmethod
import string
from user_interface import UserInterface


class CipherStrategy(ABC):
    @abstractmethod
    def execute(self, content : str) -> str:
        pass
    @abstractmethod
    def get_name(self) -> str:
        pass
    @abstractmethod
    def validate_content(self) -> None:
        pass
    @abstractmethod
    def cipher(self) -> None:
        pass

class ROT47Strategy(CipherStrategy):
    def __init__(self):
        self.offset = 47
        self.name = "rot47"
        self.content = None
        self.cipher_content = None

    def execute(self, content : str) -> str:
        self.content = content
        self.validate_content()
        self.cipher()
        return self.cipher_content

    def cipher(self):
        """
        the actual cipher algorithm remains original content and produce cipher content
        args : None
        return : None
        """

        ascii_bgn, ascii_end = 33, 127
        ascii_codes = [c for c in range(ascii_bgn, ascii_end)]
        # [33 ... 126]
        ascii_chars_dict = {char_: code_ for (char_, code_) in zip([chr(c) for c in ascii_codes], ascii_codes)}
        # {character : code}
        ascii_codes_dict = {code_: char_ for (char_, code_) in ascii_chars_dict.items()}
        # {code : character}

        non_cipher_content_codes = []
        for char_ in self.content:
            non_cipher_content_codes.append(ascii_chars_dict.get(char_))

        cipher_content_codes = []

        for code_ in non_cipher_content_codes:
            if code_ is None:
                cipher_content_codes.append(None)
            else:
                shifted = 33 + ((code_ - 33 + 47) % 94)
                cipher_content_codes.append(shifted)

        cipher_content = []
        for code_ in cipher_content_codes:
            if code_ is None:
                cipher_content.append("*")
            else:
                cipher_content.append(ascii_codes_dict[code_])

        self.cipher_content = "".join(cipher_content)

    def get_name(self) -> str:
        return self.name

    def validate_content(self) -> None:
        """
        remains original content or replace unallowed characters with " * " depends on user choice
        args : None
        return : None
        """
        if not self.content:
            raise ValueError("No content to cipher provided")

        non_allowed_chars, non_allowed_index = [], []
        # checks if content contains any no allowed chars
        for (idx, c) in enumerate(self.content, start=0):
            ascii_code = ord(c)
            if ascii_code < 33 or ascii_code > 126:
                if c == " ":
                    non_allowed_chars.append("space")
                else:
                    non_allowed_chars.append(c)
                non_allowed_index.append(idx)

        if non_allowed_chars:
            if UserInterface.show_replace_option(non_allowed_chars, non_allowed_index):
                # replace not allowed characters with " * "
                non_cipher_content_replaced = list(self.content)
                for pos_ in non_allowed_index:
                    non_cipher_content_replaced[pos_] = "*"
                non_cipher_content_replaced = "".join(non_cipher_content_replaced)
                self.content = non_cipher_content_replaced
            else:
                raise ValueError("User abort cipher")
        else:
            return

class ROT13Strategy(CipherStrategy):
    def __init__(self):
        self.offset = 13
        self.name = "rot13"
        self.content = None
        self.cipher_content = None

    def get_name(self) -> str:
        return self.name

    def execute(self, content) -> str:
        self.content = content
        self.validate_content()
        self.cipher()
        return self.cipher_content

    def cipher(self) -> None:
        """
        the actual cipher algorithm remains original content and produce cipher content
        args : None
        return : None
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
                cipher_content_codes.append(None)
            else:
                relative_code = code_ - 33
                if relative_code < self.offset:
                    shifted_relative = relative_code + self.offset
                else:
                    shifted_relative = relative_code - self.offset

                shifted_relative_wrapped = shifted_relative % 94
                shifted_code = shifted_relative_wrapped + 33
                cipher_content_codes.append(shifted_code)

        cipher_content = []
        for code_ in cipher_content_codes:
            if code_ is None:
                cipher_content.append("*")
            else:
                cipher_content.append(latin_codes_dict[code_])

        self.cipher_content = "".join(cipher_content)

    def validate_content(self):
        """
        remains original content or replace unallowed characters with " * " depends on user choice
        args : None
        return : None
        """
        if not self.content:
            raise ValueError("No content to cipher provided")

        non_latin_chars, non_latin_index = [], []
        # checks if content contains any no allowed chars
        for (idx, c) in enumerate(self.content, start=0):
            if c not in string.ascii_lowercase:
                if c == " ":
                    non_latin_chars.append("space")
                else:
                    non_latin_chars.append(c)
                non_latin_index.append(idx)

        if non_latin_chars:
            if UserInterface.show_replace_option(non_latin_chars, non_latin_index):
                # replace not allowed characters with " * "
                non_cipher_content_replaced = list(self.content)
                for pos_ in non_latin_index:
                    non_cipher_content_replaced[pos_] = "*"
                non_cipher_content_replaced = "".join(non_cipher_content_replaced)
                self.content = non_cipher_content_replaced
            else:
                raise ValueError("User abort cipher")
        else:
            return


class CipherFactory:
    _rot_methods = ["rot13", "rot47"]

    @staticmethod
    def get_rot_methods():
        return CipherFactory._rot_methods

    @staticmethod
    def get_cipher(method : str) -> CipherStrategy:

        if method == "rot13":
            return ROT13Strategy()
        elif method == "rot47":
            return ROT47Strategy()

        raise ValueError(f"Unknown cipher method: {method}")
