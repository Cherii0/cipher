import pytest
import sys

sys.path.append("../src")
from src.cipher_manager import CipherManager
from src.strategy import ROT13Strategy
import builtins


@pytest.fixture
def init_cipher_obj(mocker):
    mocker.patch(
        target="user_interface.UserInterface.show_method_choice",
        return_value=["rot13", "rot47"],
    )
    mocker.patch(
        target="user_interface.UserInterface.method_choice", return_value="rot13"
    )
    mocker.patch(
        target="strategy.CipherFactory.get_cipher", return_value=ROT13Strategy()
    )


@pytest.fixture
def mocker_filepath(mocker):
    mocker.patch(
        target="user_interface.UserInterface.choice_filepath", return_value="cipher.txt"
    )
    mocker.patch(target="file_handler.FileHandler.read", return_value="python")


@pytest.mark.execute
def test_if_execute_from_file_return_expected_values_then_pass(
    init_cipher_obj, mocker_filepath
):
    assert CipherManager.execute(from_file=True) == ("python", "clguba")


@pytest.mark.execute
def test_if_execute_from_user_input_return_expected_values_then_pass(
    init_cipher_obj, monkeypatch, mocker
):
    mocker.patch(target="strategy.ROT13Strategy.execute", return_value="clguba")
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: "python")
    assert CipherManager.execute(from_file=False) == ("python", "clguba")
