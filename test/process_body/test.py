import sqlite3
import pickle
from pprint import pprint

import random
import nltk
from nltk import FreqDist
from nltk.tokenize import word_tokenize

SQL_query = '''
SELECT c.body
FROM comments as c, submissions as s
WHERE s.submission_id = c.submission_id
AND s.created <= '2017-08-01'
AND s.created >= '2017-07-01';
'''

# Connect to database a obtain all comments with given labels
db = sqlite3.connect('../canada_subreddit_test.db')
cur = db.cursor()
cur.execute(SQL_query)
comments = [word_tokenize(c[0]) for c in cur]
db.close()

all_words = []
for c in comments:
    for w in c:
        all_words.append(w.lower())
all_words = FreqDist(all_words)
word_features = list(all_words.keys())
pprint(word_features)
