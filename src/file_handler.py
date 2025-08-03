import re
import time

SLEEP_TIME = 1.5

class FileHandler:
    @staticmethod
    def read_about(filepath : str) -> list:
        with open(file=filepath, mode="r", encoding="UTF-8") as file:
            return file.readlines()

    @staticmethod
    def read(filepath : str) -> str:
        content = ""
        char = True
        with open(file=filepath, mode="r", encoding="UTF-8") as file:
            while char:
                char = file.read(1)
                if not char.isascii():
                    char = "*"
                elif re.match(pattern = r"[\n]", string = char):
                    char = " "
                content += char
        print(f"\nfile {filepath} loaded\n")
        time.sleep(SLEEP_TIME)
        return content

    @staticmethod
    def append(filepath : str, content : str):
        with open(file = filepath, mode = "a", encoding="UTF-8") as file:
            file.write("\n")
            file.write(content)

    @staticmethod
    def write(filepath : str, content : str) -> None:
        if not isinstance(filepath, str):
            raise ValueError
        if not re.match(string=filepath, pattern=r"(?P<file_path>\w{1,})(\.)(?P<extension>txt|json)"):
            print("given filepath has no extension txt or json")
        with open(file=filepath, mode="w", encoding="UTF-8") as file:
            file.write(content)
