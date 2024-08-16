#!/usr/bin/env python3

import argparse
import sys
from cook_import.main import (
    get_html_content,
    parse_recipe,
    parse_ingredients,
    process_instructions,
)
from cook_import.utils import print_recipe

from cook_import.utils import eprint

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
    return parser, parser.parse_args()

def main():
    parser, args = parse_arguments()
    if len(sys.argv) == 1:
        parser.print_help()
        return 1

    if not args.link:
        print("Error: The --link argument is required.", file=sys.stderr)
        parser.print_help()
        return 1

    try:
        html = get_html_content(args.link)
        scraper = parse_recipe(html, args.link)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1

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
    return 0

if __name__ == "__main__":
    sys.exit(main())