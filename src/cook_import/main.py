#!/usr/bin/env python3

import argparse
import re
import sys
import requests

from recipe_scrapers import (
    scrape_html,
    WebsiteNotImplementedError,
    NoSchemaFoundInWildMode,
)
from ingredient_parser import parse_ingredient

from .utils import (
    eprint,
    sub_lists,
    print_recipe,
    highlight_replacement_in_text,
    HEADERS,
)

single_stop_words = {
    "and", "or", "for", "the", "of", "powder", "syrup", "pinch",
    "cheese", "ground", "powdered", "seeds",
}
small_amount_words = {"dash", "pinch", "sprinkle", "smidgen", "drop", "bunch"}

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Automatically extract recipes from online websites."
    )
    parser.add_argument("-l", "--link", help="Input a URL link to a recipe")
    parser.add_argument(
        "-f",
        "--file",
        help="If you want the output to be in a file, use this flag. Otherwise defaults to console screen.",
        action="store_true",
    )
    return parser.parse_args()

def get_html_content(url):
    return requests.get(url, headers=HEADERS).content

def parse_recipe(html, url):
    try:
        return scrape_html(html, org_url=url)
    except WebsiteNotImplementedError as e:
        try:
            return scrape_html(html, org_url=url, wild_mode=True)
        except NoSchemaFoundInWildMode:
            raise ValueError(f"The domain {e.domain} is currently not supported.")

def parse_ingredients(ingredients):
    return [
        parse_ingredient(re.sub(r"\.", "", ingredient))
        for ingredient in ingredients
    ]

def process_instructions(instructions, ingredients_list):
    instructions = convert_timers(instructions)
    for ingredient in ingredients_list:
        instructions = process_ingredient(instructions, ingredient)
    return instructions.replace("\n", "\n\n")

def convert_timers(instructions):
    time_regex_match_str = r"(\d+|\d+\.\d+|\d+-\d+|\d+ to \d+) (min(?:utes)?|hours?|days?)"
    return re.sub(time_regex_match_str, r"~{\1%\2}", instructions)

def process_ingredient(instructions, combined_ingredient):
    ingredient_name = combined_ingredient.name.text
    quantity, unit = extract_quantity_and_unit(combined_ingredient)
    
    ing_regex_match_str = create_ingredient_regex(ingredient_name)
    ing_regex = re.compile(ing_regex_match_str, flags=re.I)
    
    match_obj = ing_regex.search(instructions)
    if match_obj is None:
        return instructions
    
    match_start, match_end = match_obj.start(1), match_obj.end(1)
    highlight_replacement_in_text(instructions, match_start, match_end)
    
    ing_replacement = create_ingredient_replacement(match_obj[1], quantity, unit)
    return instructions[:match_start] + ing_replacement + instructions[match_end:]

def extract_quantity_and_unit(combined_ingredient):
    quantity = combined_ingredient.amount[0].quantity
    unit = combined_ingredient.amount[0].unit
    
    if isinstance(quantity, (int, float)) and quantity % 1 == 0:
        quantity = int(quantity)
    if isinstance(quantity, float) and len(str(quantity)) > 5:
        quantity = f"{quantity:.2f}"
    if unit in small_amount_words and quantity == 0:
        quantity = 1
    
    return quantity, unit

def create_ingredient_regex(ingredient_name):
    ing_list = sub_lists(ingredient_name.split(" "))
    ing_list = list(filter(lambda x: len(x) > 0, ing_list))
    if len(ing_list) > 1:
        ing_list = list(filter(lambda x: x[0] not in single_stop_words, ing_list))
    ing_list = sorted(ing_list, reverse=True, key=lambda x: len(x))
    ing_regex_match_str = "|".join(
        [rf'\b{re.escape(" ".join(x))}\b' for x in ing_list]
    )
    return r"(" + ing_regex_match_str + r")"

def create_ingredient_replacement(ingredient, quantity, unit):
    if unit:
        return f"@{ingredient}{{{quantity}%{unit}}}"
    elif quantity == 0:
        return f"@{ingredient}{{}}"
    else:
        return f"@{ingredient}{{{quantity}}}"

def main():
    args = parse_arguments()
    if len(sys.argv) == 1:
        # Use argparse's print_help() method instead of the undefined parser variable
        parse_arguments().print_help()
        sys.exit()
    
    html = get_html_content(args.link)
    try:
        scraper = parse_recipe(html, args.link)
    except ValueError as e:
        print(str(e))
        sys.exit(1)
    
    title = scraper.title()
    image = scraper.image()
    total_time = scraper.total_time()
    
    eprint("Title:", title)
    eprint("Image:", image)
    
    instructions = scraper.instructions()
    ingredients_list = parse_ingredients(scraper.ingredients())
    
    eprint("\nDebug: Ingredients List")
    for idx, ingredient in enumerate(ingredients_list, 1):
        eprint(f"{idx}. {ingredient}")
    eprint("")
    
    instructions = process_instructions(instructions, ingredients_list)
    
    print_recipe(title, args.link, total_time, image, instructions, to_file=args.file)

if __name__ == "__main__":
    main()