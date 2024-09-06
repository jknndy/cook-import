HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
}


def sub_lists(lst):
    subs = [[]]
    for i in range(len(lst)):
        for j in range(i + 1, len(lst) + 1):
            subs.append(lst[i:j])
    subs.sort(key=lambda x: (len(x), lst.index(x[0]) if x else -1))
    return subs


def print_recipe(title, link, total_time, image, instructions, to_file=False):
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
    with open(filename, "r") as file:
        return file.read()
