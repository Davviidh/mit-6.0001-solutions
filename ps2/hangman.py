# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    for i in secret_word:
        if i not in letters_guessed:
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    word = ''
    for i in secret_word:
        if i not in letters_guessed:
            word += '_ '
        else:
            word += i
    return word



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    letters = ''
    for i in string.ascii_lowercase:
        if i not in letters_guessed:
            letters += i
    return letters

    

def hangman(secret_word):
    n = 6
    vowels = ['a', 'e', 'i', 'o', 'u']
    l = len(secret_word)
    letters_guessed = []
    warnings = 3
    print(f'''
      Welcome to the game Hangman!
      I am thinking of a word that is {l} letters long
      You have 3 warnings left
      ------------------------''')
    while n > 0:
      letter = str.lower(input(f'''
      ---------------------------
      You have {n} guesses left. 
      Available letters: {get_available_letters(letters_guessed)} 
      Please guess a letter: ''' ))
      if not str.isalpha(letter):
        warnings -= 1
        if warnings < 0:
          print(f"Oops! That is not a valid letter. You have no warnings left: {get_guessed_word(secret_word, letters_guessed)}")
          n -= 1
        else:
          print(f"Oops! That is not a valid letter. You have {warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
      elif letter in letters_guessed:
        warnings -= 1
        if warnings < 0:
          print(f"Oops! You've already guessed that letter. You have no warnings left: {get_guessed_word(secret_word, letters_guessed)}")
          n -= 1
        else:
          print(f"Oops! You've already guessed that letter. You now have {warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
      else:
        letters_guessed.append(letter)
        if letter not in secret_word:
          print(f'''
      That letter is not in my word! {get_guessed_word(secret_word, letters_guessed)}''')
          if letter in vowels:
            n -= 2
          else:
            n -= 1
        else:
          print(f'''
      That letter is in my word! {get_guessed_word(secret_word, letters_guessed)}''')
          if is_word_guessed(secret_word, letters_guessed):
            return (True, n*(len(set(secret_word))))
    return (False, secret_word)




# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    my_word = my_word.replace(" ", "")
    
    # Check lengths
    if len(my_word) != len(other_word):
        return False
        
    # Gather revealed letters
    revealed_letters = set()
    for i in my_word:
        if i != '_':
            revealed_letters.add(i)
            
    # Loop through and check each position
    for i in range(len(my_word)):
        if my_word[i] != '_':
            if my_word[i] != other_word[i]:
                return False
        else:
            if other_word[i] in revealed_letters:
                return False
    return True



def show_possible_matches(my_word):
    res = []
    for i in wordlist:
       if match_with_gaps(my_word, i):
          res.append(i)
    if len(res) > 0:
       print(" ".join(res))
    else:
       print("No mathces found")
show_possible_matches('t_ _ t')



def hangman_with_hints(secret_word):
    n = 6
    vowels = ['a', 'e', 'i', 'o', 'u']
    l = len(secret_word)
    letters_guessed = []
    warnings = 3
    print(f'''
      Welcome to the game Hangman!
      I am thinking of a word that is {l} letters long
      You have 3 warnings left
      ------------------------''')
    while n > 0:
      letter = str.lower(input(f'''
      ---------------------------
      You have {n} guesses left. 
      Available letters: {get_available_letters(letters_guessed)} 
      Please guess a letter: ''' ))
      if letter == '*':
         show_possible_matches(get_guessed_word(secret_word, letters_guessed))
      else:
        if not str.isalpha(letter):
          warnings -= 1
          if warnings < 0:
            print(f"Oops! That is not a valid letter. You have no warnings left: {get_guessed_word(secret_word, letters_guessed)}")
            n -= 1
          else:
            print(f"Oops! That is not a valid letter. You have {warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
        elif letter in letters_guessed:
          warnings -= 1
          if warnings < 0:
            print(f"Oops! You've already guessed that letter. You have no warnings left: {get_guessed_word(secret_word, letters_guessed)}")
            n -= 1
          else:
            print(f"Oops! You've already guessed that letter. You now have {warnings} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
        else:
          letters_guessed.append(letter)
          if letter not in secret_word:
            print(f'''
        That letter is not in my word! {get_guessed_word(secret_word, letters_guessed)}''')
            if letter in vowels:
              n -= 2
            else:
              n -= 1
          else:
            print(f'''
        That letter is in my word! {get_guessed_word(secret_word, letters_guessed)}''')
            if is_word_guessed(secret_word, letters_guessed):
              return (True, n*(len(set(secret_word))))
    return (False, secret_word)



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
#     # pass

#     # To test part 2, comment out the pass line above and
#     # uncomment the following two lines.
    
#     secret_word = choose_word(wordlist)
#     res = hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    res = hangman_with_hints(secret_word)
    if res[0]:
      print(f'''
      You Won!
      Your total score is: {res[1]}
            ''')
    else:
       print(f'You lose! The word was {res[1]}')
