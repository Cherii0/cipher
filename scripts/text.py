from dataclasses import dataclass, field


@dataclass
class Text:
    _content : str = None
    _rot_type : str =  None
    _encrypted : bool = None

    @property
    def content(self):
        return self._content

    @property
    def file_path(self):
        return self._file_path

    @property
    def encrypted(self):
        return self._encrypted

    @encrypted.setter
    def encrypted(self, value : bool):
        self._encrypted = value

    @property
    def rot_type(self):
        return self._rot_type

    @rot_type.setter
    def rot_type(self, value : str):
        self._rot_type = value
