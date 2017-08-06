import sqlite3
import pickle
from pprint import pprint

from FeatureSet import FeatureSet

# import random
# import nltk
# from nltk import FreqDist
# from nltk.tokenize import word_tokenize

pickle_file = "logreg_classifier.pickle"
database = '../canada_subreddit_test.db'
SQL_query = '''
SELECT c.body, s.label
FROM comments as c, submissions as s
WHERE s.submission_id = c.submission_id
AND s.created <= '2017-08-01'
AND s.created >= '2017-07-27';
'''

fs = FeatureSet(SQL_query,database).make_features()

with open(pickle_file,"rb") as file:
    classifier = pickle.load(file)
    file.close()

counter = 0
for f in fs:
    guess = classifier.classify(f[0])
    print("Label:", f[1])
    print("Guess:", guess)
    print('\n')
    if guess == f[1]:
        counter =+ 1

print(len(featuresets))
print(str(counter))
