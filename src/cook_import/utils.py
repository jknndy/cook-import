import sys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
}

def eprint(*args, **kwargs):
    """
    Print to standard error for the console.
    """
    print(*args, file=sys.stderr, **kwargs)

def sub_lists(lst):
    subs = [[]]
    for i in range(len(lst)):
        for j in range(i + 1, len(lst) + 1):
            subs.append(lst[i:j])
    return subs
def highlight_replacement_in_text(instructions, match_start, match_end):
    start = max(0, match_start - 18)
    end = min(len(instructions), match_end + 18)

    highlighted = instructions[start:end]
    pointer = " " * (match_start - start) + "^" * (match_end - match_start)

    eprint("...", highlighted, "...")
    eprint("...", pointer, "...")
    
def print_recipe(title, link, total_time, image, instructions, to_file=False):
    """
    Write the recipe to a file or print to stdout
    """
    recipe = [
        f">> source: {link}",
        f">> time required: {total_time} minutes",
        f">> image: {image}",
        "\n" + instructions,
    ]
    formatted_recipe = "\n".join(recipe) + "\n"
    
    if to_file:
        with open(f"{title}.cook", "w") as outfile:
            outfile.write(formatted_recipe)
    else:
        print(formatted_recipe)

def get_file_contents(filename):
    """
    Read and return the contents of a file
    """
    with open(filename, 'r') as file:
        return file.read()