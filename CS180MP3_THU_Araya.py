from collections import defaultdict, OrderedDict
from mp3helpers import *
from time import time
import copy
import numpy as np

lenDict = 40000
steps = [4]

ppFilenames = list(map(pp_filename, filenameNos))#[:1000]
testFilenames = ppFilenames[10000:70335:2]
trainFilenames = list(set(ppFilenames) - set(testFilenames))
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
    #cp1 = time()
    fileDict = OrderedDict.fromkeys(dictionaryList, 0)
    #cp2 = time()
    for word in fileWords:
        if word in fileDict:
            fileDict[word] += 1
    #cp3 = time()
    #trainCsv.write(','.join(map(str, fileDict.values())) + '\n')
    #print(cp2-cp1, cp3-cp2)
    return ','.join(map(str, fileDict.values()))

def step3_all(fnList, datasetFn):
    Csv = open(datasetFn, 'w')
    chunk = 100
    vals = []
    for val, i in zip(map(step3_file, fnList), range(1, len(fnList)+1)):
        vals.append(val)
        if i % 10 == 0:
            print(i, "out of", len(fnList))
        if i % chunk == 0:
            print("writing")
            Csv.write('\n'.join(vals)+'\n')
            vals = []
    Csv.write('\n'.join(vals)+'\n')

def step4():
    chunk = 10
    trainCsv = open('dataset-training.csv', 'r')
    model = BernoulliNb()
    ct = 0
    X = np.zeros((chunk, lenDict))
    for line in trainCsv:
        stuffs = line.split(',')
        print(len(stuffs))
        X[ct] = map(int, stuffs)

        ct += 1
        if ct == chunk:
            break
    print(X)


total=len(filenames)
print(str(total), 'files')

if 1 in steps:
    print('Doing step 1...')
    #map_task_multi(step1, filenames)
    map_task_single(step1, filenames)

if 2 in steps:
    print('Doing step 2...')
    wordLists = map_task_single(step2_file, ppFilenames)

    print('Saving file...')
    sortedTuples = sorted(dictionary.items(), key=lambda i: i[1], reverse=True)
    save_file((
        '\n'.join(map(lambda i: i[0], sortedTuples[:lenDict])),
        'dictionary.txt'
        ))

if 3 in steps:
    print('Doing step 3 alone...')
    dictionaryList = read_dictionary()
    step3_all(trainFilenames, 'dataset-training.csv')
    step3_all(testFilenames, 'dataset-test.csv')

if 4 in steps:
    print('Doing step 4...')
    step4()

