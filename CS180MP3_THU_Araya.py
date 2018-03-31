from collections import defaultdict, OrderedDict
from mp3helpers import *
from time import time
import copy

parallel = False
lenDict = 50000

ppFilenames = list(map(pp_filename, filenameNos))#[:1000]
dictionary = defaultdict(int)

def map_task_multi(func, List):
    vals = []
    with Pool(processes=None) as pool:
        for val, i in zip(pool.imap(func, List), range(1, len(List)+1)):
            vals.append(val)
            if i % 1000 == 0:
                print(i, "out of", len(List))
    return vals

def map_task_single(func, List):
    vals = []
    for val, i in zip(map(func, List), range(1, len(List)+1)):
        vals.append(val)
        if i % 10 == 0:
            print(i, "out of", len(List))
    return vals

def step1(filename):
    #print('Reading', filename)
    rawEmail = read_file(filename)
    #print('Preprocessing', filename)
    ppEmail = preprocess(rawEmail)
    save_file((ppEmail, pp_filename(filename)))
    #return rawEmail

def step2(text):
    global dictionary
    for word in text.split(' '):
        dictionary[word] += 1
        #print(dictionary)

def step2_file(filename):
    #print('Processing', filename)
    step2(read_file(filename))

def read_dictionary():
    return(read_file('dictionary.txt').split('\n'))

def step3_file(filename):
    fileWords = read_file(filename).split(' ')
    return step3(fileWords)

def step3(fileWords):
    cp1 = time()
    fileDict = OrderedDict.fromkeys(dictionaryList, 0)
    cp2 = time()
    for word in fileWords:
        if word in fileDict:
            fileDict[word] += 1
    cp3 = time()
    #trainCsv.write(','.join(map(str, fileDict.values())) + '\n')
    print(cp2-cp1, cp3-cp2)
    return ','.join(map(str, fileDict.values()))


total=len(filenames)
print(str(total), 'filez')

"""
print('Doing step 1...')

if parallel:
    map_task_parallel(step1, filenames)
else:
    map_task_parallel(step1, filenames)
"""


"""
print('Doing step 2...')
wordLists = map_task_single(step2_file, ppFilenames)

print('Saving file...')
sortedTuples = sorted(dictionary.items(), key=lambda i: i[1], reverse=True)
save_file((
    '\n'.join(map(lambda i: i[0], sortedTuples[:lenDict])),
    'dictionary.txt'
    ))

"""

trainCsv = open('dataset-training.csv', 'w')
print('Doing step 3 alone...')
dictionaryList = read_dictionary()
dictionary = OrderedDict.fromkeys(dictionaryList, 0)
chunk = 100
vals = []
for val, i in zip(map(step3_file, ppFilenames), range(1, len(ppFilenames)+1)):
    vals.append(val)
    if i % 10 == 0:
        print(i, "out of", len(ppFilenames))
    if i % chunk == 0:
        print("writing")
        trainCsv.write('\n'.join(vals)+'\n')
        vals = []

trainCsv.write('\n'.join(vals)+'\n')
