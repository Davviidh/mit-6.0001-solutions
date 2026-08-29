import string
def is_word_guessed(secret_word, letters_guessed):
    for i in secret_word:
        if i not in letters_guessed:
            return False
    return True
def get_guessed_word(secret_word, letters_guessed):
    word = ''
    for i in secret_word:
        if i not in letters_guessed:
            word += '_ '
        else:
            word += i
    return word
def get_available_letters(letters_guessed):
    letters = ''
    for i in string.ascii_lowercase:
        if i not in letters_guessed:
            letters += i
    return letters
print(is_word_guessed('apple', ['a', 'p', 'l', 'e']))