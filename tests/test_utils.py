import pytest
from unittest.mock import patch, mock_open

from cook_import.utils import (
    sub_lists,
    print_recipe,
    get_file_contents,
)



@pytest.mark.parametrize("to_file", [True, False])
def test_print_recipe(to_file, capsys):
    with patch("builtins.open", new_callable=mock_open) as mock_file:
        print_recipe(
            "Test Recipe",
            "http://example.com",
            30,
            "http://example.com/image.jpg",
            "Test instructions",
            to_file=to_file,
        )

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
    with patch("builtins.open", new_callable=mock_open, read_data="Test file contents"):
        content = get_file_contents("test.txt")
        assert content == "Test file contents"



@pytest.mark.parametrize(
    "lst, expected",
    [
        ([], [[]]),
        ([1], [[], [1]]),
        ([1, 2], [[], [1], [2], [1, 2]]),
        ([1, 2, 3], [[], [1], [2], [3], [1, 2], [2, 3], [1, 2, 3]]),
    ],
)
def test_sub_lists(lst, expected):
    result = sub_lists(lst)
    assert result == expected
