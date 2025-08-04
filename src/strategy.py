from abc import ABC, abstractmethod
import string
from src.user_interface import UserInterface


class UserCancelReplace(Exception):
    pass


class CipherStrategy(ABC):

    @staticmethod
    @abstractmethod
    def execute(content: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def validate_content(content: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def cipher(content: str) -> str:
        pass


class ROT47Strategy(CipherStrategy):
    offset = 47
    name = "rot47"

    @staticmethod
    def execute(content: str) -> str:
        content = ROT47Strategy.validate_content(content)
        cipher_content = ROT47Strategy.cipher(content)
        return cipher_content

    @staticmethod
    def cipher(content) -> str:
        """
        the actual cipher algorithm remains original content and produce cipher content
        args : None
        return : None
        """

        ascii_bgn, ascii_end = 33, 127
        ascii_codes = [c for c in range(ascii_bgn, ascii_end)]
        # [33 ... 126]
        ascii_chars_dict = {
            char_: code_
            for (char_, code_) in zip([chr(c) for c in ascii_codes], ascii_codes)
        }
        # {character : code}
        ascii_codes_dict = {code_: char_ for (char_, code_) in ascii_chars_dict.items()}
        # {code : character}

        non_cipher_content_codes = []
        for char_ in content:
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

        cipher_content = "".join(cipher_content)
        return cipher_content

    @staticmethod
    def get_name() -> str:
        return ROT47Strategy.name

    @staticmethod
    def validate_content(content: str) -> str:
        """
        remains original content or replace unallowed characters with " * " depends on user choice
        args : None
        return : None
        """
        if not content:
            raise ValueError("No content to cipher provided")

        non_allowed_chars, non_allowed_index = [], []
        # checks if content contains any no allowed chars
        for idx, c in enumerate(content, start=0):
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
                non_cipher_content_replaced = list(content)
                for pos_ in non_allowed_index:
                    non_cipher_content_replaced[pos_] = "*"
                non_cipher_content_replaced = "".join(non_cipher_content_replaced)
                return non_cipher_content_replaced
            else:
                raise UserCancelReplace
        else:
            return content


class ROT13Strategy(CipherStrategy):
    offset = 13
    name = "rot13"

    @staticmethod
    def get_name() -> str:
        return ROT13Strategy.name

    @staticmethod
    def execute(content) -> str:
        content = ROT13Strategy.validate_content(content)
        cipher_content = ROT13Strategy.cipher(content)
        return cipher_content

    @staticmethod
    def cipher(content) -> str:
        """
        the actual cipher algorithm remains original content and produce cipher content
        args : None
        return : None
        """

        latin_bgn, latin_end = 0, 26

        latin_codes = [c for c in range(latin_bgn, latin_end)]
        # [0, 1, 2 ... 25] # 26 total = 26 latin letters

        latin_letters_dict = {
            char_: code_ for (char_, code_) in zip(string.ascii_lowercase, latin_codes)
        }
        # {'a': 0, 'b': 1, ... 'z': 25}

        latin_codes_dict = {
            code_: char_ for (char_, code_) in latin_letters_dict.items()
        }
        # {0: 'a', 1: 'b' ... 25: 'z'}

        non_cipher_content_codes = []  # 0, 24, 21, 11 etc
        for char_ in content:
            non_cipher_content_codes.append(latin_letters_dict.get(char_))

        cipher_content_codes = []  # 0, 12, None, 13, 21 etc

        for code_ in non_cipher_content_codes:
            if code_ is None:
                continue
            elif code_ < ROT13Strategy.offset:
                cipher_content_codes.append(code_ + ROT13Strategy.offset)
            else:
                cipher_content_codes.append(code_ - ROT13Strategy.offset)

        cipher_content = []
        for code_ in cipher_content_codes:
            if code_ is None:
                cipher_content.append("*")
            else:
                cipher_content.append(latin_codes_dict[code_])

        cipher_content = "".join(cipher_content)
        return cipher_content

    @staticmethod
    def validate_content(content: str) -> str:
        """
        remains original content or replace unallowed characters with " * " depends on user choice
        args : None
        return : None
        """
        if not content:
            raise ValueError("No content to cipher provided")

        non_latin_chars, non_latin_index = [], []
        # checks if content contains any no allowed chars
        for idx, c in enumerate(content, start=0):
            if c not in string.ascii_lowercase:
                if c == " ":
                    non_latin_chars.append("space")
                else:
                    non_latin_chars.append(c)
                non_latin_index.append(idx)

        if non_latin_chars:
            if UserInterface.show_replace_option(non_latin_chars, non_latin_index):
                # replace not allowed characters with " * "
                non_cipher_content_replaced = list(content)
                for pos_ in non_latin_index:
                    non_cipher_content_replaced[pos_] = "*"
                non_cipher_content_replaced = "".join(non_cipher_content_replaced)
                return non_cipher_content_replaced
            else:
                raise UserCancelReplace
        else:
            return content


class EmptyRotMethods(Exception):
    pass


class CipherFactory:
    _rot_methods = ["rot13", "rot47"]

    @staticmethod
    def update_rot_methods(rot_methods: list[str]) -> None:
        for rm in rot_methods:
            if rm in CipherFactory._rot_methods:
                pass
            else:
                CipherFactory._rot_methods.append(rm)

    @staticmethod
    def clear_rot_methods():
        CipherFactory._rot_methods.clear()

    @staticmethod
    def get_rot_methods() -> list:
        if not CipherFactory._rot_methods:
            raise EmptyRotMethods
        return CipherFactory._rot_methods

    @staticmethod
    def get_cipher(method: str) -> CipherStrategy:
        if method == "rot13":
            return ROT13Strategy()
        elif method == "rot47":
            return ROT47Strategy()
        raise ValueError(f"Unknown cipher method: {method}")
