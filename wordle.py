"""
Solves the WORDLE game.

 - Guess the WORDLE in 6 tries.
 - Each guess must be a valid 5 letter word.
 - After each guess, the color of the tiles will change to show how 
   close your guess was to the word.

Author: John Q
Date: 1 July 2022
"""


import emoji
import json
import pprint


def check_guess(g, a, r, e, debug=False):
    "Checks the guess using user input."

    print('Is the letter:')
    print(' 1) In the word and in the correct spot?')
    print(' 2) In the word but in the wrong spot?')
    print(' 3) Not in the word in any spot?')

    # Iterate over the guess
    for i in range(0, len(g)):

        # If the position is known, then skip it
        if len(a[i]) == 1:
            print(g[i] + '?: 1')
            # Update the emoji string
            e += ':green_square:'

        # If the position is unknown, then check it
        else:
            # Ask the user
            opt = int(input(g[i] + '?: '))

            if opt == 1:
                # This letter is correct in this position
                a[i] = [g[i]]
                # Add the letter to the list of required letters
                if g[i] not in r:
                    r.append(g[i])
                # Update the emoji string
                e += ':green_square:'
            
            elif opt == 2:
                # This letter is incorrect in this position
                if g[i] in a[i]:
                    a[i].remove(g[i])
                # The letter still needs to be somewhere in the word
                # So add it to the list of required letters
                if g[i] not in r:
                    r.append(g[i])
                # Update the emoji string
                e += ':yellow_square:'
            
            elif opt == 3:
                # This letter is correct in no positions
                if g[i] in a[0]:
                    a[0].remove(g[i])
                if g[i] in a[1]:
                    a[1].remove(g[i])
                if g[i] in a[2]:
                    a[2].remove(g[i])
                if g[i] in a[3]:
                    a[3].remove(g[i])
                if g[i] in a[4]:
                    a[4].remove(g[i])
                # Update the emoji string
                e += ':black_large_square:'
            else:
                print('ERROR!')

    # Update the emoji string
    e += '\n'

    if debug:
        pprint.pprint(a)
        pprint.pprint(r)
        print(emoji.emojize(e))

    # Return the updated answer dictionary
    # and the updated list of required letters
    return a, r, e


def list_valid_words(a, r, debug=False):
    "Compiles a list of words that are valid answers."

    dictionary_filename = 'words.json'

    # Load the word list from the json file into a Python dictionary
    with open(dictionary_filename, 'r') as json_file:
        word_dict = json.load(json_file)

    # Initialize the list of valid words
    val_words = []

    # Iterate over the word list dictionary
    for w in word_dict:
        # Determine whether the word is a valid answer
        if is_valid(w, a, r, debug):
            val_words.append(w)

    if debug: pprint.pprint(val_words)

    # Return the list of valid words
    return val_words


def is_valid(w, a, r, debug=False):
    """Determines whether a word is a valid answer."""

    # Check that the length of the word is equal to 5
    if len(w) != 5:
        return False    # Word is invalid => return False

    # Check if the word is capitalized (i.e., is a proper noun)
    if w[0].isupper():
        return False    # Word is invalid => return False

    # Convert the word to uppercase
    w = w.upper()

    # Check that the word includes all of the required letters
    for l in r:
        if l not in list(w):
            return False    # Word is invalid => return False

    # Iterate over the letters in the word and check if they match the answer
    for i in range(0, len(w)):
        if w[i] not in a[i]:
            return False    # Word is invalid => return False

    # If the word hasn't been discarded yet, this means that it matches the answer
    # and only includes valid and unknown letters
    return True    # Word is valid => return True


def is_in_wordle_list(g, debug=False):
    "Checks if the guess is in the Wordle word list using user input."

    print('')
    print('Is the word: ' + str(g).upper() + ' in the Wordle word list?')

    opt = str(input('Y/N: ')).upper()

    if opt == 'Y' or opt == 'YES':
        return True
    elif opt == 'N' or opt == 'NO':
        return False


if __name__ == "__main__":
    # Set debug
    debug = False

    # Initialize the answer
    answer = {0:['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],\
              1:['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],\
              2:['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],\
              3:['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],\
              4:['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],}

    # Initialize a list of the required letters
    req_letters = []

    # Initialize the emoji string
    emoji_str = ''

    # Generate guesses
    guesses = list_valid_words(answer, req_letters, debug)

    # Initialize the number of attempts
    trys = 1

    while trys <= 6:
        # Check if the guess is in the Wordle word list
        for guess in guesses:
            if trys == 1:
                # Hard-code the first guess to 'ADIEU'
                guess = 'ADIEU'
                # Break out of the loop
                break
            elif is_in_wordle_list(guess):
                # The guess is in the word list
                guess = guess.upper()
                # Break out of the loop
                break
            else:
                continue

        print('')
        print('Guess Number ' + str(trys) + ': ' + guess)
        print('---------------------')

        # Check the guess
        answer, req_letters, emoji_str = check_guess(guess, answer, req_letters, emoji_str, debug)

        # Check if the WORDLE has been solved
        if len(answer[0]) == 1 and len(answer[1]) == 1 and len(answer[2]) == 1 and len(answer[3]) == 1 and len(answer[4]) == 1:
            # The WORDLE has been solved!
            break

        # Generate new guesses
        guesses = list_valid_words(answer, req_letters, debug)

        # 
        if len(guesses) == 0:
            print('')
            print('No More Guesses...')
            trys = 9
            break

        # Increment the number of attempts
        trys += 1

    if trys <=6:
        print('')
        print('The answer to the WORDLE is:')
        print('    ' + answer[0][0] + answer[1][0] + answer[2][0] + answer[3][0] + answer[4][0])
        print('')
        print('Found in ' + str(trys) + ' guesses.')
        print('')
    elif trys > 6:
        print('')
        print('Failed to solve the WORDLE!')
        print('')

    # Print the emoji wrapup
    print(emoji.emojize(emoji_str))
