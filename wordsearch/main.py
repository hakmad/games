from os import name, system
from random import choice, randint


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
    if name == "nt":
        system("cls")
    else:
        system("clear")


def select_words(min_word_length, max_word_length, number_of_words,
        word_file):
    selected_words = []

    with(open(word_file, "r")) as file:
        words = file.read().splitlines()

    for i in range(number_of_words):
        word = choice(words)
        while not(min_word_length <= len(word) <= max_word_length):
            word = choice(words)

        selected_words.append(word.upper())

    return selected_words


def make_wordsearch(words, grid_width, grid_height):
    grid = [["" for x in range(grid_size)] for y in range(grid_size)]

    for word in words:
        word_length = len(word)

        placed = False
        placeable = False

        while not placed:
            if not placeable:
                start_x = randint(0, grid_width - 1)
                start_y = randint(0, grid_height - 1)

                d_x, d_y = choice(directions)

                placeable = True

            end_x = start_x + (word_length * d_x)
            end_y = start_y + (word_length * d_y)

            if not(0 <= end_x <= grid_width - 1) or \
                not(0 <= end_y <= grid_height - 1):
                placeable = False
            else:
                for i in range(word_length):
                    current_letter = word[i]
                    
                    letter_x = start_x + ((i + 1) * d_x)
                    letter_y = start_y + ((i + 1) * d_y)

                    grid_letter = grid[letter_x][letter_y]

                    if not(len(grid_letter) == 0):
                        if not(grid_letter == current_letter):
                            placeable = False
                            break

                if placeable:
                    for i in range(word_length):
                        current_letter = word[i]

                        letter_x = start_x + ((i + 1) * d_x)
                        letter_y = start_y + ((i + 1) * d_y)

                        grid[letter_x][letter_y] = current_letter

                    placed = True

    for y in range(len(grid)):
        row = grid[y]

        for x in range(len(row)):
            grid_letter = grid[x][y]

            if len(grid_letter) == 0:
                grid[x][y] = chr(randint(0, alphabet_length - 1) + ord("A"))

    return grid


def pretty_print_words(words):
    for i in range(0, len(words), 2):
        print("%-12s\t%11s" % (words[i], words[i + 1]))
    print()


def pretty_print_wordsearch(grid):
    for row in grid:
        for letter in row:
            print(letter, end=" ")
        print()
    print()


if __name__ == "__main__":
    clear_screen()

    words = select_words(min_word_length, max_word_length, number_of_words,
            word_file)
    wordsearch = make_wordsearch(words, grid_size, grid_size)

    pretty_print_wordsearch(wordsearch)
    pretty_print_words(words)
