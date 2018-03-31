import glob
import email
from multiprocessing import Pool
from os import mkdir, path
import nltk
import random
try:
    from random_shit import *
except ImportError:
    pass


"""
list of filenames
"""
filenames = glob.glob(path.join('trec07p', 'data', 'inmail.*'))#[:1000]
filenameNos = map(lambda x: x.split('.')[-1], filenames)

"""
list of strings that are either 'ham'/'spam' based on whether the email is ham/spam.
"""
checker = [''] + [line.split()[0] for line in open(path.join('trec07p', 'full', 'index'), 'r').readlines()]

"""
returns 'ham' if email is ham, else returns 'spam'
"""
def is_spam(filename):
    return checker[int(filename.split('.')[-1])]

"""
reads file with encoding latin-1
"""
def read_file(filename):
    with open(filename, 'r', encoding='latin-1') as fileObj:
        emailStr = fileObj.read()
    #print(filename)
    return emailStr

"""
given a tuple (text, filename) save it in encoding latin-1
"""
def save_file(data):
    with open(data[1], 'w', encoding='latin-1') as fileObj:
        emailStr = fileObj.write(data[0])

"""
make directory if not exists
"""
def makedir(newdir):
    if not path.exists(newdir):
        mkdir(newdir)


"""
return which encoding did not produce an error out of the choices below.
if all produced an error, return 'weird'
"""
def which_encoding(filename):
    emailStr = None
    encodings = ['utf_8', 'cp1252']
    for enc in encodings:
        fileObj = open(filename, 'r', encoding=enc)
        try:
            emailStr = fileObj.read()
        except UnicodeDecodeError:
            fileObj.close()
        else:
            fileObj.close()
            return enc
    if emailStr == None:
        return 'weird'

"""
using a grouping function, return which emails in each group are spam/ham
"""
def group(grouping_function, filenames):
    groups = {}
    pool = Pool(processes=None)
    #email_groups = list(map(grouping_function, filenames))
    email_groups = pool.map(grouping_function, filenames)
    for i in range(len(email_groups)):
        grp = str(email_groups[i])
        if grp not in groups.keys():
            groups[grp] = {'spam': 0, 'ham': 0}
        groups[grp][is_spam(filenames[i])] += 1
    return groups

"""
pretty prints the output generated by group()
"""
def show_group_stats(groups):
    s = 10 
    s_g = 10
    def printl_g(string):
        print(str(string).ljust(s_g), end='')
    def printl(string):
        print(str(string).ljust(s), end='')
    def printr(string):
        print(str(string).rjust(s), end='')
    printl_g(' ')
    printl('ham')
    printl('spam')
    printl('total')
    print()
    for key in groups:
        printl_g(key)
        printr(groups[key]['ham'])
        printr(groups[key]['spam'])
        printr(sum(groups[key].values()))
        print()
    printl_g('total')
    hams = sum([groups[key]['ham'] for key in groups])
    spams = sum([groups[key]['spam'] for key in groups])
    printr(hams)
    printr(spams)
    printr(hams+spams)
    print()


