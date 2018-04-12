import random
from mp3helpers import *
def game():
    total = 0
    correct = 0
    while True:
        print('==============SPAM FILTER: THE GAME==================')
        input('Is this spam? Or is this ham? Enter y to see the email: ')
        filename = random.choice(filenames)
        print(read_file(filename))
        spamorham = input('Type "spam" if you think this is spam. Otherwise, type "ham": ')
        if spamorham == is_spam(filename):
            print('CORRECT! It is ' + spamorham + '.')
            correct += 1
        else:
            print('WRONG! It is ' + is_spam(filename) + '.')
        total += 1
        asdf = input('Try again? (y/n)')
        if asdf != 'y':
            break
    print('You made', correct, 'correct choices out of', total, 'total choices, so', correct / total * 100, '% is your accuracy. Congratulations!')

game()
