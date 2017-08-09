import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
from pprint import pprint

import pandas
import numpy

library = '../'
post_id = '6eq9fa'
stop_words = set(stopwords.words("english"))
stop_words.update(['.', ',', '"', "'", '?', '!',
                   '>', "\'\'", "``", "...",
                   ':', ';', '(', ')', '[', ']', '{', '}'])
ps = PorterStemmer()


def removePeriod(words):
    count = 0
    for comm in words:
        if '.' in comm:
            ind = comm.index('.')
            fi = comm[:ind]
            ind += 1
            la = comm[ind:]
            words.append(fi)
            words.append(la)
            del words[count]
        count += 1


with open(library + post_id + '.txt', 'r') as file:
    comments = file.read()
    file.close()

words = word_tokenize(comments)

# filterwords = [w for w in words if not w in stop_words]
filterwords = []
for w in words:
    if not (w in stop_words):
        filterwords.append(w.lower())

fdist = FreqDist(filterwords)
print(fdist.tabulate(50))
print(stop_words)
