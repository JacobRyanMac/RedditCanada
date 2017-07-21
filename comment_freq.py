# Naive bayes

import sqlite3
import random

from nltk import FreqDist
from nltk import NaiveBayesClassifier, classify
from nltk.tokenize import word_tokenize

# from nltk.tokenize import wordpunct_tokenize
# wordpunct_tokenize(s)

db = sqlite3.connect('/Users/jacobmacdougall/canada/canada.db')
cur = db.cursor()
cur.execute('''
SELECT c.body, s.label
FROM submissions as s, comments as c
WHERE s.submission_id = c.submission_id;
''')

documents = [(FreqDist(word_tokenize(c[0])), c[1]) for c in cur]
