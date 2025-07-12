from dataclasses import dataclass

@dataclass
class Text:
    _content : str = None
    _rot_type : str =  None
    _encrypted : bool = None


class TextManager:
    __texts = {}

    __filepath = None
    __content = None
    __encrypted = None
    __rot_type = None

    @classmethod
    def get_texts(cls) -> dict:
        return cls.__texts

    @classmethod
    def set_params(cls, **kwargs):
        if "filepath" in kwargs and kwargs["filepath"] is not None:
            cls.__filepath = kwargs["filepath"]
        if "content" in kwargs and kwargs["content"] is not None:
            cls.__content = kwargs["content"]
        if "rot_type" in kwargs and kwargs["rot_type"] is not None:
            cls.__rot_type = kwargs["rot_type"]
        if "encrypted" in kwargs and kwargs["encrypted"] is not None:
            cls.__encrypted = kwargs["encrypted"]

    @classmethod
    def create_obj(cls):
        obj = Text(cls.__content, cls.__rot_type, cls.__encrypted)
        if cls.__filepath:
            cls.__texts.update({cls.__filepath : obj})
            cls.restore_obj_params()

    @classmethod
    def restore_obj_params(cls):
        __filepath = None
        __content = None
        __encrypted = None
        __rot_type = None
