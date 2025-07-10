from abc import ABC, abstractmethod
from src.cipher.rot_methods import *


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

class CipherFactory:
    @staticmethod
    def get_cipher(method : str) -> CipherStrategy:

        if method == "rot13":
            return ROT13Strategy()
        elif method == "rot47":
            return ROT47Strategy()

        raise ValueError(f"Unknown cipher method: {method}")
