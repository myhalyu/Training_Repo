import random

file_path = 'D:\Python\Repo\Training_Repo\dict.txt'  # path for input file
unknown_symbol = '_'  # used to show unknown letters
read_array = []  # initialize array to store words from original file
word_array = []  # initialize array to store validated words
congrats_message = 'Congratulations! You have guessed the word '  # message to be shown when word is guessed


def read_file(path):  # read file as is
    array = []
    array = open(path).readlines()
    return array


def validate_records(array):  # filter out records with numbers and special symbols; remove spaces, make letters uppercase
    validated_array = []
    for i in range(0, len(array)):
        if str(array[i]).replace('\n', '').isalpha():
            validated_array.append(str(array[i]).replace('\n', '').upper().strip())
    return validated_array


def select_word(array):  # selecting one word from array
    word = array[random.randint(0, len(word_array) - 1)]
    return word


def blind_word(word, symbol):  # creating word with only unknown letters
    blinded_word = symbol * len(word)  # type = str
    return blinded_word


def guess_letter():  # single guess attempt; validation for input letter
    enter_message = 'Please enter your letter:\n'
    error_message = 'You need to specify letter:\n '
    symbol = input(enter_message).upper()
    while True:
        if symbol.isalpha():
            break
    else:
        symbol = input(error_message).upper()
    return symbol


def check_symbol(symbol, guess_word, current_word):  # checking if guessed letter is present in word
    if symbol in guess_word:
        for i in range(0, len(current_word)):
            if guess_word[i] == guess:
                current_word = current_word[:i] + guess + current_word[i + 1:]
    else:
        print('No luck, the letter %s is not in this word. Try again' % symbol)
    return current_word


read_array = read_file(file_path)  # read file as is
word_array = validate_records(read_array)  # validation for words
guess_word = select_word(word_array)  # selecting word
current_word = blind_word(guess_word, unknown_symbol)  # creating word with only unknown letters

print(current_word + ' (' + str(len(current_word)) + ' letters in total)')  # printing guessed word and letters count

i=0

while True:
    guess = guess_letter()
    current_word = check_symbol(guess, guess_word, current_word)
    i += 1
    print(current_word)
    if current_word.count(unknown_symbol) == 0:
        print(congrats_message + guess_word + '. You have spent %d attempts' % i)
        break
