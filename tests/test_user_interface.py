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

next :
    _type_filepath
    _show_avaliable_files
    _filter_files
    show_replace_option