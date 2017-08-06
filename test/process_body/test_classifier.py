import sqlite3
import pickle
from pprint import pprint

import random
import nltk
from nltk import FreqDist
from nltk.tokenize import word_tokenize

pickle_file = "logreg_classifier.pickle"
SQL_query = '''
SELECT c.body, s.title, s.label
FROM comments as c, submissions as s
WHERE s.submission_id = c.submission_id
AND s.created <= '2017-08-01'
AND s.created >= '2017-07-27';
'''

# Connect to database a obtain all comments with given labels
db = sqlite3.connect('../canada_subreddit_test.db')
cur = db.cursor()
cur.execute(SQL_query)
comments = [(c[0],c[1],c[2]) for c in cur]
db.close()

random.shuffle(comments)

all_words = []
for c in comments:
    tokens = word_tokenize(c[0])
    for w in tokens:
        all_words.append(w.lower())
all_words = FreqDist(all_words)
-
# Get a random set of the words to use as features
word_features = list(all_words.keys())[:3000]

def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

featuresets = [(find_features(word_tokenize(c[0])), c[0], c[1], c[2]) for c in comments]

with open(pickle_file,"rb") as file:
    classifier = pickle.load(file)
    file.close()

counter = 0
with open("test_output.txt","wb") as file:
    for f in featuresets:
        guess = classifier.classify(f[0])
        if guess == f[3]:
            file.write(b'\n\n-------==============-------!!!!------MATCH-----!!!!-------===============------\n')
            counter += 1
        file.write(b'Title: ' + f[2].encode("utf-8"))
        file.write(b'\n')
        file.write(b'Label: ' + f[3].encode("utf-8"))
        file.write(b'\n')
        file.write(b'Guess: ' + guess.encode("utf-8"))
        file.write(b'\n')
        file.write(b'Comment: ' + b'\n' + f[1].encode("utf-8"))
        file.write(b'\n')
        file.write(b'--------------------------------------------------------------------------------\n')
    file.close()

print(len(featuresets))
print(str(counter))
