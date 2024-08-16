import pytest
from unittest.mock import patch, mock_open
from io import StringIO
import sys

from cook_import.utils import (
    eprint,
    sub_lists,
    highlight_replacement_in_text,
    print_recipe,
    get_file_contents
)

def test_eprint(capsys):
    eprint("Test error message")
    captured = capsys.readouterr()
    assert captured.err.strip() == "Test error message"


@pytest.mark.parametrize("to_file", [True, False])
def test_print_recipe(to_file, capsys):
    with patch('builtins.open', new_callable=mock_open) as mock_file:
        print_recipe("Test Recipe", "http://example.com", 30, "http://example.com/image.jpg", "Test instructions", to_file=to_file)
        
        if to_file:
            mock_file.assert_called_once_with("Test Recipe.cook", "w")
            mock_file().write.assert_called_once()
        else:
            captured = capsys.readouterr()
            assert ">> source: http://example.com" in captured.out
            assert ">> time required: 30 minutes" in captured.out
            assert ">> image: http://example.com/image.jpg" in captured.out
            assert "Test instructions" in captured.out

def test_get_file_contents():
    with patch('builtins.open', new_callable=mock_open, read_data="Test file contents"):
        content = get_file_contents("test.txt")
        assert content == "Test file contents"

# You can add more tests here as needed