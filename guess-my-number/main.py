from os import name, system
from random import randint


# Variables for generating random numbers and number of guesses.
# Change these for different kinds of games.
lower_bound = 1
upper_bound = 100
attempts = 10


def clear_screen():
    """Clear a terminal screen by issuing commands."""
    if name == "nt":
        system("cls")
    else:
        system("clear")


# Main program.
if __name__ == "__main__":
    clear_screen()

    # Pick a random number and set the remaining guesses.
    number = randint(lower_bound, upper_bound)
    remaining_guesses = attempts

    # Print information out to the screen.
    print("I'm thinking of a number between {} and {}.".format(lower_bound,
        upper_bound))
    print("You have {} tries to guess my number.".format(attempts))
    print("Can you guess what it is?")

    # Until the user has no more guesses...
    while remaining_guesses > 0:
        try:
            # Attempt to get an integer input from the user.
            guess = int(input("\n{} remaining guesses: ".format(
                remaining_guesses)))

            clear_screen()

            # Check users guess.
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
            # User didn't input an integer, report error.
            print("My number is an integer!")
            remaining_guesses -= 1

    # Game over.
    if remaining_guesses > 0:
        # User won.
        print("The number was {}. Well done. :D".format(number))
    else:
        # User lost.
        print("You couldn't guess my number. Better luck next time!")
