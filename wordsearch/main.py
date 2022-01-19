from os import name, system
from random import choice, randint


# Various settings.
# Change these to adjust wordsearch output.
alphabet_length = 26

directions = [
        (1, 1),
        (1, 0),
        (1, -1),
        (0, 1),
        (0, -1),
        (-1, 1),
        (-1, 0),
        (-1, -1)
        ]

word_file = "words.txt"

min_word_length = 4
max_word_length = 10

number_of_words = 10

grid_size = 14


def clear_screen():
    """Clear the terminal by issuing system commands."""
    if name == "nt":
        system("cls")
    else:
        system("clear")


def select_words(min_word_length, max_word_length, number_of_words,
        word_file):
    """Select words from a word file.

    Arguments:
    min_word_length (int) - minimum word length to select.
    max_word_length (int) - maximum word length to select.
    number_of_words (int) - number of words to select.
    word_file (str) - file name of file containing words to select.

    Returns:
    selected_words (list) - list of words.
    """
    selected_words = []

    # Open file and get list of all words.
    with(open(word_file, "r")) as file:
        words = file.read().splitlines()

    # Repeat for as many number of words needed.
    for i in range(number_of_words):
        # Select random word from list of words.
        word = choice(words)
        while not(min_word_length <= len(word) <= max_word_length):
            word = choice(words)

        # Add selected word to word list.
        selected_words.append(word.upper())

    return selected_words


def make_wordsearch(words, grid_width, grid_height):
    """Create a word search based on a set of words and some sizes.

    Arguments:
    words (list) - list of words.
    grid_width (int) - width of wordsearch grid.
    grid_height (int) - height of wordsearch grid.

    Returns:
    grid (str) - a wordsearch grid.
    """
    # Create empty grid.
    grid = [["" for x in range(grid_size)] for y in range(grid_size)]

    # For every word.
    for word in words:
        word_length = len(word)

        placed = False
        placeable = False

        # While word hasn't been added to grid.
        while not placed:
            # Check if word can be placed in grid.
            if not placeable:
                start_x = randint(0, grid_width - 1)
                start_y = randint(0, grid_height - 1)

                d_x, d_y = choice(directions)

                placeable = True

            end_x = start_x + (word_length * d_x)
            end_y = start_y + (word_length * d_y)

            if not(0 <= end_x <= grid_width - 1) or \
                not(0 <= end_y <= grid_height - 1):
                # Word won't fit, stop.
                placeable = False
            else:
                # Check if grid areas have any characters already in them.
                for i in range(word_length):
                    current_letter = word[i]
                    
                    letter_x = start_x + ((i + 1) * d_x)
                    letter_y = start_y + ((i + 1) * d_y)

                    grid_letter = grid[letter_x][letter_y]

                    if not(len(grid_letter) == 0):
                        if not(grid_letter == current_letter):
                            # Word can't be placed, stop.
                            placeable = False
                            break

                if placeable:
                    # Word can be put on wordsearch, add it.
                    for i in range(word_length):
                        current_letter = word[i]

                        letter_x = start_x + ((i + 1) * d_x)
                        letter_y = start_y + ((i + 1) * d_y)

                        grid[letter_x][letter_y] = current_letter

                    placed = True

    # Fill grid with random letters.
    for y in range(len(grid)):
        row = grid[y]

        for x in range(len(row)):
            grid_letter = grid[x][y]

            if len(grid_letter) == 0:
                grid[x][y] = chr(randint(0, alphabet_length - 1) + ord("A"))
    
    #
    return grid


def pretty_print_words(words):
    """Print words nicely.

    Arguments:
    words (list) - list of words to print.
    """
    for i in range(0, len(words), 2):
        print("%-12s\t%11s" % (words[i], words[i + 1]))
    print()


def pretty_print_wordsearch(grid):
    """Print a wordsearch nicely.

    Arguments:
    grid (str) - a wordsearch grid.
    """
    for row in grid:
        for letter in row:
            print(letter, end=" ")
        print()
    print()


# Main program.
if __name__ == "__main__":
    # Clear screen.
    clear_screen()

    # Select words and create wordsearch.
    words = select_words(min_word_length, max_word_length, number_of_words,
            word_file)
    wordsearch = make_wordsearch(words, grid_size, grid_size)

    # Show wordsearch and words.
    pretty_print_wordsearch(wordsearch)
    pretty_print_words(words)
