import sys

sys.path.append("../src")
from src.strategy import (
    CipherFactory,
    EmptyRotMethods,
    ROT13Strategy,
    UserCancelReplace,
)
import pytest


@pytest.mark.factory
def test_should_return_type_list():
    assert isinstance(CipherFactory.get_rot_methods(), list)


@pytest.fixture
def clear_rot_methods_list():
    CipherFactory.clear_rot_methods()


@pytest.mark.factory
def test_if_methods_empty_then_raise(clear_rot_methods_list):
    with pytest.raises(EmptyRotMethods):
        CipherFactory.get_rot_methods()


@pytest.fixture
def init_rot_methods():
    rot_methods = ["rot13", "rot47"]
    CipherFactory.update_rot_methods(rot_methods)


@pytest.mark.factory
def test_when_rot_methods_str_type_then_pass(init_rot_methods):
    assert isinstance(CipherFactory.get_rot_methods()[0], str)


@pytest.fixture
def init_rot_methods_with_duplicates():
    rot_methods = ["rot13", "rot47", "rot13"]
    CipherFactory.clear_rot_methods()
    CipherFactory.update_rot_methods(rot_methods)


@pytest.mark.factory
def test_rot_methods_duplicates(init_rot_methods_with_duplicates):
    assert CipherFactory.get_rot_methods()[0] != CipherFactory.get_rot_methods()[-1]


@pytest.mark.factory
def test_when_rot13_request_then_return_rot13_strategy():
    assert isinstance(CipherFactory.get_cipher("rot13"), ROT13Strategy)


@pytest.mark.factory
def test_when_unallowed_method_then_raise():
    with pytest.raises(ValueError):
        CipherFactory.get_cipher("ABCD")


@pytest.fixture
def create_rot13_cipher():
    return CipherFactory.get_cipher("rot13")


@pytest.mark.strategy_rot13
def test_when_get_name_rot13_then_returns_name(create_rot13_cipher):
    assert create_rot13_cipher.get_name() == "rot13"


@pytest.mark.strategy_rot13
def test_validate_content_when_no_content_then_raise(create_rot13_cipher):
    with pytest.raises(ValueError):
        create_rot13_cipher.validate_content("")


@pytest.mark.strategy_rot13
def test_validate_content_when_correct_content_then_pass(create_rot13_cipher):
    content = "abcd"
    assert create_rot13_cipher.validate_content(content) == content


@pytest.fixture
def mock_replace_option_false(mocker):
    mocker.patch(
        "src.user_interface.UserInterface.show_replace_option", return_value=False
    )


@pytest.fixture
def mock_replace_option_true(mocker, create_rot13_cipher):
    mocker.patch(
        "src.user_interface.UserInterface.show_replace_option", return_value=True
    )


@pytest.mark.strategy_rot13
def test_validate_content_when_incorrect_and_replace_then_pass(
    create_rot13_cipher, mock_replace_option_true
):
    content = "ab cźd"
    replaced_content = "ab*c*d"
    assert create_rot13_cipher.validate_content(content) == replaced_content


@pytest.mark.strategy_rot13
def test_cipher_when_abcd_then_nopq(create_rot13_cipher):
    content = "abcd"
    cipher_content = "nopq"
    assert create_rot13_cipher.cipher(content) == cipher_content


@pytest.mark.strategy_rot13
def test_cipher_when_hellopython_then_uryybclguba(create_rot13_cipher):
    content = "hellopython"
    cipher_content = "uryybclguba"
    assert create_rot13_cipher.cipher(content) == cipher_content


@pytest.fixture
def create_rot47_cipher():
    return CipherFactory.get_cipher("rot47")


@pytest.mark.strategy_rot47
def test_when_get_name_then_return_name(create_rot47_cipher):
    rot_method = "rot47"
    assert create_rot47_cipher.get_name() == rot_method


@pytest.mark.strategy_rot47
def test_validate_content_when_correct_then_pass(create_rot47_cipher):
    content = "ABCD"
    assert create_rot47_cipher.validate_content(content) == content


@pytest.mark.strategy_rot47
def test_validate_content_when_incorrect_and_no_replace_then_raise(
    create_rot47_cipher, mock_replace_option_false
):
    content = "ab cd"
    with pytest.raises(UserCancelReplace):
        create_rot47_cipher.validate_content(content)


@pytest.mark.strategy_rot47
def test_validate_content_when_incorrect_and_replace_then_correct(
    create_rot47_cipher, mock_replace_option_true
):
    content = "ab cd"
    corrected_content = "ab*cd"
    assert create_rot47_cipher.validate_content(content) == corrected_content


@pytest.mark.strategy_rot47
def test_when_cipher_abcd_then_2345(create_rot47_cipher):
    content = "abcd"
    cipher_content = "2345"
    assert create_rot47_cipher.cipher(content) == cipher_content
