import sqlite3
import random
import pickle
from nltk import FreqDist
from nltk.tokenize import word_tokenize

# split by n means len(n)/5 are in train and 1/5 is in test
split = lambda x: - int(len(x) / 5)
file_name = "set_housing_pot.pickle"
db = sqlite3.connect('../canada_subreddit_test.db')
cur = db.cursor()
cur.execute('''
SELECT c.body, s.label
FROM submissions as s, comments as c
WHERE s.submission_id = c.submission_id
AND (s.label = 'Housing'
OR s.label = 'Pot');
''')

documents = [(word_tokenize(c[0]), c[1]) for c in cur]
random.shuffle(documents)
db.close()

all_words = []
for w in documents:
    for k in w[0]:
        all_words.append(k.lower())
all_words = FreqDist(all_words)

word_features = list(all_words.keys())[:3000]
def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features
featuresets = [(find_features(rev), category) for (rev, category) in documents]

k = split(featuresets)
training_set = featuresets[:k]
testing_set = featuresets[k:]

with open(file_name,"wb") as save_classifier:
    pickle.dump(training_set, save_classifier)
    pickle.dump(testing_set, save_classifier)
    save_classifier.close()
