import pytest
import sys
sys.path.append("../src")
from src.user_interface import UserInterface
import builtins


@pytest.mark.tutorial
def test_show_tutorial_when_rot13_then_tut_rot13(capsys):
    UserInterface.show_tutorial("rot13")
    stdout, stderr, = capsys.readouterr()
    assert stdout == "\n\n * For method rot13 provide  content that contains only letters A-Z not even space allowed\n\n"

@pytest.mark.tutorial
def test_show_tutorial_when_rot47_then_tut_rot47(capsys):
    UserInterface.show_tutorial("rot47")
    stdout, stderr, = capsys.readouterr()
    assert stdout == "\n\n * For method rot47 provide ASCII characters within the range" \
                     " of 33 to 126, which excludes spaces, newlines\n\n\n"

@pytest.mark.tutorial
def test_show_tutorial_when_unknown_method_then_raise():
    with pytest.raises(ValueError):
        UserInterface.show_tutorial("")

@pytest.mark.tutorial
def test_show_tutorial_when_no_str_input_then_raise():
    with pytest.raises(ValueError):
        UserInterface.show_tutorial(21)

@pytest.mark.show_method_choice
def test_2_method_choice_show_correct_methods_based_on_factory(capsys, mocker):
    mocker.patch("strategy.CipherFactory.get_rot_methods", return_value = ["rot13", "rot47"])
    msg = "\n -  METHODS AVALIABLE  - \n\n\n" + "1. rot13\n\n" + "2. rot47\n\n"
    UserInterface.show_method_choice()
    stdout, stderr = capsys.readouterr()
    assert stdout == msg

@pytest.mark.show_method_choice
def test_3_method_choice_show_correct_methods_based_on_factory(capsys, mocker):
    mocker.patch("strategy.CipherFactory.get_rot_methods", return_value=["rot13", "rot47", "rot21"])
    msg = "\n -  METHODS AVALIABLE  - \n\n\n" + "1. rot13\n\n" + "2. rot47\n\n" + "3. rot21\n\n"
    UserInterface.show_method_choice()
    stdout, stderr = capsys.readouterr()
    assert stdout == msg

@pytest.mark.show_method_choice
def test_return_same_printed_methods(mocker):
    methods = ["rot13"]
    mocker.patch("strategy.CipherFactory.get_rot_methods", return_value=methods)
    assert UserInterface.show_method_choice() == methods

@pytest.mark.method_choice
def test_when_correct_value_then_return_str(monkeypatch):
    methods = ["rot13", "rot47"]
    expected_method = "rot13"
    monkeypatch.setattr(target=builtins, name="input",  value=lambda _ : expected_method)
    tested_method = UserInterface.method_choice(methods)
    assert expected_method == tested_method

@pytest.mark.method_choice
def test_when_incorrect_then_correct_method_then_return_str(monkeypatch):
    methods = ["rot13", "rot47"]
    inputs = iter(["rottttt", "rot47"])
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: next(inputs))
    tested_method = UserInterface.method_choice(methods)
    assert tested_method == "rot47"

@pytest.mark.method_choice
def test_when_no_methods_then_raise():
    methods = []
    with pytest.raises(IndexError):
        UserInterface.method_choice(methods)


@pytest.mark.choice_filepath
def test_when_given_filepaths_and_input_correct_then_return_filepath(mocker, monkeypatch):
    expected_filepath = "file1.txt"
    mocker.patch("os.listdir", return_value=["file1.txt", "file2.txt"])
    monkeypatch.setattr(target=builtins, name="input",  value=lambda _ : expected_filepath)
    assert UserInterface.choice_filepath() == expected_filepath


# pytest -m "choice_filepath" .\test_user_interface.py -v --show-capture=no
@pytest.mark.choice_filepath
def test_when_correct_filepath_and_given_incorrect_filepaths_then_correct_then_return_filepath(mocker, monkeypatch):
    inputs = iter(["fileellree", "file1.txt"])
    mocker.patch("os.listdir", return_value=["file1.txt", "file2.txt"])
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: next(inputs))
    assert UserInterface.choice_filepath() == "file1.txt"


@pytest.mark.type_filepath
def test_when_correct_filepath_then_return_filepath(monkeypatch):
    filepaths = ["file1.txt", "file2.txt"]
    filepath = "file1.txt"
    monkeypatch.setattr(target=builtins, name="input", value=lambda _ :filepath)
    assert UserInterface._type_filepath(filepaths) == filepath

@pytest.mark.type_filepath
def test_when_incorrect_filepath_then_correct_then_return_correct_filepath(monkeypatch):
    filepaths = ["file1.txt", "file2.txt"]
    inputs = iter(["aaaa", "bbbb", "file1.txt", "cccc"])
    monkeypatch.setattr(target=builtins, name="input", value=lambda _ : next(inputs))
    assert UserInterface._type_filepath(filepaths) == "file1.txt"


@pytest.mark.type_filepath
def test_when_non_str_filepath_then_str_then_return_str_filepath(monkeypatch):
    filepaths = ["file1.txt", "file2.txt"]
    inputs = iter([(2,3), "file1.txt"])
    monkeypatch.setattr(target=builtins, name="input", value=lambda _ : next(inputs))
    assert UserInterface._type_filepath(filepaths) == "file1.txt"

@pytest.mark.show_avaliable_files
def test_show_avaliable_files_when_correct_filepaths(capsys):
    msg = "\nAVALIABLE FILES : \n\n" + "1. file1.txt\n" + "2. file2.txt\n"
    filepaths = ["file1.txt", "file2.txt"]
    UserInterface._show_avaliable_files(filepaths)
    stdout, stderr = capsys.readouterr()
    assert msg == stdout

@pytest.mark.show_avaliable_files
def test_show_info_no_filepaths_when_empty_filepaths(capsys):
    msg = "There is no match files in current directory cipher_files\n"
    filepaths = []
    UserInterface._show_avaliable_files(filepaths)
    stdout, stderr = capsys.readouterr()
    assert msg == stdout

@pytest.mark.filter_files
def test_if_directory_empty_return_empty_list():
    filepaths = []
    pattern = r"(?P<file_path>\w{1,})(\.)(?P<extension>txt|json)"
    assert UserInterface._filter_files(filepaths, pattern) == []

@pytest.mark.filter_files
def test_if_non_str_pattern_then_raise():
    filepaths = ["file1.txt", "file2.txt"]
    pattern = 21
    with pytest.raises(ValueError):
        UserInterface._filter_files(filepaths, pattern)

@pytest.mark.replace_option
def test_when_replace_list_empty_then_return_none():
    chars = []
    pos = []
    assert UserInterface.show_replace_option(chars, pos) is None

@pytest.mark.replace_option
def test_when_correct_replace_input_then_show_output(capsys):
    chars = ["ź", " ", "_", "ó"]
    pos = [3, 5, 8, 12]
    msg = "\n Found non allowed characters at given positions : \n\n" + "ź : 3\n" + "  : 5\n" + "_ : 8\n"  + "ó : 12\n"
    UserInterface.show_replace_option(chars, pos)
    stdout, stderr = capsys.readouterr()
    assert msg == stdout
