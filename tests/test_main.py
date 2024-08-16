import re
from unittest.mock import patch, MagicMock


from cook_import.main import (
    parse_arguments,
    parse_ingredients,
    convert_timers,
    create_ingredient_replacement,
)

def test_parse_arguments():
    with patch('sys.argv', ['cook_import.py', '-l', 'http://example.com', '-f']):
        args = parse_arguments()
        assert args.link == 'http://example.com'
        assert args.file == True


def test_parse_ingredients():
    ingredients = ['1 cup flour', '2 eggs']
    result = parse_ingredients(ingredients)
    assert len(result) == 2
    assert result[0].name.text == 'flour'
    assert result[1].name.text == 'eggs'

def test_convert_timers():
    instructions = "Cook for 30 minutes, then wait for 2 hours"
    result = convert_timers(instructions)
    assert result == "Cook for ~{30%minutes}, then wait for ~{2%hours}"

def test_create_ingredient_replacement():
    result = create_ingredient_replacement("flour", 2, "cups")
    assert result == "@flour{2%cups}"

