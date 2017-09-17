'''
We want to have a script that makes feature sets out of comments
Feature sets are dictionaries.
classify each comment of a submission
create sums of the classifiers
give that as distribution of what the submission is about
'''
import sqlite3
import random
import nltk
import pickle
from nltk import FreqDist
from nltk.tokenize import word_tokenize

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression

SQL_query = '''
SELECT c.body, s.label
FROM submissions as s, comments as c
WHERE s.submission_id = c.submission_id
AND (s.label = "Internet"
OR s.label = "Housing"
OR s.label = "Pot");
'''

# Used to get 4/5 of the data for train, and 1/5 of the data for test
split = lambda x: - int(len(x) / 5)

# Connect to database a obtain all comments with given labels
db = sqlite3.connect('canada_subreddit.db')
cur = db.cursor()
cur.execute(SQL_query)

# tokenize words and add the label, random the order and close the db
comments = [(word_tokenize(c[0]), c[1]) for c in cur]
random.shuffle(comments)
db.close()

# Gather all words from both labels
all_words = []
for c in comments:
    for w in c[0]:
        word = w
        if word[:2] != "//":
            if '*' in word:
                word = word.replace('*','')
            all_words.append(word.lower())
all_words = FreqDist(all_words)
print(all_words.B())

# Get a random set of the words to use as features
word_features = list(all_words.keys())[:4000]

# make feature sets from each comment and mark it with a label
# function returns a feature set of form {"example" : True, "word" : False}
# it will be the length of word_features
def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features
featuresets = [(find_features(comment), label) for (comment, label) in comments]

k = split(featuresets)
training_set = featuresets[:k]
testing_set = featuresets[k:]

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

with open("logreg_classifier.pickle","wb") as save_classifier:
    pickle.dump(LogisticRegression_classifier, save_classifier)
    save_classifier.close()
