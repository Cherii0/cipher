import pytest
import sys
sys.path.append("../src")
from src.file_handler import FileHandler


@pytest.mark.write
@pytest.mark.parametrize("input_", ["12345", "abcd"])
def test_write_correct_content_then_read_it_if_equal_then_pass(tmpdir, input_):
    output_file = tmpdir.join("output.txt")
    FileHandler.write(str(output_file), content=input_)
    assert output_file.read() == input_

@pytest.mark.write
@pytest.mark.parametrize("filepath", ["file.file", "file.ABCD", "filefile"])
def test_when_incorrect_filepath_then_proper_output_info(capsys, filepath):
    warning = "given filepath has no extension txt or json\n"
    FileHandler.write(filepath=filepath, content="abcd")
    stdout, stderr = capsys.readouterr()
    assert stdout == warning

