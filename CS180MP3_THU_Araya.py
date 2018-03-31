import nltk
from collections import Counter
from mp3helpers import *
import re

parallel = True

patterns_to_remove = [
        re.compile('<style>.*</style>', re.S),
        re.compile('<.*?>', re.S)
]

tokenPositives = [
    re.compile('^[A-Za-z0-9\-\.]{1,30}$')
]

tokenNegatives = [
    re.compile('^[\-\.]+$')
]

# from https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s19.html
def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)

#preprocess('trec07p/data/inmail.58044', encoding='utf_8')

#groups = group(which_encoding, filenames)
#show_group_stats(groups)

makedir('preprocess')

def pp_filename(filename):
    return 'preprocess/inmail.' + filename.split('.')[-1]

def preprocess(text):
    def email_obj_is_text(emailObj):
        return emailObj.get_content_type() == 'text/plain' or emailObj.get_content_type() == 'text/html'

    emailObj = email.message_from_string(text)
    addtl_words = []
    # from and subject attributes added
    addtl_words.append(emailObj['From'])
    if emailObj['Subject']:
        addtl_words.append(emailObj['Subject'])
    # if multipart, walk through all parts, get all text shits
    if emailObj.is_multipart():
        payloads = emailObj.walk()
        b = ' '.join((map(lambda p: p.get_payload(),
            filter(email_obj_is_text, payloads))))
        body = b
    elif email_obj_is_text(emailObj):
        body = emailObj.get_payload()
    else:
        body = emailObj.get_content_type().replace('/', '')
    for r in patterns_to_remove:
        body = re.sub(r, '', body)
    body = body.replace('\x92', "'")
    body = body.replace('=92', "'")
    body = body.replace('=20', ' ')
    body = (body + '\n' + '\n'.join(addtl_words)).lower()
    tokens = nltk.word_tokenize(body)
    for tp in tokenPositives:
        tokens = filter(tp.match, tokens)
    for tn in tokenNegatives:
        tokens = filter(lambda tok: not tn.match(tok), tokens)
    body = ' '.join(tokens)
    #body = '=================OLD:\n' + text + '==================NEW:\n' + body
    return body

def step1(filename):
    #print('Reading', filename)
    rawEmail = read_file(filename)
    #print('Preprocessing', filename)
    ppEmail = preprocess(rawEmail)
    save_file((ppEmail, pp_filename(filename)))
    #return rawEmail

def step2(text):
    pass

def step2_file(filename):
    pass

print('Doing step 1...')
total=len(filenames)
print(str(total), 'files')

if parallel:
    with Pool(processes=None) as pool:
        for _, i in zip(pool.imap_unordered(step1, filenames), range(1, total+1)):
            #print('%d out of %d, %.2f%%' % (i, total, i / total * 100))
            pass
else:
    for _, i in zip(map(step1, filenames), range(1, total+1)):
        pass
    #print('%d out of %d, %.2f%%' % (i, total, i / total * 100))
#print('Saving...')
#save_as_one_file(ppEmails)

