import json
import difflib

# initializing
data = json.load(open("resources/dictionary.json"))
active = True

def word_search(word):
    """checks for word in the datafile"""
    if word in data:
        return word
    elif word.lower() in data:
        return word.lower()
    elif word.upper() in data:
        return word.upper()
    elif word.capitalize() in data:
        return word.capitalize()
    else:
        print("Word not found.")
        similarities(word)
        return False

def definition(word):
    """takes a word, passes it to datafile to print definition"""
    word = word_search(word)
    if word:
        print('\n{}:'.format(word.capitalize()))
        for no_of_def in data[word]:
            print('\n* {}'.format(no_of_def))

def similarities(word):
    """takes a word, passes it to datafile to provide similar words"""
    sim_list = difflib.get_close_matches(word, data.keys(), 3)
    if len(sim_list) > 1:
        print("Similar words found: ", end=" ")
        for w in sim_list[:-1]:
            print("'{}'".format(w), end=", ")
        print("'{}'.".format(sim_list[-1]))
    elif len(sim_list) == 1:
        print("A similar word found: '{}'".format(sim_list[0]))
    else:
        print("No similar words found.")

def retry():
    while True:
        # retry? y/n
        try:
            cont = str(input("\nTry again? (y/n)"))[0].lower()
            if cont == 'y':
                return True
            elif cont == 'n':
                return False
            else:
                print("\nInvalid. Try again")
        except:
            print("\nInvalid. Try again")

while active:
    # main script of Eng Dictionary
    definition(str(input("\nSelect the word you need definition for: ")))
    active = retry()

# on exit
print("\nThank you for using this English Dictionary")
