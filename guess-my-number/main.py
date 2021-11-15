from os import name, system
from random import randint


lower_bound = 1
upper_bound = 100
attempts = 10


def clear_screen():
    if name == "nt":
        system("cls")
    else:
        system("clear")


if __name__ == "__main__":
    clear_screen()

    number = randint(lower_bound, upper_bound)
    remaining_guesses = attempts

    print("I'm thinking of a number between {} and {}.".format(lower_bound,
        upper_bound))
    print("You have {} tries to guess my number.".format(attempts))
    print("Can you guess what it is?")

    while remaining_guesses > 0:
        try:
            guess = int(input("\n{} remaining guesses: ".format(
                remaining_guesses)))

            clear_screen()

            if guess > number:
                print("Too high!")
                remaining_guesses -= 1
            elif guess < number:
                print("Too low!")
                remaining_guesses -= 1
            else:
                print("Correct!")
                break

        except ValueError:
            print("My number is an integer!")
            remaining_guesses -= 1

    if remaining_guesses > 0:
        print("The number was {}. Well done. :D".format(number))
    else:
        print("You couldn't guess my number. Better luck next time!")
