import sqlite3
import pickle
from pprint import pprint

import random
import nltk
from nltk import FreqDist
from nltk.tokenize import word_tokenize

pickle_file = "naive_bayes_classifier.pickle"
SQL_query = '''
SELECT c.body, s.title
FROM comments as c, submissions as s
WHERE s.submission_id = c.submission_id
AND s.label = 'Self-post'
AND s.submission_id = '6jdbvq';
'''

# Connect to database a obtain all comments with given labels
db = sqlite3.connect('../canada_subreddit_test.db')
cur = db.cursor()
cur.execute(SQL_query)
comments = [(c[0],c[1]) for c in cur]
db.close()

random.shuffle(comments)

all_words = []
for c in comments:
    tokens = word_tokenize(c[0])
    for w in tokens:
        all_words.append(w.lower())
all_words = FreqDist(all_words)

# Get a random set of the words to use as features
word_features = list(all_words.keys())[:3000]

def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

featuresets = [(find_features(word_tokenize(c[0])), c[1], c[0]) for c in comments]

with open(pickle_file,"rb") as file:
    classifier = pickle.load(file)
    file.close()

for f in featuresets:
    print('Title:', f[1])
    print('Guess:', classifier.classify(f[0]))
    print('Comment:','\n' + f[2])
    print('\n\n')
    # print(classifier.classify(f[0]),'\t',str(f[3]))
