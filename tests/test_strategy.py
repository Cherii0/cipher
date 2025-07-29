from src.strategy import CipherFactory, EmptyRotMethods, ROT13Strategy
import pytest

@pytest.mark.factory
def test_should_return_type_list():
    assert  isinstance(CipherFactory.get_rot_methods(), list)

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