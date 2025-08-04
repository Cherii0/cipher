import pytest
import sys

sys.path.append("../src")
from src.menu import Menu
import builtins


def test_printed_menu_from_show_front_menu(capsys, monkeypatch):
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: 1)
    Menu.show_front_menu()
    msg = (
        "\n" * 101
        + "---------------------\n"
        + "|        MENU       |\n"
        + "---------------------\n"
        + "1. managed files\n"
        + "2. cipher\n"
        + "3. decipher\n"
        + "4. about program\n"
        + "5. exit\n"
        + "---------------------\n"
    )
    stdout, stderr = capsys.readouterr()
    assert stdout == msg


def test_front_menu_choice_when_correct_int_input_pass(monkeypatch):
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: 1)
    assert Menu._provide_choice() == 1


def test_front_menu_choice_when_word_then_correct_int_then_pass(monkeypatch):
    inputs = iter(["abcd", 1])
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: next(inputs))
    assert Menu._provide_choice() == 1


def test_front_menu_choice_when_incorrect_range_then_correct_int_pass(monkeypatch):
    inputs = iter([221, 1])
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: next(inputs))
    assert Menu._provide_choice() == 1


def test_show_cipher_options(capsys, monkeypatch):
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: 1)
    Menu.show_cipher_options("CIPHER")
    msg = (
        "\n" * 101
        + "---------------------\n"
        + "|      CIPHER       |\n"
        + "---------------------\n"
        + "1. from provided text\n"
        + "2. from file system\n"
        + "---------------------\n"
    )
    stdout, stderr = capsys.readouterr()
    assert stdout == msg


def test_cipher_options_correct_int_then_pass(monkeypatch):
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: 1)
    assert Menu._provide_cipher_option_input() == 1


def test_cipher_options_when_word_then_correct_int_then_pass(monkeypatch):
    inputs = iter(["zzz", 1])
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: next(inputs))
    assert Menu._provide_cipher_option_input() == 1


def test_cipher_options_when_incorrect_range_then_correct_int_pass(monkeypatch):
    inputs = iter([5, 1])
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: next(inputs))
    assert Menu._provide_cipher_option_input() == 1


def test_show_saving_choices(capsys, monkeypatch):
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: 1)
    Menu.show_saving_choices()
    msg = (
        "\n" * 101
        + "\nYour options for further content processing :\n\n"
        + "1. Show both versions\n"
        + "2. Save only non cipher to new location\n"
        + "3. Save only cipher to new location\n"
        + "4. Save to separate cipher and non cipher locations\n"
        + "5. Save into one file both versions\n\n"
    )
    stdout, stderr = capsys.readouterr()
    assert stdout == msg


def test_show_saving_choices_correct_int_then_pass(monkeypatch):
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: 1)
    assert Menu._provide_saving_choice() == 1


def test_show_saving_choices_when_word_then_correct_int_then_pass(monkeypatch):
    inputs = iter(["bda", 1])
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: next(inputs))
    assert Menu._provide_saving_choice() == 1


def test_show_saving_choices_when_incorrect_range_then_correct_int_pass(monkeypatch):
    inputs = iter([13, 1])
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: next(inputs))
    assert Menu._provide_saving_choice() == 1


def test_show_both_versions_when_correct_both_vers_then_pass(capsys, monkeypatch):
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: " ")
    msg = "\n" * 101 + "\nProvided content : python\n" + "Cipher  version  : clguba\n"
    Menu.show_both_versions(content="python", cipher_content="clguba")
    stdout, stderr = capsys.readouterr()
    assert stdout == msg


def test_show_both_versions_when_missing_contents_then_adequate_msg(
    capsys, monkeypatch
):
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: " ")
    msg = (
        "\n" * 101
        + "\nProvided content : Content missing\n"
        + "Cipher  version  : Cipher content missing\n"
    )
    Menu.show_both_versions(content="", cipher_content="")
    stdout, stderr = capsys.readouterr()
    assert stdout == msg


def test_show_both_versions_when_int_content_then_raise(monkeypatch):
    monkeypatch.setattr(target=builtins, name="input", value=lambda _: " ")
    with pytest.raises(ValueError):
        Menu.show_both_versions(content=1, cipher_content="")
